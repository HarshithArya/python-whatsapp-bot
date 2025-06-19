@echo off
echo Starting WhatsApp Bot with Flask and ngrok...
echo.
echo Starting Flask app in new window...
start "Flask WhatsApp Bot" cmd /k "C:\Users\harsh\AppData\Local\Programs\Python\Python313\python.exe run.py"
echo.
echo Starting ngrok tunnel in new window...
start "ngrok Tunnel" cmd /k ""C:\Users\harsh\Downloads\Compressed\ngrok-v3-stable-windows-amd64\ngrok.exe" http 8000 --domain suitably-possible-ringtail.ngrok-free.app"
echo.
echo Both services are starting in separate windows.
echo Keep both windows open for the bot to work.
pause 