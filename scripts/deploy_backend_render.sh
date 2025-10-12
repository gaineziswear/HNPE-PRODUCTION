#!/usr/bin/env bash
# Deploy backend Docker image to Render via Render API
# Requires RENDER_API_KEY env var and a service already created on Render (you can create it once via UI)
set -e
if [ -z "$RENDER_API_KEY" ]; then
  echo "RENDER_API_KEY not set. Set it in GitHub Actions secrets."
  exit 1
fi
echo "This script is a placeholder that triggers Render deploy via the Render REST API."
# Example: trigger a deploy by hitting the deploy hook or Render API
# curl -X POST -H "Accept: application/json" -H "Authorization: Bearer $RENDER_API_KEY" \
#  https://api.render.com/deploy/srv-xxxx/deploys
echo "Replace the commented curl with your Render service id and call the API."
