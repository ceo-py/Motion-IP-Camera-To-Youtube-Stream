#!/bin/bash
# Send a message to Discord webhook when Motion detects motion

WEBHOOK_URL="DISCORD WEB HOOK LINK OR ANY OTHER WEBHOOK THAT YOU WANT TO USE"

# Customize the message here
MESSAGE="⚠️ Motion detected by camera in Kitchen at $(date '+%Y-%m-%d %H:%M:%S')"

# Send to Discord
curl -H "Content-Type: application/json" \
     -X POST \
     -d "{\"content\": \"$MESSAGE\"}" \
     "$WEBHOOK_URL" \
     --silent --output /dev/null