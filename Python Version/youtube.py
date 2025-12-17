from generate_token import get_authenticated_service
import datetime

PLAYLIST_ID = "PLV0e0d_ZUComWaSZdRi2wLH9MSYujkZvz"


def get_playlist_id(youtube_service, playlist_name):
    """
    Get the playlist ID for a given playlist name.
    """
    request = youtube_service.playlists().list(
        part='snippet',
        mine=True,
        maxResults=50
    )
    response = request.execute()

    for playlist in response['items']:
        if playlist['snippet']['title'] == playlist_name:
            return playlist['id']
    return None


def update_video_name(youtube_service, video_id, new_title):
    request = youtube_service.videos().update(
        part='snippet',
        body={
            'id': video_id,
            'snippet': {
                'title': new_title
            }
        }
    )
    request.execute()


def check_video_in_playlist(youtube_service, video_id, playlist_id):
    """
    Check if a video is already in the given playlist.
    """
    request = youtube_service.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    for item in response['items']:
        if item['snippet']['resourceId']['videoId'] == video_id:
            return True
    return False


def add_video_to_playlist(youtube_service, video_id, playlist_id):
    """
    Add a video to the specified playlist.
    """
    # update_video_name(youtube_service, video_id)
    request = youtube_service.playlistItems().insert(
        part='snippet',
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    )
    request.execute()
    print(f"Added video {video_id} to the playlist.")


def list_unlisted_live_videos(youtube_service):
    # Call the YouTube API to list live broadcasts from the authenticated user's channel
    request = youtube_service.liveBroadcasts().list(
        part='snippet, status',
        mine=True,
        maxResults=50
    )
    response = request.execute()

    for item in response.get('items', []):
        if item['status']['privacyStatus'] != 'private':
            continue

        video_id = item.get("id")

        if not video_id:
            continue

        in_playlist = check_video_in_playlist(
            youtube_service, video_id, PLAYLIST_ID)

        if in_playlist:
            continue

        add_video_to_playlist(youtube_service, video_id, PLAYLIST_ID)


def get_existing_stream_id(youtube, stream_name):
    """Retrieve the stream ID based on the stream key."""
    request = youtube.liveStreams().list(
        part="snippet",
        mine=True  # Ensure you get streams related to your account
    )
    response = request.execute()

    # Find the stream that matches the stream_key
    try:
        for stream in response['items']:

            id = stream['id']
            current_stream_name = stream["snippet"]["title"]
            if current_stream_name == stream_name:
                return id
    except:
        pass

    return None  # If the stream is not found


def create_scheduled_broadcast(youtube, title, description, start_time):
    """Create a scheduled YouTube live broadcast."""
    request = youtube.liveBroadcasts().insert(
        part="snippet,contentDetails,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "scheduledStartTime": start_time  # Time in ISO 8601 format
            },
            "status": {
                "privacyStatus": "unlisted"  # Can be 'private', 'unlisted', 'public'
            },
            "contentDetails": {
                "monitorStream": {
                    "enableMonitorStream": False  # Optional: Disable monitoring
                }
            }
        }
    )
    response = request.execute()
    return response


def bind_stream_to_broadcast(youtube, broadcast_id, stream_id):
    """Bind the existing stream to the broadcast."""
    request = youtube.liveBroadcasts().bind(
        part="id,contentDetails",
        id=broadcast_id,
        streamId=stream_id
    )
    response = request.execute()
    return response


def go_live(youtube, broadcast_id):
    """Transition a scheduled broadcast to live."""
    youtube.liveBroadcasts().transition(
        part="status",
        broadcastStatus="live",
        id=broadcast_id
    ).execute()
    add_video_to_playlist(youtube, broadcast_id, PLAYLIST_ID)


def go_end_stream(youtube, broadcast_id):
    """Transition a scheduled broadcast to end the stream."""
    youtube.liveBroadcasts().transition(
        part="status",
        broadcastStatus="complete",  # Mark the stream as complete (ended)
        id=broadcast_id
    ).execute()


def gen_stream_name_desc(camera: str, time:datetime) -> str:
    return f"{camera.split()[0] + time.split(".")[0]}", f"This stream is scheduled via the API for {camera}"

def gen_start_time()-> datetime:
        return (datetime.datetime.now(datetime.timezone.utc) +
                  datetime.timedelta(hours=2)).isoformat()

if __name__ == '__main__':
    # Authenticate and get the service object
    youtube = get_authenticated_service()

    # playlist_id = get_playlist_id(youtube, "Cameras")

    # list_unlisted_live_videos(youtube)

    # Define stream details
    camera = "Yard Camera"
    title, description = gen_stream_name_desc(camera, gen_start_time())

    # Schedule the start time (for example, 1 hour from now)


    # Create scheduled broadcast
    broadcast_response = create_scheduled_broadcast(
        youtube, title, description, start_time)
    broadcast_id = broadcast_response['id']
    print(f"Scheduled Broadcast Created: {broadcast_id}")

    stream_id = get_existing_stream_id(youtube, camera)
    if not stream_id:
        print("Stream not found.")
        exit()

    bind_response = bind_stream_to_broadcast(youtube, broadcast_id, stream_id)
    print(f"Stream linked to broadcast: {bind_response['id']}")

    # Create stream and link to the broadcast
    # add_video_to_playlist(youtube, PLAYLIST_ID, broadcast_id)

    go_live(youtube, broadcast_id)
    print(f"Broadcast {broadcast_id} is now live!")
    # print(f"Stream created and linked to broadcast: {stream_response['id']}")
