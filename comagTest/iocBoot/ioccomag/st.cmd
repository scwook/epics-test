#!../../bin/darwin-x86/comag

#- You may have to change comag to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/comag.dbd"
comag_registerRecordDeviceDriver pdbbase

## Load record instances
#dbLoadRecords("db/comag.db","user=scwook")
dbLoadRecords("db/test.db")
#dbLoadTemplate("db/test.template")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq sncxxx,"user=scwook"
