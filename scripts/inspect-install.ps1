[CmdletBinding()]
param(
    [string]$Install,
    [string]$ExamplesRoot,
    [string[]]$ClassName
)

$ErrorActionPreference = 'Stop'
if (-not $Install) {
    $candidates = @(Get-ChildItem -LiteralPath $env:ProgramFiles -Directory -Filter 'AnyLogic * Personal Learning Edition')
    if ($candidates.Count -ne 1) {
        throw "Found $($candidates.Count) default PLE installations. Pass -Install with the intended root."
    }
    $Install = $candidates[0].FullName
}
$Install = (Resolve-Path -LiteralPath $Install).Path
$pluginRoot = Join-Path $Install 'plugins'
if (-not $ExamplesRoot) {
    $bundled = @(Get-ChildItem -LiteralPath $pluginRoot -Directory -Filter 'com.anylogic.examples_*')
    if ($bundled.Count -eq 1) {
        $ExamplesRoot = $bundled[0].FullName
    } else {
        $ExamplesRoot = Join-Path $env:ProgramData (Split-Path -Leaf $Install)
    }
}
$engines = @(Get-ChildItem -Path "$pluginRoot/com.anylogic.engine_*/com.anylogic.engine.jar" -File)
$pedestrians = @(Get-ChildItem -Path "$pluginRoot/com.anylogic.pedestrian_library_*/lib/PedestrianLibrary.jar" -File)
if ($engines.Count -ne 1 -or $pedestrians.Count -ne 1) {
    throw "Expected one engine JAR and one Pedestrian Library JAR under $pluginRoot."
}

$apiDocs = Join-Path $engines[0].DirectoryName 'javadoc'
Write-Output "Install: $Install"
Write-Output "Engine build: $($engines[0].Directory.Name)"
Write-Output "Engine API reference: $apiDocs"
Write-Output "Pedestrian library: $($pedestrians[0].FullName)"
Write-Output "Examples root: $ExamplesRoot"
if (Test-Path -LiteralPath $ExamplesRoot) {
    $names = @(
        'PedGoTo', 'Stairs', 'Pedestrian Elevator', 'Elevator Failure',
        'Elevator Manual Control', 'Elevator Connecting Floors Defined by Different Agents',
        'Subway Entrance Hall - Phase 1'
    )
    Get-ChildItem -LiteralPath $ExamplesRoot -Recurse -File -Filter '*.alp' |
        Where-Object BaseName -In $names |
        ForEach-Object { Write-Output $_.FullName }
}

if ($ClassName) {
    $classPath = "$($engines[0].FullName);$($pedestrians[0].FullName)"
    $javap = Join-Path $Install 'jre/bin/javap.exe'
    & $javap -public -cp $classPath @ClassName
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
