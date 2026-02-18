#!/bin/bash

# Sacred Essence v3.1 Bridge Script: memo_v3
# Author: Zhu (鑄)

ENGINE_DIR="/home/nerv0/.openclaw/workspace/memory/octagram/engine"
PYTHON_BIN="python3"

# Default values
TOPIC="general"
TITLE=""
CONTENT=""
ABSTRACT=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --topic) TOPIC="$2"; shift ;;
        --title) TITLE="$2"; shift ;;
        --content) CONTENT="$2"; shift ;;
        --abstract) ABSTRACT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [[ -z "$TITLE" ]] || [[ -z "$CONTENT" ]]; then
    echo "Usage: memo_v3 --title \"Title\" --content \"Content\" [--topic \"Topic\"] [--abstract \"Abstract\"]"
    exit 1
fi

# Call engine
$PYTHON_BIN "$ENGINE_DIR/main.py" encode \
    --topic "$TOPIC" \
    --title "$TITLE" \
    --content "$CONTENT" \
    --abstract "$ABSTRACT"
