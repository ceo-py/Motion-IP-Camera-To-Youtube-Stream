import redis
from config import REDIS
from utils import print_message

# Redis connection setup (replace with your Redis host and port if needed)
redis_client = redis.StrictRedis(host=REDIS["HOST"], port=REDIS["PORT"], db=0, decode_responses=True)


def save_broadcast_id_to_redis(camera_name: str, broadcast_id: str) -> None:
    """Save the broadcast ID to Redis with a key based on the camera name."""
    redis_key = f"{camera_name}_broadcast_id"
    redis_client.set(redis_key, broadcast_id)
    print_message(f"Saved broadcast ID {broadcast_id} to Redis for camera {camera_name}.")

def get_broadcast_id_from_redis(camera_name: str) -> str:
    """Retrieve the broadcast ID from Redis for the given camera."""
    redis_key = f"{camera_name}_broadcast_id"
    broadcast_id = redis_client.get(redis_key)
    if broadcast_id:
        redis_client.delete(redis_key)
        print_message(f"Retrieved and deleted broadcast ID {broadcast_id} from Redis for camera {camera_name}.")
        return broadcast_id
    else:
        print_message(f"No broadcast ID found for camera {camera_name} in Redis.")
        return None



