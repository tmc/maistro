#!/bin/bash
# Run sample flow
# Usage: ./run-sample-flow.sh
set -euo pipefail

cd ./samples
unzip -qqo sample.zip
xcrun simctl install Booted Wikipedia.app
maestro test ios-flow.yaml
