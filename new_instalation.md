
Install scoop
Set-ExecutionPolicy RemoteSigned -scope CurrentUser
iwr -useb get.scoop.sh | iex




As administrator
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux

Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform

wsl --install

Invoke-WebRequest -Uri https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi -OutFile wsl_update_x64.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I wsl_update_x64.msi /quiet /norestart'

wsl --set-default-version 2
wsl --install -d Ubuntu-24.04
