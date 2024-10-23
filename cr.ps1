$set = $args[0]
$problem = $args[1]
$debug = $args[2]

$solpath = "./solutions/$set/$problem.rs"
$outputpath = "./output/$set/$problem.exe"

if ($debug -eq 1) {
    Write-Output "Set: $set, problem: $problem"
    Write-Output "Solutions path = $solpath"
    Write-Output "Output path = $outputpath"
}

rustc $solpath --out-dir output/$set/

if ($debug -eq 1) {
    Write-Output "Finished compiling, executing..`r`n"
}

Invoke-Expression $outputpath