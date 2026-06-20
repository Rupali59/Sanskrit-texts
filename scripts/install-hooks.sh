#!/usr/bin/env bash
# install-hooks.sh — one-shot setup. Points git at the committed .githooks/ dir.
#
# Per-clone setup: bash scripts/install-hooks.sh
# Idempotent.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .githooks ]]; then
  echo "install-hooks: .githooks/ missing; nothing to install." >&2
  exit 1
fi

chmod +x .githooks/* 2>/dev/null || true

current="$(git config --get core.hooksPath 2>/dev/null || true)"
if [[ "$current" == ".githooks" ]]; then
  echo "install-hooks: already configured (core.hooksPath=.githooks)"
  exit 0
fi

git config core.hooksPath .githooks
echo "install-hooks: set core.hooksPath=.githooks"
echo "Active hooks:"
ls -1 .githooks/
