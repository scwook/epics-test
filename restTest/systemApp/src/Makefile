TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = system
# system.dbd will be created and installed
DBD += system.dbd

# system.dbd will be made up from these files:
system_DBD += base.dbd

# Include dbd files from all support applications:
#system_DBD += xxx.dbd
system_DBD += dbSubSystem.dbd

# Add all the support libraries needed by this IOC
#system_LIBS += xxx

# system_registerRecordDeviceDriver.cpp derives from system.dbd
system_SRCS += system_registerRecordDeviceDriver.cpp
system_SRCS += dbSubSystem.c

# Build the main IOC entry point on workstation OSs.
system_SRCS_DEFAULT += systemMain.cpp
system_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#system_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
system_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

