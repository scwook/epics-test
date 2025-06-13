#!../../bin/darwin-x86/system

#- You may have to change system to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/system.dbd"
system_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadRecords("db/rest.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=scwook"
