#!/usr/bin/env bash
# Deploy frontend to Vercel using Vercel CLI (requires VERCEL_TOKEN)
set -e
if [ -z "$VERCEL_TOKEN" ]; then
  echo "VERCEL_TOKEN not set. Use GitHub secret VERCEL_TOKEN or set VERCEL_TOKEN in environment."
  exit 1
fi
npm i -g vercel
cd frontend
vercel --token "$VERCEL_TOKEN" --prod --confirm
