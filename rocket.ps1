param (
    [string] $url,
    [int] $numRequests,
    [string] $method = 'GET',
    [hashtable] $headers = @{}
)

if (-not $url -or -not $numRequests) {
    Write-Host "Usage: rocket.ps1 -url <URL> -numRequests <numRequests>"
    exit 1
}

$startTime = Get-Date

# Send the specified number of HTTP requests in parallel
for ($i = 1; $i -le $numRequests; $i++) {
    Invoke-RestMethod -Uri $url
}

$endTime = Get-Date
$totalTime = ($endTime - $startTime).TotalMilliseconds

Write-Host "Total time for $numRequests requests: $totalTime ms"
Write-Host "Average response time: $(($totalTime / $numRequests)) ms"
