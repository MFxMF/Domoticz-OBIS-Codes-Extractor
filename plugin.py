#!/usr/bin/env python
"""
OBIS Codes Extractor
Author: MFxMF 2019
Requirements: 
    1.python module telnetlib3 
        (pi@raspberrypi:~$ sudo pip3 install telnetlib3)
    2.Communication module RS485 to LAN converter module -> https://www.usriot.com/products/modbus-serial-to-ethernet-converters.html
"""
"""
<plugin key="OBISEXTACTOR" name="Obis CODES EXTRACTOR" version="1.0.0" author="MFxMF">
    <params>
        <param field="Address" label="IP" width="200px" required="true" default="192.168.1.1" />
        <param field="Port" label="Port" width="200px" required="true" default="26" />
        <param field="Mode1" label="Initalize Code" width="40px" required="true" default="/?!"  />
        <param field="Mode2" label="Verbose" width="75px">
            <options>
                <option label="Yes" value="Yes"/>
                <option label="No" value="No"  default="No" />
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import telnetlib
import re
class BasePlugin:
    def __init__(self):
        return

    def onStart(self):
        obisRaw=None
        Domoticz.Log("Obis Code Extractor plugin start")
        try:
            tn=telnetlib.Telnet(Parameters["Address"],Parameters["Port"],5)
            tn.write(Parameters["Mode1"].encode('ascii')+b"\x0D\x0A")
            obisRaw=tn.read_until(b"!",50)
            tn.close()  
            obisRaw=obisRaw.decode("utf-8", errors="ignore")
            obisRawList = []
            buff = []
            for c in obisRaw:
                if c == '\r':
                    continue
                if c == '\n':
            
                    obisRawList.append(''.join(buff))
                    buff = []
                else:
                    buff.append(c)
            else:
                if buff:
                   obisRawList.append(''.join(buff))
            obisCodes=[]
            for ln in obisRawList:
                if re.match(r"(^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])-([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]):([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])).([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])).([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])))",ln):
                    st=ln.split("(")[0];
                    obisCodes.append(st)
            
            devID=0
            for devID in range(len(obisCodes)): 
                if devID+1 not in Devices:
                    Domoticz.Device(Name=obisCodes[devID], Unit=devID+1,TypeName="Text", Used=0).Create()

        except:
            Domoticz.Log("Connection Problem - Processing Aborted")
    def onStop(self):
        Domoticz.Log("Obis Code Extractor plugin stop")

    def onHeartbeat(self):
        Domoticz.Log("Obis Code Extractor running")
        obisRaw=None
        try:
            tn=telnetlib.Telnet(Parameters["Address"],Parameters["Port"],5)
            tn.write(Parameters["Mode1"].encode('ascii')+b"\x0D\x0A")
            obisRaw=tn.read_until(b"!",50)
            tn.close()  
            obisRaw=obisRaw.decode("utf-8", errors="ignore")
            obisRawList = []
            buff = []
            for c in obisRaw:
                if c == '\r':
                    continue
                if c == '\n':
                    obisRawList.append(''.join(buff))
                    buff = []
                else:
                    buff.append(c)
            else:
                if buff:
                   obisRawList.append(''.join(buff))
            obisCodes=[]
            for ln in obisRawList:
                if re.match(r"(^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])-([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]):([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])).([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])).([A-Z]|([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])))",ln):
                    st=ln.split("(")[0];
                    obisCodes.append(st)
            devID=1 
            for obis in obisCodes:
                if devID not in Devices:
                    Domoticz.Device(Name=obisCodes[devID-1], Unit=devID,TypeName="Text", Used=0).Create()
                for ln in obisRawList:
                    if ln.startswith(obis+"("):
                        st=ln[ln.find("(")+1:ln.find(")")].split("*")[0];
                        Devices[devID].Update(0,str(st))
                devID=devID+1
            if Parameters["Mode2"] == "Yes":
                Domoticz.Log("Raw OBIS Data\n")
                Domoticz.Log(obisRaw)
        except:
            Domoticz.Log("Connection Problem - Processing Aborted")

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug("'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

