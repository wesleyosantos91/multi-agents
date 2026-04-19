param()
$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { return }
try { $inputObj = $raw | ConvertFrom-Json -ErrorAction Stop } catch { return }

$tool = [string]$inputObj.toolName
$argsRaw = [string]$inputObj.toolArgs
$command = $argsRaw
$targetPath = $argsRaw

try {
  $parsed = $argsRaw | ConvertFrom-Json -ErrorAction Stop
  if ($parsed.command) { $command = [string]$parsed.command }
  if ($parsed.path) { $targetPath = [string]$parsed.path }
  if ($parsed.filePath) { $targetPath = [string]$parsed.filePath }
} catch {}

$denyReason = $null

if ($tool -match '^(bash|powershell|execute)$') {
  if ($command -match '(?i)git\s+push\s+--force|git\s+push\s+-f|git\s+reset\s+--hard|rm\s+-rf\s+/') {
    $denyReason = 'Comando destrutivo bloqueado.'
  }
}

if (-not $denyReason -and $tool -match '^(edit|create|write)$') {
  if ($targetPath -match '(?i)\.(env|pem|key|secret|credentials|token)$') {
    $denyReason = 'Edicao de arquivo sensivel bloqueada.'
  }
}

if ($denyReason) {
  @{ permissionDecision = 'deny'; permissionDecisionReason = $denyReason } | ConvertTo-Json -Compress
} else {
  @{ permissionDecision = 'allow' } | ConvertTo-Json -Compress
}
