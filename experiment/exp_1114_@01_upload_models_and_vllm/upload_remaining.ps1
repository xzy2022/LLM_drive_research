$models = @(
    "DeepSeek-R1-Distill-Qwen-7B",
    "Qwen2.5-Coder-7B-Instruct",
    "Qwen3.5-4B",
    "Qwen3.5-9B",
    "Qwen2.5-Coder-14B-Instruct"
)

$remoteBase = "xxx:/data/xxx/models/"
$logFile = "experiment/exp_1114_@01_upload_models_and_vllm/logs/upload.log"

foreach ($m in $models) {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$time] Starting upload: $m"
    Write-Output "[$time] Starting upload: $m"
    
    $src = "E:\models\$m"
    scp -r $src $remoteBase
    
    $finishTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logFile -Value "[$finishTime] Finished upload: $m"
    Write-Output "[$finishTime] Finished upload: $m"
}

$allDoneTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "[$allDoneTime] All uploads completed."
Write-Output "[$allDoneTime] All uploads completed."
