param(
    [string]$ToolsRoot = (Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) '..\.muscle-atlas'),
    [string]$BootstrapPython = 'py',
    [string]$CondaExe = 'C:\ProgramData\Anaconda3\Scripts\conda.exe',
    [switch]$OpenSim,
    [switch]$Blender
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ToolsRoot = [IO.Path]::GetFullPath($ToolsRoot)
function Invoke-Checked([string]$Exe, [string[]]$Arguments) {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Exe failed with exit $LASTEXITCODE" }
}
New-Item -ItemType Directory -Force $ToolsRoot | Out-Null
$bootstrap = Join-Path $ToolsRoot 'bootstrap'
if (-not (Test-Path "$bootstrap\Scripts\python.exe")) {
    Invoke-Checked $BootstrapPython @('-3.13','-m','venv',$bootstrap)
}
$uv = "$bootstrap\Scripts\uv.exe"
if (-not (Test-Path $uv)) {
    Invoke-Checked "$bootstrap\Scripts\python.exe" @('-m','pip','install','uv==0.13.1')
}
$venv = Join-Path $ToolsRoot 'py311'
if (-not (Test-Path "$venv\Scripts\python.exe")) {
    Invoke-Checked $uv @('venv','--python','3.11.17',$venv)
}
Invoke-Checked $uv @('pip','install','--python',"$venv\Scripts\python.exe",'-r',(Join-Path $PSScriptRoot 'requirements-win.lock.txt'))
if ($OpenSim) {
    $prefix = Join-Path $ToolsRoot 'opensim'
    if (-not (Test-Path "$prefix\conda-meta\history")) {
        Invoke-Checked $CondaExe @('create','--prefix',$prefix,'--file',(Join-Path $PSScriptRoot 'opensim-win-64.explicit.txt'),'-y')
    }
    Invoke-Checked $CondaExe @('run','-p',$prefix,'python',(Join-Path $PSScriptRoot 'opensim_smoke.py'))
}
if ($Blender) {
    $zip = Join-Path $ToolsRoot 'blender-4.5.0-windows-x64.zip'
    $base = 'https://download.blender.org/release/Blender4.5/'
    $target = Join-Path $ToolsRoot 'blender-4.5.0-windows-x64'
    if (-not (Test-Path "$target\blender.exe")) {
        if (-not (Test-Path $zip)) { Invoke-WebRequest "$base/blender-4.5.0-windows-x64.zip" -OutFile $zip }
        $manifest = (Invoke-WebRequest "$base/blender-4.5.0.sha256").Content
        $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
        if (-not ($manifest -match $hash)) { throw 'Blender checksum mismatch; preserve download for diagnosis' }
        Expand-Archive -LiteralPath $zip -DestinationPath $ToolsRoot
    }
    Invoke-Checked "$target\blender.exe" @('--background','--factory-startup','--python-expr',"import bpy; assert bpy.app.version[:2] == (4,5); print('BLENDER_SMOKE_OK')")
}
Invoke-Checked "$venv\Scripts\python.exe" @((Join-Path $PSScriptRoot 'mujoco_smoke.py'))
Write-Output "Ready: $venv ; no global PATH, proxy, driver or firewall changes."
