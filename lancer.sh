#!/bin/sh
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_DIR"
if [ "$(uname -s)" != Linux ] || [ "$(uname -m)" != x86_64 ]; then
 echo 'Ce lanceur cible Linux x86_64. Voir README pour Windows/macOS.' >&2; exit 1
fi
if [ -n "${UZDOOM_BIN:-}" ]; then
 ENGINE_BIN=$UZDOOM_BIN
else
 python3 tools/fetch_engine.py
 ENGINE_BIN="$PROJECT_DIR/runtime/engine/usr/bin/uzdoom"
fi
mkdir -p saves config
exec "$ENGINE_BIN" -iwad "$PROJECT_DIR/dist/crique.ipk3" -config "$PROJECT_DIR/config/crique.ini" -savedir "$PROJECT_DIR/saves" -noautoload -nojoy +vid_preferbackend 0 +screenblocks 12 +crosshair 0 +cl_run false +freelook true +map MAP01 "$@"
