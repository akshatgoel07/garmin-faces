#!/usr/bin/env bash
# usage: scripts/face.sh build|run|export|shot <face> [device]
set -euo pipefail
cmd=${1:?build|run|export|shot} face=${2:?face folder under faces/} dev=${3:-fr965}
root=$(cd "$(dirname "$0")/.." && pwd)
dir="$root/faces/$face"
sdk=$(cat "$HOME/Library/Application Support/Garmin/ConnectIQ/current-sdk.cfg")
key="$HOME/.garmin/developer_key.der"
mkdir -p "$dir/bin"
case $cmd in
  build) "$sdk/bin/monkeyc" -d "$dev" -f "$dir/monkey.jungle" -o "$dir/bin/$face.prg" -y "$key" -w -l 1 ;;
  run)   "$sdk/bin/connectiq" >/dev/null 2>&1 & sleep 6
         "$sdk/bin/monkeydo" "$dir/bin/$face.prg" "$dev" ;;
  export) "$sdk/bin/monkeyc" -e -f "$dir/monkey.jungle" -o "$dir/bin/$face.iq" -y "$key" -r -w
          ls -la "$dir/bin/$face.iq" ;;
  shot)  out=${4:-$dir/bin/sim.png}
         osascript -e 'tell application "System Events" to set frontmost of process "simulator" to true' >/dev/null
         sleep 1
         g=$(osascript -e 'tell application "System Events" to tell process "simulator" to get {position, size} of window 1' | tr -d ' ')
         screencapture -x -R "$g" "$out" && echo "$out" ;;
  *) echo "unknown command $cmd" >&2; exit 1 ;;
esac
