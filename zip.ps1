$rootDir = Read-Host -Prompt "Enter the directory path you want to search"
$env:TMPDIR = "."

if (-not $rootDir) {
    Write-Error "Provided directory is null or empty."
    return
}

if (-not (Test-Path $rootDir -PathType Container)) {
    Write-Error "Directory $rootDir does not exist."
    return
}

$patterns = @(
    'password\s*=\s*[^;\n]{1,100}', 
    'api_key\s*=\s*[^;\n]{1,100}',
    'secret\s*=\s*[^;\n]{1,100}',
    '(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])',
    '-----BEGIN [A-Z ]*PRIVATE KEY-----',
    '[a-f0-9]{32}',   
    '[a-f0-9]{64}'    
)

$alreadyMatched = @{}

function Search-Files {
    param (
        [Parameter(Mandatory=$true)]
        [string]$dir
    )

    if (-not $dir) {
        Write-Warning "Null or empty directory passed to Search-Files."
        return
    }

    Get-ChildItem -Path $dir -File | ForEach-Object {
        $filePath = $_.FullName

        # If the file is a zip archive, extract and search within
        if ($_.Extension -eq ".zip") {
            $tempDir = Join-Path $env:TMPDIR (New-Guid)
            Expand-Archive -Path $filePath -DestinationPath $tempDir
            Search-Files -dir $tempDir
            Remove-Item -Path $tempDir -Recurse -Force
        }
        else {
            $patterns | ForEach-Object {
                $pattern = $_

                # Check if the pattern exists in the file
                $matches = Select-String -Path $filePath -Pattern $pattern -ErrorAction SilentlyContinue
                if ($matches) {
                    $matches | ForEach-Object {
                        $matchedWord = $_.Matches[0].Value

                        if (-not $alreadyMatched.ContainsKey("$pattern-$matchedWord")) {
                            $alreadyMatched["$pattern-$matchedWord"] = $true

                            $startIndexBefore = [math]::Max(0, $_.Matches[0].Index - 50)
                            $lengthBefore = $_.Matches[0].Index - $startIndexBefore
                            $lineBefore = $_.Line.Substring($startIndexBefore, $lengthBefore)

                            $remainingLength = $_.Line.Length - ($_.Matches[0].Index + $_.Matches[0].Length)
                            $charsAfterMatch = [math]::Min(50, $remainingLength)
                            $lineAfter = $_.Line.Substring($_.Matches[0].Index + $_.Matches[0].Length, $charsAfterMatch)

                            Write-Host "File: $filePath, Line: $($_.LineNumber), Match:" -NoNewline
                            Write-Host " $lineBefore" -NoNewline
                            Write-Host "$matchedWord" -NoNewline -ForegroundColor Red
                            Write-Host "$lineAfter"
                        }
                    }
                }
            }
        }
    }

    # Recurse into directories
    Get-ChildItem -Path $dir -Directory | ForEach-Object {
        Search-Files -dir $_.FullName
    }
}

# Start the search process
Search-Files -dir $rootDir

