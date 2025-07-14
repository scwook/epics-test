TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = cls
# cls.dbd will be created and installed
DBD += cls.dbd

# cls.dbd will be made up from these files:
cls_DBD += base.dbd

# Include dbd files from all support applications:
#cls_DBD += xxx.dbd
cls_DBD += stream.dbd
cls_DBD += drvAsynIPPort.dbd
cls_DBD += asyn.dbd

# Add all the support libraries needed by this IOC
#cls_LIBS += xxx
cls_LIBS += asyn
cls_LIBS += stream

# cls_registerRecordDeviceDriver.cpp derives from cls.dbd
cls_SRCS += cls_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
cls_SRCS_DEFAULT += clsMain.cpp
cls_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#cls_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
cls_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

