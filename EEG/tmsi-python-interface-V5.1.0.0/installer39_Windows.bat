call py -3.9 --version
if %errorlevel% neq 0 exit /b %errorlevel%
call py -3.9 -m venv .venv
call .\.venv\Scripts\activate
pip install -r .\requirements39_Windows.txt
echo --------------------------------------
echo installation successfully completed
echo --------------------------------------
echo installation successfully completed
pause >nul