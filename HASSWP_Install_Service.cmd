@echo off
echo [Extract the HASSWP ZIP contents to C:\HassWP]
schtasks.exe /create /TN HASSWP /XML C:\HassWP\HASSWP.xml
schtasks.exe /run /TN HASSWP 
schtasks.exe /TN HASSWP

pause