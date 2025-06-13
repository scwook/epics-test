#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include <dbDefs.h>
#include <registryFunction.h>
#include <subRecord.h>
#include <aSubRecord.h>
#include <epicsExport.h>

#include <string.h>

static long curlSubInit(aSubRecord *prec) {
    return 0;
}

static long curlGetRequest(aSubRecord *prec) {
    char *address = (char *)prec->a;
    char *endpoint =(char *)prec->b;
    char curl[100] = "curl ";
        
    strcat(curl, address);
    strcat(curl, endpoint);

    //printf("%s\n", curl);
    int result;
    result = system(curl);

    return 0;
}

epicsRegisterFunction(curlSubInit);
epicsRegisterFunction(curlGetRequest);
