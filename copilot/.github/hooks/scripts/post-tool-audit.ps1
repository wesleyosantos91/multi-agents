param()
$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { return }
try { $inputObj = $raw | ConvertFrom-Json -ErrorAction Stop } catch { return }

$text = $raw
if ($inputObj.toolResult) { $text += "`n" + ($inputObj.toolResult | Out-String) }
if ($text -match '(?i)AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|PRIVATE\s+KEY|password\s*=') {
  Write-Error '[quality-gates] Possivel segredo detectado no output.'
}
