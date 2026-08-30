param(
    [int]$MinCoverage = 80
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' not found on PATH. Please install JDK 17 (javac/java) and ensure it's on PATH."
    }
}

Ensure-Command 'java'
Ensure-Command 'javac'
Ensure-Command 'curl'

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent

$DepsDir = Join-Path $Root '.deps'
$BuildDir = Join-Path $Root '.build'
$MainOut = Join-Path $BuildDir 'classes'
$TestOut = Join-Path $BuildDir 'test-classes'
$ReportDir = Join-Path $BuildDir 'reports\jacoco'

New-Item -ItemType Directory -Force -Path $DepsDir, $MainOut, $TestOut, $ReportDir | Out-Null

# ---- Dependencies (download once) ----
$junitVersion = '1.10.2'
$jacocoVersion = '0.8.12'

$JunitJar = Join-Path $DepsDir "junit-platform-console-standalone-$junitVersion.jar"
$JacocoAgentJar = Join-Path $DepsDir "org.jacoco.agent-$jacocoVersion-runtime.jar"
$JacocoCliJar = Join-Path $DepsDir "org.jacoco.cli-$jacocoVersion-nodeps.jar"

function Download-IfMissing([string]$Url, [string]$OutFile) {
    if (Test-Path $OutFile) {
        return
    }

    Write-Host "Downloading $(Split-Path -Leaf $OutFile)..."
    curl.exe -L --fail -o $OutFile $Url
}

Download-IfMissing "https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/$junitVersion/junit-platform-console-standalone-$junitVersion.jar" $JunitJar
Download-IfMissing "https://repo1.maven.org/maven2/org/jacoco/org.jacoco.agent/$jacocoVersion/org.jacoco.agent-$jacocoVersion-runtime.jar" $JacocoAgentJar
Download-IfMissing "https://repo1.maven.org/maven2/org/jacoco/org.jacoco.cli/$jacocoVersion/org.jacoco.cli-$jacocoVersion-nodeps.jar" $JacocoCliJar

# ---- Compile ----
$MainSrcDir = Join-Path $Root 'src'
$TestSrcDir = Join-Path $Root 'src\test\java'

# Force array semantics even when only one file is found (important under StrictMode).
$MainSources = @(
    Get-ChildItem -Path $MainSrcDir -Recurse -Filter *.java |
        Where-Object { $_.FullName -notmatch '\\src\\test\\' } |
        ForEach-Object { $_.FullName }
)

$TestSources = @(
    if (Test-Path $TestSrcDir) {
        Get-ChildItem -Path $TestSrcDir -Recurse -Filter *.java | ForEach-Object { $_.FullName }
    }
)

if ($MainSources.Count -eq 0) {
    throw "No main Java sources found under $MainSrcDir"
}
if ($TestSources.Count -eq 0) {
    throw "No test Java sources found under $TestSrcDir"
}

Write-Host "Compiling main sources ($($MainSources.Count))..."
& javac -encoding UTF-8 -d $MainOut @MainSources

Write-Host "Compiling test sources ($($TestSources.Count))..."
$TestClasspath = "$MainOut;$JunitJar"
& javac -encoding UTF-8 -d $TestOut -classpath $TestClasspath @TestSources

# ---- Run tests with JaCoCo agent ----
$JacocoExec = Join-Path $BuildDir 'jacoco.exec'

Write-Host "Running tests..."
& java "-javaagent:$JacocoAgentJar=destfile=$JacocoExec" -jar $JunitJar `
    --class-path "$MainOut;$TestOut" `
    --scan-class-path

# ---- JaCoCo report ----
$HtmlDir = Join-Path $ReportDir 'html'
$XmlReport = Join-Path $ReportDir 'jacoco.xml'

New-Item -ItemType Directory -Force -Path $HtmlDir | Out-Null

Write-Host "Generating JaCoCo report..."
& java -jar $JacocoCliJar report $JacocoExec `
    --classfiles $MainOut `
    --sourcefiles $MainSrcDir `
    --html $HtmlDir `
    --xml $XmlReport | Out-Null

# ---- Parse coverage from XML (INSTRUCTION counter) ----
[xml]$jacocoXml = Get-Content -Raw -Path $XmlReport

# Note: the XML document element is <report>, so use XPath instead of $jacocoXml.report
$instrCounter = $jacocoXml.SelectSingleNode('/report/counter[@type="INSTRUCTION"]')
if (-not $instrCounter) {
    throw "Failed to find INSTRUCTION counter in JaCoCo XML report at $XmlReport"
}

$missed = [double]$instrCounter.GetAttribute('missed')
$covered = [double]$instrCounter.GetAttribute('covered')
$total = $missed + $covered
if ($total -le 0) {
    throw 'JaCoCo reported zero instructions. Did compilation succeed?'
}

$coveragePct = [Math]::Round(($covered / $total) * 100.0, 2)
Write-Host "Instruction coverage: $coveragePct% (covered=$covered missed=$missed)"
Write-Host "HTML report: $HtmlDir"

if ($coveragePct -lt $MinCoverage) {
    Write-Error "Coverage $coveragePct% is below required minimum $MinCoverage%"
    exit 1
}

Write-Host "OK - coverage meets threshold ($MinCoverage%)."
