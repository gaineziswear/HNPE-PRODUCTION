#!/usr/bin/env bash
set -e
cp .env.example .env || true
docker compose up -d db
sleep 5
echo "DB started; run migrations manually or with your tool of choice."
