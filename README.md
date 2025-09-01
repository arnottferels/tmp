# GitHub cleanup scripts

Scripts to clean up GitHub actions runs and deployments. Deletions are irreversible.

## Workflow

### Delete all workflow runs

```pwsh
# delete all runs
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runIds = gh run list --json databaseId --jq ".[].databaseId"

foreach ($id in $runIds) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}
```

```pwsh
# verbose: delete all runs with confirmation (y/n/a/q, default q)
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runIds = gh run list --json databaseId --jq ".[].databaseId"

# list all run IDs first
if ($runIds.Count -eq 0) {
    Write-Output "No runs to delete"
} else {
    Write-Output "Found run IDs to delete:"
    $runIds | ForEach-Object { Write-Output $_ }
}

# options:
# y = yes (delete this one)
# n = no (skip this one)
# a = yes to all
# q = quit (skip all next ones, default if Enter)

$deleteAll = $false; $quit = $false

foreach ($id in $runIds) {
    if ($deleteAll) { gh api "repos/$repo/actions/runs/$id" -X DELETE; continue }
    if ($quit) { Write-Output "Skipped run $id (quit)"; continue }

    $choice = Read-Host "Delete run $id? (y/n/a/q, default q)"
    switch ($choice.ToLower()) {
        'y' { gh api "repos/$repo/actions/runs/$id" -X DELETE }
        'n' { Write-Output "Skipped run $id" }
        'a' { $deleteAll = $true; gh api "repos/$repo/actions/runs/$id" -X DELETE }
        'q' { $quit = $true; Write-Output "Skipped run $id (quit)" }
        default { $quit = $true; Write-Output "Skipped run $id (quit by default)" }
    }

    if ($LASTEXITCODE -eq 0 -and ($choice -match 'y|a')) { Write-Output "Deleted run $id" }
    elseif ($choice -match 'y|a') { Write-Output "Failed run $id" }
}
```

### Keep latest run, delete the rest

```pwsh
# keep latest, delete older runs
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runs = gh run list --limit 100 --json databaseId --jq ".[1:] | .[].databaseId"

foreach ($id in $runs) {
    gh api "repos/$repo/actions/runs/$id" -X DELETE
}
```

```pwsh
# verbose: keep latest, delete older runs with confirmation (y/n/a/q, default q)
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$runs = gh run list --limit 100 --json databaseId --jq ".[1:] | .[].databaseId"

# list all run IDs first
if ($runs.Count -eq 0) {
    Write-Output "No runs to delete"
} else {
    Write-Output "Found run IDs to delete (all except latest):"
    $runs | ForEach-Object { Write-Output $_ }
}

# options:
# y = yes (delete this one)
# n = no (skip this one)
# a = yes to all
# q = quit (skip all next ones, default if Enter)

$deleteAll = $false; $quit = $false

foreach ($id in $runs) {
    if ($deleteAll) { gh api "repos/$repo/actions/runs/$id" -X DELETE; continue }
    if ($quit) { Write-Output "Skipped run $id (quit)"; continue }

    $choice = Read-Host "Delete run $id? (y/n/a/q, default q)"
    switch ($choice.ToLower()) {
        'y' { gh api "repos/$repo/actions/runs/$id" -X DELETE }
        'n' { Write-Output "Skipped run $id" }
        'a' { $deleteAll = $true; gh api "repos/$repo/actions/runs/$id" -X DELETE }
        'q' { $quit = $true; Write-Output "Skipped run $id (quit)" }
        default { $quit = $true; Write-Output "Skipped run $id (quit by default)" }
    }

    if ($LASTEXITCODE -eq 0 -and ($choice -match 'y|a')) { Write-Output "Deleted run $id" }
    elseif ($choice -match 'y|a') { Write-Output "Failed run $id" }
}
```

## Deployment

### Delete all deployments

```pwsh
# delete all deployments
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$deploymentIds = gh api "repos/$repo/deployments" --jq ".[].id"

foreach ($id in $deploymentIds) {
    gh api "repos/$repo/deployments/$id" -X DELETE
}
```

```pwsh
# verbose: delete all deployments with confirmation (y/n/a/q, default q)
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$deploymentIds = gh api "repos/$repo/deployments" --jq ".[].id"

# list all deployment IDs first
if ($deploymentIds.Count -eq 0) {
    Write-Output "No deployments to delete"
} else {
    Write-Output "Found deployment IDs to delete:"
    $deploymentIds | ForEach-Object { Write-Output $_ }
}

# options:
# y = yes (delete this one)
# n = no (skip this one)
# a = yes to all
# q = quit (skip all next ones, default if Enter)

$deleteAll = $false; $quit = $false

foreach ($id in $deploymentIds) {
    if ($deleteAll) { gh api "repos/$repo/deployments/$id" -X DELETE; continue }
    if ($quit) { Write-Output "Skipped deployment $id (quit)"; continue }

    $choice = Read-Host "Delete deployment $id? (y/n/a/q, default q)"
    switch ($choice.ToLower()) {
        'y' { gh api "repos/$repo/deployments/$id" -X DELETE }
        'n' { Write-Output "Skipped deployment $id" }
        'a' { $deleteAll = $true; gh api "repos/$repo/deployments/$id" -X DELETE }
        'q' { $quit = $true; Write-Output "Skipped deployment $id (quit)" }
        default { $quit = $true; Write-Output "Skipped deployment $id (quit by default)" }
    }

    if ($LASTEXITCODE -eq 0 -and ($choice -match 'y|a')) { Write-Output "Deleted deployment $id" }
    elseif ($choice -match 'y|a') { Write-Output "Failed deployment $id" }
}
```

### Keep latest deployment, delete the rest

```pwsh
# keep latest deployment, delete older ones
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$deploymentIds = gh api "repos/$repo/deployments" --jq ".[1:] | .[].id"

foreach ($id in $deploymentIds) {
    gh api "repos/$repo/deployments/$id" -X DELETE
}
```

```pwsh
# verbose: keep latest, delete older deployments with confirmation (y/n/a/q, default q)
$repo = gh repo view --json nameWithOwner --jq ".nameWithOwner"
$deploymentIds = gh api "repos/$repo/deployments" --jq ".[1:] | .[].id"

# list all deployment IDs first
if ($deploymentIds.Count -eq 0) {
    Write-Output "No deployments to delete"
} else {
    Write-Output "Found deployment IDs to delete (all except latest):"
    $deploymentIds | ForEach-Object { Write-Output $_ }
}

# options:
# y = yes (delete this one)
# n = no (skip this one)
# a = yes to all
# q = quit (skip all next ones, default if Enter)

$deleteAll = $false; $quit = $false

foreach ($id in $deploymentIds) {
    if ($deleteAll) { gh api "repos/$repo/deployments/$id" -X DELETE; continue }
    if ($quit) { Write-Output "Skipped deployment $id (quit)"; continue }

    $choice = Read-Host "Delete deployment $id? (y/n/a/q, default q)"
    switch ($choice.ToLower()) {
        'y' { gh api "repos/$repo/deployments/$id" -X DELETE }
        'n' { Write-Output "Skipped deployment $id" }
        'a' { $deleteAll = $true; gh api "repos/$repo/deployments/$id" -X DELETE }
        'q' { $quit = $true; Write-Output "Skipped deployment $id (quit)" }
        default { $quit = $true; Write-Output "Skipped deployment $id (quit by default)" }
    }

    if ($LASTEXITCODE -eq 0 -and ($choice -match 'y|a')) { Write-Output "Deleted deployment $id" }
    elseif ($choice -match 'y|a') { Write-Output "Failed deployment $id" }
}
```
