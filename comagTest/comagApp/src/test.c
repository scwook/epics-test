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

wfdset devWfSoft = {
    {5, NULL, NULL, init_record, NULL},
    read_wf};
epicsExportAddress(dset, devWfSoft);

static long init_record(dbCommon *pcommon)
{
    waveformRecord *prec = (waveformRecord *)pcommon;
    long nelm = prec->nelm;
    printf("nelm: %d\n", nelm);

    long status = dbLoadLinkArray(&prec->inp, prec->ftvl, prec->bptr, &nelm);
    // long status = 1;
    printf("nelm: %d\n", nelm);
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

    printf("nord: %d\n", prec->nord);

    // srand(time(NULL));

    // 랜덤 값 생성
    // int random_value = rand();
    // printf("Random value: %d\n", random_value);

    // // 특정 범위 내의 랜덤 값 생성 (예: 0에서 99 사이)
    // int min = 0;
    // int max = 99;
    // int random_value_in_range = (rand() % (max - min + 1)) + min;

    // double *data = prec->bptr;
    // data[0] = random_value_in_range;
    // data[1] = random_value_in_range + 10;
    // data[2] = random_value_in_range + 20;
    // data[3] = random_value_in_range + 30;
    // data[4] = random_value_in_range + 40;
    // data[5] = random_value_in_range + 50;

    // prec->inp.value.instio.string = "coff2.csv";
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
// struct wfrt {
//     long nRequest;
//     epicsTimeStamp *ptime;
// };

// static long readLocked(struct link *pinp, void *vrt)
// {
//     waveformRecord *prec = (waveformRecord *) pinp->precord;
//     struct wfrt *prt = (struct wfrt *) vrt;
//     long status = dbGetLink(pinp, prec->ftvl, prec->bptr, 0, &prt->nRequest);

//     if (!status && prt->ptime)
//         dbGetTimeStamp(pinp, prt->ptime);

//     return status;
// }

static long read_wf(waveformRecord *prec)
{
    return 0;
}
