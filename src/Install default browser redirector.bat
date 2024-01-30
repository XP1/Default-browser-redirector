@echo on

regedit /s "Default browser redirector.reg"

mkdir "%AppData%\Default browser redirector"
copy "default_browser_redirector.pyw" "%AppData%\Default browser redirector"
copy "browser_rules.json" "%AppData%\Default browser redirector"

pause