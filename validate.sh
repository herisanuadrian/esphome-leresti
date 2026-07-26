#!/bin/bash

# ESPHome YAML Validator — Claude Code safe version
# Usage: ./validate.sh <config-name>

CONFIG_NAME=${1:-esp-tourbillon}
CONFIG_FILE="${CONFIG_NAME}.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    CONFIG_FILE="config/${CONFIG_NAME}.yaml"
fi

source ../esphome-env/bin/activate

if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: Config file not found: ${CONFIG_NAME}.yaml"
    exit 1
fi

# Capture output, filter immediately — never let full config reach stdout
RESULT=$(esphome config "$CONFIG_FILE" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "PASS: $CONFIG_NAME validated successfully"
else
    # Extract only actionable lines
    echo "FAIL: $CONFIG_NAME"
    echo "$RESULT" | grep -E "^(ERROR|WARNING|Invalid|Failed|in \/)" | head -20
fi

exit $EXIT_CODE