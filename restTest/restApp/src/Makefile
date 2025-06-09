TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================
#USR_INCLUDES += /usr/include/x86_64-linux-gnu
USR_LDFLAGS += -lcurl

#=============================
# Build the IOC application
PROD_IOC = rest

# rest.dbd will be created and installed
DBD += rest.dbd

USR_SRCS += dbSubRest.c

# rest.dbd will be made up from these files:
rest_DBD += base.dbd

# Include dbd files from all support applications:
#rest_DBD += xxx.dbd
rest_DBD += dbSubRest.dbd

# Add all the support libraries needed by this IOC
#rest_LIBS += xxx

# rest_registerRecordDeviceDriver.cpp derives from rest.dbd
rest_SRCS += rest_registerRecordDeviceDriver.cpp

# Build the main IOC entry point on workstation OSs.
rest_SRCS_DEFAULT += restMain.cpp
rest_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#rest_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
rest_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

