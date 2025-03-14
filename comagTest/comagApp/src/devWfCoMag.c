/*************************************************************************\
* Copyright (c) 2008 UChicago Argonne LLC, as Operator of Argonne
*     National Laboratory.
* Copyright (c) 2002 The Regents of the University of California, as
*     Operator of Los Alamos National Laboratory.
* SPDX-License-Identifier: EPICS
* EPICS BASE is distributed subject to a Software License Agreement found
* in file LICENSE that is included with this distribution.
\*************************************************************************/

/*
 *      Original Authors: Bob Dalesio and Marty Kraimer
 *      Date: 6-1-90
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "alarm.h"
#include "dbDefs.h"
#include "dbAccess.h"
#include "dbEvent.h"
#include "recGbl.h"
#include "devSup.h"
#include "waveformRecord.h"
#include "epicsExport.h"

/* Create the dset for devWfSoft */
static long init_record(dbCommon *pcommon);
static long read_wf(waveformRecord *prec);
static long readCoff(waveformRecord *prec);

wfdset devWfSoft = {
    {5, NULL, NULL, init_record, NULL},
    read_wf
};
epicsExportAddress(dset, devWfSoft);

static long init_record(dbCommon *pcommon)
{
    waveformRecord *prec = (waveformRecord *)pcommon;
    long nelm = prec->nelm;
    // long status = dbLoadLinkArray(&prec->inp, prec->ftvl, prec->bptr, &nelm);
    // printf("status: %d\n", status);
    long status = 0;

    if (!status) {
        prec->nord = nelm;
        prec->udf = FALSE;
    }
    else
        prec->nord = 0;

   double *data = prec->bptr;
   data[0] = 1.234;
   data[1] = 567.1234;
   data[2] = 234234;

    printf("file: %s\n", prec->inp.value.instio.string);

    // status = readCoff(prec);

    return status;
}

static long readCoff(waveformRecord *prec) {
    double *data = prec->bptr;

    char *filepath = prec->inp.value.instio.string;
    FILE *file = fopen(filepath, "r");

    if (file == NULL) {
        printf("Error opening file %s\n", filepath);
        return 1;
    }

    char line[4096];
    const int MAX_NUMS = 410;
    double numbers[MAX_NUMS];
    int num_count = 0;
   
    while(fgets(line, sizeof(line), file) && num_count < MAX_NUMS) {
        line[strcspn(line, "\n")] = '\0';
        char *token = strtok(line,  ",");

        // char *endptr;
        while(token !=NULL) {
            numbers[num_count] = atof(token);
            // data[num_count] = atof(token);
            // printf("value: %s\n", token);
            // if(endptr != token) {
            
            // } else {
            //     printf("Conversion failed: %d\n", num_count);
            //     return 1;
            // }
            num_count += 1;
            token = strtok(NULL, ",");
        }

        printf("num: %d\n", num_count);
    }

    fclose(file);

    // printf("Numbers from CSV file:\n");
    // for (int i = 0; i < num_count; i++) {
    //     printf("%d ", numbers[i]);
    // }
    // printf("\n");
}


struct wfrt {
    long nRequest;
    epicsTimeStamp *ptime;
};

static long readLocked(struct link *pinp, void *vrt)
{
    waveformRecord *prec = (waveformRecord *) pinp->precord;
    struct wfrt *prt = (struct wfrt *) vrt;
    long status = dbGetLink(pinp, prec->ftvl, prec->bptr, 0, &prt->nRequest);

    if (!status && prt->ptime)
        dbGetTimeStamp(pinp, prt->ptime);

    return status;
}

static long read_wf(waveformRecord *prec)
{

    int num_elements = prec->nord;
    double *data = prec->bptr;

    if (data == NULL) {
        printf("Error: No data in waveform record.\n");
        return -1;
    }

    printf("Reading waveform data from record %s:\n", prec->name);
    for (int i = 0; i < num_elements; i++) {
        printf("Data[%d]: %f\n", i, data[i]);
    }

    return 0;
}

// struct
// {
//     long num;
//     DEVSUPFUN report;
//     DEVSUPFUN init;
//     DEVSUPFUN init_record;
//     DEVSUPFUN get_ioint_info;
//     DEVSUPFUN read_wf;
// } devCoMagSoft = {
//     5,
//     NULL,
//     NULL,
//     init_record,
//     NULL,
//     read_wf,
// };

// epicsExportAddress(dset, devCoMagSoft);