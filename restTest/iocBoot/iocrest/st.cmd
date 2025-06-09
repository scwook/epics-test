#!../../bin/darwin-x86/rest

#- You may have to change rest to something else
#- everywhere it appears in this file

< envPaths

cd "${TOP}"

## Register all support components
dbLoadDatabase "dbd/rest.dbd"
rest_registerRecordDeviceDriver pdbbase

## Load record instances
dbLoadRecords("db/rest.db")

cd "${TOP}/iocBoot/${IOC}"
iocInit

## Start any sequence programs
#seq seqRest
