<#
Usage: .\push_to_remote.ps1 -RemoteUrl "https://github.com/<owner>/<repo>.git" [-Branch main]

This helper will:
 - add or update the `origin` remote
 - rename current branch to the provided branch name if needed
 - push the branch and set upstream
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$RemoteUrl,
    [string]$Branch = "main"
)

Write-Host "Adding/updating remote origin -> $RemoteUrl"
try {
    $existing = git remote get-url origin
    if ($existing) {
        Write-Host "Remote 'origin' exists. Updating URL."
        git remote set-url origin $RemoteUrl
    }
} catch {
    Write-Host "Remote 'origin' does not exist. Adding remote."
    git remote add origin $RemoteUrl
}

# Determine current branch
$current = (git rev-parse --abbrev-ref HEAD).Trim()
Write-Host "Current branch: $current"
if ($current -ne $Branch) {
    Write-Host "Renaming branch $current -> $Branch"
    git branch -m $Branch
}

Write-Host "Pushing to origin/$Branch and setting upstream"
git push -u origin $Branch
Write-Host "Push complete."
