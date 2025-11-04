Param(
    [string]$Repo = ".",
    [string]$Artifacts = "Documentron/artifacts",
    [string]$Docs = "Documentron/docs",
    [string[]]$Steps,
    [string[]]$Skip
)

$argsList = @("Documentron/ux/cli/appdoc.py", "--repo", $Repo, "--artifacts", $Artifacts, "--docs", $Docs)
if ($Steps) { $argsList += @("--steps") + $Steps }
if ($Skip)  { $argsList += @("--skip")  + $Skip }

if ($env:PYTHONEXECUTABLE) {
    & $env:PYTHONEXECUTABLE $argsList
    exit $LASTEXITCODE
} else {
    python $argsList
    exit $LASTEXITCODE
}
