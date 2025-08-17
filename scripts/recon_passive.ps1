param([Parameter(Mandatory=$true)][string]$domain)
$Out = "recon_$domain" + (Get-Date -UFormat %Y%m%d)
New-Item -ItemType Directory -Force -Path $Out | Out-Null

# 1) 從 crt.sh 抓取被動子域（低頻請求；請勿高併發）
$subs = try {
  (Invoke-WebRequest -UseBasicParsing "https://crt.sh/?q=%25.$domain&output=json" -TimeoutSec 15).Content |
    ConvertFrom-Json | ForEach-Object { $_.name_value } |
    ForEach-Object { $_.ToLower().Replace("*.","") } | Sort-Object -Unique
} catch { @() }
$subs | Set-Content "$Out\subs.txt"

# 2) 以低速 HEAD 檢查存活，產出 CSV
$rows = foreach ($h in $subs) {
  foreach ($scheme in @('https','http')) {
    $url = "$scheme://$h"
    try {
      $r = Invoke-WebRequest -UseBasicParsing -MaximumRedirection 2 -TimeoutSec 5 -Method Head $url
      $code = [int]$r.StatusCode
    } catch { $code = 0 }
    [pscustomobject]@{
      url=$url; status=$code; title=''; technologies=''; login='no'; api='no'
    }
  }
}
$rows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "$Out\targets.csv"
Write-Host "[+] Done: $Out\targets.csv"
