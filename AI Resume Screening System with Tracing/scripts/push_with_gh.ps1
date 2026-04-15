<#
PowerShell helper to create a GitHub repo and push the current project using `gh` CLI.
Prerequisites: GitHub CLI installed and `gh auth login` performed.
#>
param(
  [string]$repoName = "IN226104302_FASTAPI",
  [string]$visibility = "public"
)

Write-Host "Creating repo $repoName (visibility=$visibility) via gh..."
gh repo create $repoName --$visibility --source . --remote origin --push

Write-Host "Repo created and pushed. Open: https://github.com/$(gh api user --jq .login)/$repoName"
