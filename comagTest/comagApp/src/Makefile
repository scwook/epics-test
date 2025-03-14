TOP=../..

include $(TOP)/configure/CONFIG
#----------------------------------------
#  ADD MACRO DEFINITIONS AFTER THIS LINE
#=============================

#=============================
# Build the IOC application

PROD_IOC = comag
# comag.dbd will be created and installed
DBD += comag.dbd

# comag.dbd will be made up from these files:
comag_DBD += base.dbd

# Include dbd files from all support applications:
#comag_DBD += xxx.dbd
comag_DBD += devCoMag.dbd
# comag_DBD += devWfCoMag.dbd
# comag_DBD += test.dbd

# Add all the support libraries needed by this IOC
#comag_LIBS += xxx

# comag_registerRecordDeviceDriver.cpp derives from comag.dbd
comag_SRCS += comag_registerRecordDeviceDriver.cpp
comag_SRCS += devCoMag.c
# comag_SRCS += devWfCoMag.c
# comag_SRCS += test.c

# Build the main IOC entry point on workstation OSs.
comag_SRCS_DEFAULT += comagMain.cpp
comag_SRCS_vxWorks += -nil-

# Add support from base/src/vxWorks if needed
#comag_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary

# Finally link to the EPICS Base libraries
comag_LIBS += $(EPICS_BASE_IOC_LIBS)

#===========================

include $(TOP)/configure/RULES
#----------------------------------------
#  ADD RULES AFTER THIS LINE

