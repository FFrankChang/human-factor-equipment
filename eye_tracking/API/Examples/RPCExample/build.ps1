#
# Calls CMake to configure and build RPCExample
#

param(
    [string]$Config = "Release",
    [string]$Generator = "Visual Studio 16 2019"
)

$BuildDirName = "build"
$SourceDirName = "RPCExample"
$BuildDir = [io.path]::combine($PSScriptRoot, $BuildDirName)
$SourceDir = [io.path]::combine($PSScriptRoot, $SourceDirName)

New-Item -Force -ItemType Directory -Path "$BuildDir"
Push-Location "$BuildDir"
cmake -G "$Generator" -A "x64" "$SourceDir"
Pop-Location

if ($?) {
    cmake --build "$BuildDir" --config "$Config"
}
