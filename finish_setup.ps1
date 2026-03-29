# Wait until Ollama executable exists in default installation path
$ollamaPath = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"

Write-Host "Waiting for OllamaSetup.exe to finish installing..."
while (-not (Test-Path $ollamaPath)) {
    Start-Sleep -Seconds 10
}

Write-Host "Ollama installed! Starting background service..."
Start-Process -FilePath $ollamaPath -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep -Seconds 10

Write-Host "Starting the massive 4.7 GB Llama3 download..."
& $ollamaPath run llama3 "Hello, you are now completely installed and ready."

# Send a Windows Toast Notification when complete
$Title = "Setup Complete!"
$Msg = "The 5GB AI Engine has successfully finished downloading! Your app is 100% ready to use."

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
$XmlString = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">$Title</text>
            <text id="2">$Msg</text>
        </binding>
    </visual>
</toast>
"@

$XmlDocument = New-Object Windows.Data.Xml.Dom.XmlDocument
$XmlDocument.LoadXml($XmlString)
$ToastNotification = [Windows.UI.Notifications.ToastNotification]::new($XmlDocument)
$ToastNotifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("AI Document Setup")
$ToastNotifier.Show($ToastNotification)

Write-Host "ALL DONE!"
