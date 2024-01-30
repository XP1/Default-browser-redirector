import os
import subprocess
subprocess.Popen(["pyw", os.path.expandvars("%%AppData%%\Default browser redirector\default_browser_redirector.pyw"), "%1"], creationflags=subprocess.CREATE_NO_WINDOW)