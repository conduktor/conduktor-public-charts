#!/bin/bash

# Ensure yq is installed
command -v yq >/dev/null 2>&1 || { echo >&2 "yq is required but it's not installed. Aborting."; exit 1; }

# Add "chart1" and "chart2" keys to the respective values files
yq eval '. as $item ireduce ({}; . * {"console": $item})' ../console/values.yaml > nested-console-values.yaml
yq eval '. as $item ireduce ({}; . * {"gateway": $item})' ../gateway/values.yaml > nested-gateway-values.yaml

# Merge the nested values files with the base values.yaml
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' nested-console-values.yaml nested-gateway-values.yaml > values.yaml

# Clean up temporary nested values files
rm nested-console-values.yaml nested-gateway-values.yaml
