#!/bin/bash

set -e

UPLOAD=false
DEVICE=""
CONFIG_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --upload)
      UPLOAD=true
      shift
      ;;
    --device)
      DEVICE="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $(basename "$0") <file.yaml> [--upload [--device PORT]]"
      echo "  file.yaml          ESPHome config file to build"
      echo "  --upload           Compile and upload to device via USB"
      echo "  --device PORT      Serial port (e.g., /dev/ttyUSB0, /dev/ttyACM0)"
      echo "                      Auto-detected if not specified"
      exit 0
      ;;
    *)
      if [[ -n "$CONFIG_FILE" ]]; then
        echo "Error: Unknown option $1" >&2
        exit 1
      fi
      CONFIG_FILE="$1"
      shift
      ;;
  esac
done

if [[ -z "$CONFIG_FILE" ]]; then
  echo "Error: no config file given" >&2
  echo "Usage: $(basename "$0") <file.yaml> [--upload [--device PORT]]" >&2
  exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: $CONFIG_FILE not found" >&2
  exit 1
fi

# Extract current version and increment (skip if not defined in substitutions)
CURRENT_VERSION=$(grep "device_version:" "$CONFIG_FILE" | sed 's/.*"\(.*\)".*/\1/')
if [[ -z "$CURRENT_VERSION" ]]; then
  echo "No device_version found in $CONFIG_FILE, skipping version increment"
else
  MAJOR=$(echo "$CURRENT_VERSION" | cut -d. -f1)
  MINOR=$(echo "$CURRENT_VERSION" | cut -d. -f2)
  NEW_MINOR=$((MINOR + 1))
  NEW_VERSION="$MAJOR.$NEW_MINOR"

  echo "Incrementing version: $CURRENT_VERSION → $NEW_VERSION"
  sed -i.bak "s/device_version: \"$CURRENT_VERSION\"/device_version: \"$NEW_VERSION\"/" "$CONFIG_FILE"
  rm -f "$CONFIG_FILE.bak"
fi

echo "Compiling $CONFIG_FILE..."
esphome compile "$CONFIG_FILE"

if [[ "$UPLOAD" == true ]]; then
  if [[ -n "$DEVICE" ]]; then
    echo "Uploading via USB ($DEVICE)..."
    esphome upload "$CONFIG_FILE" --device "$DEVICE"
  else
    echo "Uploading via WiFi/OTA..."
    esphome upload "$CONFIG_FILE"
  fi
fi
