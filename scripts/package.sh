#!/usr/bin/env bash
# Package one plugin (or all) into dist/<name>-<version>.zip for upload to
# chatgpt.com / platform.openai.com. Zips are build artifacts, not source of
# truth — the repo folder is. Never edit a zip in place.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"
mkdir -p "$DIST"

targets=("$@")
if [ ${#targets[@]} -eq 0 ]; then
  while IFS= read -r p; do targets+=("$(basename "$p")"); done < <(find "$ROOT/plugins" -mindepth 1 -maxdepth 1 -type d | sort)
fi

for name in "${targets[@]}"; do
  dir="$ROOT/plugins/$name"
  [ -d "$dir" ] || { echo "skip: no plugin dir $name" >&2; continue; }
  manifest="$dir/plugin.json"
  if [ ! -f "$manifest" ]; then
    manifest="$dir/.codex-plugin/plugin.json"
  fi
  if [ ! -f "$manifest" ]; then echo "skip: $name has no plugin.json" >&2; continue; fi

  version="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$manifest")"
  out="$DIST/$name-$version.zip"
  rm -f "$out"
  # Zip from inside plugins/ so the plugin dir is the single top-level directory
  # in the archive. A nested plugins/<name>/ root can confuse the upload parser.
  ( cd "$ROOT/plugins" && zip -r -X "$out" "$name" -x '*.DS_Store' >/dev/null )
  echo "built $out"
done