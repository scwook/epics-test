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
#include "errlog.h"

#include <time.h>

/* Create the dset for devWfSoft */
static long init_record(dbCommon *pcommon);
static long read_wf(waveformRecord *prec);
static long readCoff(waveformRecord *prec);

static long num;

wfdset devWaveformCoMagAsync = {
    {5, NULL, NULL, init_record, NULL},
    read_wf};
epicsExportAddress(dset, devWaveformCoMagAsync);

static long init_record(dbCommon *pcommon)
{
    waveformRecord *prec = (waveformRecord *)pcommon;
    long nelm = prec->nelm;
    num = prec->nelm;

    long status = dbLoadLinkArray(&prec->inp, prec->ftvl, prec->bptr, &nelm);

    prec->nelm = num;
    nelm = num;

    if (!status)
    {
        prec->nord = nelm;
        prec->udf = FALSE;
    }
    else
        prec->nord = 0;

    prec->nord = num;

    status = readCoff(prec);

    return status;
}

static long readCoff(waveformRecord *prec)
{
    double *data = prec->bptr;

    char *filepath = prec->inp.value.instio.string;
    FILE *file = fopen(filepath, "r");

    if (file == NULL)
    {
        epicsPrintf("\033[31mError: Can not found file %s \033[0m\n", filepath);

        return 1;
    }

    char line[4096];
    const int MAX_NUMS = num;
    double numbers[MAX_NUMS];
    int num_count = 0;

    while (fgets(line, sizeof(line), file) && num_count < MAX_NUMS)
    {
        line[strcspn(line, "\n")] = '\0';
        char *token = strtok(line, ",");

        // char *endptr;
        while (token != NULL)
        {
            numbers[num_count] = atof(token);
            data[num_count] = atof(token);
            // printf("value: %s\n", token);
            // if(endptr != token) {

            // } else {
            //     printf("Conversion failed: %d\n", num_count);
            //     return 1;
            // }
            num_count += 1;
            token = strtok(NULL, ",");
        }
    }

    fclose(file);

    if(num_count != num) {
        epicsPrintf("\33[33mWarning: The set value(%d) does not match the actual value(%d)\33[0m\n", num, num_count);
    }

    return 0;
}

static long read_wf(waveformRecord *prec)
{
    printf("Pact: %d\n", prec->pact);
//    readCoff(prec);
    return 0;
}
