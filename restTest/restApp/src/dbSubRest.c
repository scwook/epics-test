#include <stdint.h>
#include <stdio.h>

#include <dbDefs.h>
#include <registryFunction.h>
#include <subRecord.h>
#include <aSubRecord.h>
#include <epicsExport.h>

#include <curl/curl.h>
#include <string.h>

static long curlSubInit(aSubRecord *prec) {
    return 0;
}

static long curlGetRequest(aSubRecord *prec) {
    char *address = (char *)prec->a;
    char *endpoint =(char *)prec->b;
    
    strcat(address, endpoint);

    CURL *curl;
    CURLcode res;
    long error = 0;

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, address);
    
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
    
        res = curl_easy_perform(curl);
    
        if(res != CURLE_OK) {
            error = -1;
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();

    return error;
}

epicsRegisterFunction(curlSubInit);
epicsRegisterFunction(curlGetRequest);
