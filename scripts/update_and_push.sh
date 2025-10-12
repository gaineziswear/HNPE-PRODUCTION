#!/usr/bin/env bash
set -e
if [ ! -d .git ]; then echo "Run inside repo root"; exit 1; fi

git add backend/core/gem_scanner.py backend/.env.example scripts/update_and_push.sh
git commit -m "feat: add advanced gem scanner"
git push origin main
echo "✅ Files pushed successfully."
