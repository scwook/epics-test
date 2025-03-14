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

#include <time.h>

/* Create the dset for devWfSoft */
static long init_record(dbCommon *pcommon);
static long read_wf(waveformRecord *prec);
static long readCoff(waveformRecord *prec);

wfdset devWaveformCoMagAsync = {
    {5, NULL, NULL, init_record, NULL},
    read_wf};
epicsExportAddress(dset, devWaveformCoMagAsync);

static long init_record(dbCommon *pcommon)
{
    waveformRecord *prec = (waveformRecord *)pcommon;
    long nelm = prec->nelm;

    long status = dbLoadLinkArray(&prec->inp, prec->ftvl, prec->bptr, &nelm);

    prec->nelm = 410;
    nelm = 410;

    if (!status)
    {
        prec->nord = nelm;
        prec->udf = FALSE;
    }
    else
        prec->nord = 0;

    prec->nord = 410;

    printf("file: %s\n", prec->inp.value.instio.string);
    status = readCoff(prec);

    // double *data = prec->bptr;

    return status;
}

static long readCoff(waveformRecord *prec)
{
    double *data = prec->bptr;

    char *filepath = prec->inp.value.instio.string;
    FILE *file = fopen(filepath, "r");

    if (file == NULL)
    {
        printf("Error opening file %s\n", filepath);
        return 1;
    }

    char line[4096];
    const int MAX_NUMS = 410;
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

    return 0;
}

static long read_wf(waveformRecord *prec)
{
    return 0;
}
