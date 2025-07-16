# test

Just a **test** repo

# pwsh

```pwsh
# keep the latest run, delete the rest
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runs = gh run list --limit 100 --json databaseId --jq ".[1:] | .[].databaseId"

foreach ($id in $runs) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}
# verbose
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runs = gh run list --limit 100 --json databaseId --jq ".[1:] | .[].databaseId"

foreach ($id in $runs) {
    Write-Output "Deleting run ID $id from $repo..."
    gh api "repos/$repo/actions/runs/$id" -X DELETE

    if ($LASTEXITCODE -eq 0) {
        Write-Output "Successfully deleted run ID $id"
    } else {
        Write-Output "Failed to delete run ID $id"
    }
}
```

```pwsh
# delete all runs
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runIds = gh run list --json databaseId --jq ".[].databaseId"

foreach ($id in $runIds) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}

# verbose
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runIds = gh run list --json databaseId --jq ".[].databaseId"

foreach ($id in $runIds) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
    if ($LASTEXITCODE -eq 0) {
        Write-Output "Deleted run ID $id"
    } else {
        Write-Output "Failed to delete run ID $id"
    }
}
```
