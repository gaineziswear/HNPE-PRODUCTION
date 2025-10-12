#!/usr/bin/env bash
# Deploy telegram bot to Render
set -e
if [ -z "$RENDER_API_KEY" ]; then
  echo "RENDER_API_KEY not set. Set it in GitHub Actions secrets."
  exit 1
fi
echo "Trigger bot deploy via Render API (replace srv-xxxx with your service id)"
# curl -X POST -H "Authorization: Bearer $RENDER_API_KEY" \
#  https://api.render.com/deploy/srv-xxxx/deploys
echo "Update this script with the Render service id for the bot and uncomment the curl."
