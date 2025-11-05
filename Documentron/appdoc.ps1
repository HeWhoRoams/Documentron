Param(
    [string]$Repo,
    [string]$Artifacts = "Generated Documentation",
    [string]$Docs = "Generated Documentation/deterministic/docs",
    [string[]]$Steps,
    [string[]]$Skip,
    [switch]$DisableDocx,
    [switch]$DisableXlsx,
    [switch]$DisableVdx
)

# Resolve script paths relative to this file's location so it works
# whether this file lives at repo root or inside the Documentron folder.
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyInModule = Join-Path $ScriptRoot "ux/cli/appdoc.py"
$pyUnderModule = Join-Path $ScriptRoot "Documentron/ux/cli/appdoc.py"

if (Test-Path $pyInModule) {
  $pyPath = $pyInModule
  $moduleDir = $ScriptRoot
}
elseif (Test-Path $pyUnderModule) {
  $pyPath = $pyUnderModule
  $moduleDir = Join-Path $ScriptRoot "Documentron"
}
else {
  Write-Error "Unable to locate appdoc.py relative to $ScriptRoot"
  exit 1
}

# Default repo root to parent of the module directory if not provided
if (-not $Repo -or $Repo -eq "") {
  $Repo = (Get-Item $moduleDir).Parent.FullName
}

# Ensure a virtual environment and required packages
# Prefer venv inside the Documentron module directory to keep repo root clean;
# fall back to an existing root-level venv if present.
$venvDirPrimary = Join-Path $ScriptRoot ".venv"
$venvDirFallback = Join-Path $Repo ".venv"
$venvPythonPrimary = Join-Path $venvDirPrimary "Scripts/python.exe"
$venvPythonFallback = Join-Path $venvDirFallback "Scripts/python.exe"

# Evaluate existence separately to avoid parser quirks on some PS versions
$hasFallback = Test-Path -LiteralPath $venvPythonFallback
$hasPrimary  = Test-Path -LiteralPath $venvPythonPrimary
if ($hasFallback -and -not $hasPrimary) {
  $venvDir = $venvDirFallback
  $venvPython = $venvPythonFallback
} else {
  $venvDir = $venvDirPrimary
  $venvPython = $venvPythonPrimary
}

function Get-PreferredPython {
  # Prefer versions with stable native wheels for lxml/python-docx
  $candidates = @('3.11','3.12','3.10')
  foreach ($v in $candidates) {
    try {
      $out = & py -$v -c "import sys; print(sys.executable)" 2>$null
      if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
    } catch {}
  }
  try {
    $out = & py -3 -c "import sys; print(sys.executable)" 2>$null
    if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
  } catch {}
  try {
    $out = & python -c "import sys; print(sys.executable)" 2>$null
    if ($LASTEXITCODE -eq 0 -and $out) { return $out.Trim() }
  } catch {}
  return $null
}

function New-VenvIfMissing {
  if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment at $venvDir" -ForegroundColor Cyan
    try {
      $basePy = Get-PreferredPython
      if (-not $basePy) {
        Write-Error "Could not locate a suitable Python (prefer 3.11/3.12). Install Python 3.11+ or set PYTHONEXECUTABLE."
        exit 1
      }
      & $basePy -m venv "$venvDir"
    } catch {
      Write-Error "Failed to create virtual environment. Ensure Python 3.11+ is installed."
      exit 1
    }
  }
}

function Ensure-Package($pyExe, [string]$moduleName, [string]$pipName) {
  & $pyExe -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('$moduleName') else 1)" *> $null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing $pipName in venv" -ForegroundColor Cyan
    & $pyExe -m pip install --upgrade pip *> $null
    & $pyExe -m pip install $pipName
    if ($LASTEXITCODE -ne 0) {
      Write-Warning "Failed to install $pipName. Conversion for that format may be skipped."
    }
  }
}

New-VenvIfMissing

if (-not (Test-Path $venvPython)) {
  Write-Error "Virtual environment python not found at $venvPython"
  exit 1
}

# Best-effort install of optional conversion dependencies
Ensure-Package $venvPython 'docx' 'python-docx'
Ensure-Package $venvPython 'openpyxl' 'openpyxl'
Ensure-Package $venvPython 'defusedxml' 'defusedxml'
Ensure-Package $venvPython 'jsonschema' 'jsonschema'

# Workaround: pin lxml < 6 for stability with CPython FT builds (3.13+/3.14t)
Write-Host "Ensuring lxml<6 for stability" -ForegroundColor Cyan
& $venvPython -m pip install "lxml<6" *> $null

# Build argument list for orchestrator and invoke using venv python
$argsList = @($pyPath, "--repo", $Repo, "--artifacts", $Artifacts, "--docs", $Docs)
if ($Steps) { $argsList += @("--steps") + $Steps }
if ($Skip)  { $argsList += @("--skip")  + $Skip }

# Ensure stable behavior on CPython FT builds (3.13+/3.14t) for native deps like lxml
$env:PYTHON_GIL = '1'

# Optional disable flags for problematic formats
if ($DisableDocx) { $env:DOCUMENTRON_DISABLE_DOCX = '1' }
if ($DisableXlsx) { $env:DOCUMENTRON_DISABLE_XLSX = '1' }
if ($DisableVdx)  { $env:DOCUMENTRON_DISABLE_VDX  = '1' }

& $venvPython $argsList
exit $LASTEXITCODE

