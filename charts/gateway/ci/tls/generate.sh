#!/usr/bin/env bash
# Regenerates selfsigned.jks used by CI tests that require TLS.
#
# SANs cover:
#   - kafka.example.com                                      (test 05 external advertised host)
#   - *.kafka.example.com                                    (test 05 broker/bootstrap wildcard)
#   - *.ct-gateway-06-listener-internal-sni.svc.cluster.local  (test 06 internal SNI broker services)
#
# The namespace prefix "ct-gateway-06-listener-internal-sni" is derived from the scenario
# name "06-listener-internal-sni" (file: 06-listener-internal-sni-values.yaml).
# If you rename the scenario, update the SAN here and regenerate.
#
# Requirements: keytool (JDK)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/selfsigned.jks"
ALIAS="gateway"
PASS="conduktor"
VALIDITY=3650  # 10 years

SAN="dns:kafka.example.com,dns:*.kafka.example.com,dns:*.ct-gateway-06-listener-internal-sni.svc.cluster.local"

rm -f "$OUT"

keytool -genkeypair \
  -alias "$ALIAS" \
  -keyalg RSA \
  -keysize 2048 \
  -dname "CN=gateway, O=Conduktor CI, C=FR" \
  -validity "$VALIDITY" \
  -keystore "$OUT" \
  -storepass "$PASS" \
  -keypass "$PASS" \
  -ext "SAN=$SAN" \
  -noprompt

echo "Generated: $OUT"
keytool -list -v -keystore "$OUT" -storepass "$PASS" | grep -A 10 "SubjectAlternativeName"
