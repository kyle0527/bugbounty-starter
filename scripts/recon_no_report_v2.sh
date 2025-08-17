#!/usr/bin/env bash
# scripts/recon_no_report_v2.sh
# 用途：對 In‑Scope 根網域做被動枚舉與低並發存活探測，輸出 targets.csv
set -euo pipefail

SCOPE_FILE="${1:-scope.txt}"
[[ -f "$SCOPE_FILE" ]] || { echo "找不到 $SCOPE_FILE"; exit 1; }

date_tag="$(date +%Y%m%d)"
while read -r DOMAIN; do
  [[ -z "$DOMAIN" ]] && continue
  OUT="recon_${DOMAIN}_${date_tag}"
  mkdir -p "$OUT"

  echo "[*] Subdomain (passive) for $DOMAIN ..."
  subfinder -d "$DOMAIN" -silent | sort -u > "$OUT/subs.txt"

  echo "[*] Liveness & fingerprint (low concurrency) ..."
  httpx -l "$OUT/subs.txt"        -silent -json -no-color        -status-code -title -tech-detect -follow-redirects        -threads 25 -rate-limit 50 > "$OUT/httpx.json"

  echo "[*] Build CSV ..."
  jq -r '
    . as $o |
    [
      (.url // ""),
      (.status_code // 0),
      (.title // ""),
      ((.technologies // []) | join("|")),
      (if ((.title // "") | test("login|sign[ -]?in|account"; "i"))
          or ((.url // "") | test("/login|/signin|/auth"; "i"))
       then "yes" else "no" end),
      (if ((.url // "") | test("://api\\.|/api/|/graphql"; "i"))
          or ((.title // "") | test("api|graphql|swagger|openapi"; "i"))
       then "yes" else "no" end)
    ] | @csv
  ' "$OUT/httpx.json" > "$OUT/targets.csv"

  echo "[+] Done: $OUT/targets.csv"
done < "$SCOPE_FILE"
