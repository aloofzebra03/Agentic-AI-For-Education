# MCP-assisted manual deploy: git push -> docker push -> SSM redeploy on EC2 -> health check
# Usage:
#   .\deployment\deploy.ps1 -Message "fix: kannada sim latency"
#   .\deployment\deploy.ps1 -SkipGit -SkipDocker          # image already on Hub; only restart EC2
#   .\deployment\deploy.ps1 -RedeployOnly                 # same as -SkipGit -SkipDocker

param(
    [string]$Message,
    [switch]$SkipGit,
    [switch]$SkipDocker,
    [switch]$RedeployOnly,
    [string]$ConfigPath = "$PSScriptRoot\deploy.config.json"
)

$ErrorActionPreference = "Stop"

if ($RedeployOnly) {
    $SkipGit = $true
    $SkipDocker = $true
}

if (-not (Test-Path $ConfigPath)) {
    Write-Error "Missing $ConfigPath - copy deploy.config.example.json to deploy.config.json and set ec2InstanceId."
}

$config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
$repoRoot = Split-Path $PSScriptRoot -Parent

function Require-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $name"
    }
}

Require-Command git
Require-Command aws
Require-Command docker

if ($config.ec2InstanceId -match '^i-XXXXXXXX') {
    throw "Set ec2InstanceId in deploy.config.json (AWS Console -> EC2 -> Instances -> Instance ID)."
}

Write-Host "=== EduAgent deploy ===" -ForegroundColor Cyan
Write-Host "Image: $($config.dockerImage)"
Write-Host "EC2:   $($config.ec2InstanceId) ($($config.ec2PublicIp))"
Write-Host "Region: $($config.awsRegion)"
Write-Host ""

# --- Git ---
if (-not $SkipGit) {
    Push-Location $repoRoot
    try {
        $status = git status --porcelain
        if (-not $status) {
            Write-Host "[git] Working tree clean - nothing to commit." -ForegroundColor Yellow
        }
        else {
            if (-not $Message) {
                throw "Uncommitted changes but no -Message provided."
            }
            Write-Host "[git] Committing..."
            git add -A
            git commit -m $Message
        }
        Write-Host "[git] Pushing to $($config.gitRemote)/$($config.gitBranch)..."
        git push $config.gitRemote $config.gitBranch
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "[git] Skipped" -ForegroundColor DarkGray
}

# --- Docker build & push ---
if (-not $SkipDocker) {
    Push-Location $repoRoot
    try {
        Write-Host "[docker] Building $($config.dockerImage)..."
        docker build -t $config.dockerImage .
        Write-Host "[docker] Pushing..."
        docker push $config.dockerImage
    }
    finally {
        Pop-Location
    }
}
else {
    Write-Host "[docker] Skipped" -ForegroundColor DarkGray
}

# --- SSM redeploy on EC2 ---
$redeployScript = Join-Path $PSScriptRoot "redeploy-fastapi.sh"
if (-not (Test-Path $redeployScript)) {
    throw "Missing $redeployScript"
}

$remoteScript = @"
export DOCKER_IMAGE='$($config.dockerImage)'
export CONTAINER_NAME='$($config.containerName)'
export ENV_FILE_ON_EC2='$($config.envFileOnEc2)'
export HOST_PORT='$($config.hostPort)'
bash -s <<'DEPLOY_EOF'
$(Get-Content $redeployScript -Raw)
DEPLOY_EOF
"@

Write-Host "[ssm] Sending redeploy command to $($config.ec2InstanceId)..."
$paramFile = Join-Path $env:TEMP "ssm-deploy-params.json"
@{ commands = @($remoteScript) } | ConvertTo-Json | Set-Content $paramFile -Encoding UTF8

$commandId = aws ssm send-command `
    --region $config.awsRegion `
    --document-name $config.ssmDocument `
    --instance-ids $config.ec2InstanceId `
    --parameters "file://$paramFile" `
    --query "Command.CommandId" `
    --output text

if (-not $commandId) {
    throw "SSM send-command failed (no CommandId). Is the instance registered in Systems Manager?"
}

Write-Host "[ssm] CommandId: $commandId - waiting..."
$status = "InProgress"
$deadline = (Get-Date).AddMinutes(10)

while ($status -in @("Pending", "InProgress", "Delayed") -and (Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 5
    $inv = aws ssm list-command-invocations `
        --region $config.awsRegion `
        --command-id $commandId `
        --details `
        --query "CommandInvocations[0].{Status:Status,Output:CommandPlugins[0].Output}" `
        --output json | ConvertFrom-Json
    $status = $inv.Status
    Write-Host "  status: $status"
}

$result = aws ssm get-command-invocation `
    --region $config.awsRegion `
    --command-id $commandId `
    --instance-id $config.ec2InstanceId `
    --output json | ConvertFrom-Json

Write-Host ""
Write-Host "=== SSM output ===" -ForegroundColor Cyan
Write-Host $result.StandardOutputContent
if ($result.StandardErrorContent) {
    Write-Host "=== SSM stderr ===" -ForegroundColor Yellow
    Write-Host $result.StandardErrorContent
}

if ($result.Status -ne "Success") {
    throw "SSM redeploy failed with status: $($result.Status)"
}

# --- Public health check ---
Write-Host ""
Write-Host "[health] $($config.healthUrl)"
try {
    $health = Invoke-RestMethod -Uri $config.healthUrl -TimeoutSec 30
    $health | ConvertTo-Json -Compress
    Write-Host "=== Deploy complete ===" -ForegroundColor Green
}
catch {
    throw "Public health check failed: $($_.Exception.Message)"
}
