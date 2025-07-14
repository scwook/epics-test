#!../../bin/darwin-x86/cls

#- You may have to change cls to something else
#- everywhere it appears in this file

< envPaths

epicsEnvSet "STREAM_PROTOCOL_PATH" "../../proto"

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/cls.dbd"
cls_registerRecordDeviceDriver pdbbase

drvAsynIPPortConfigure("CLS-DAQ", "10.1.100.253:9009", 0, 0, 0)

## Load record instances
dbLoadRecords("db/clsDaq.db","PORT=CLS-DAQ")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=scwook"
