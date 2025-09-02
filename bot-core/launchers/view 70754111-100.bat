@echo off

set t=%~n0






TITLE %t% 

cd C:\Users\Administrator\Desktop\ngodingmuluViewSP
:repeat
Set NODE_OPTIONS="--max-old-space-size=8192"
node generatex_4c.js %t% x

goto :repeat
pause


