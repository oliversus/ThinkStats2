"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

import numpy as np
import sys

import nsfg
import thinkstats2

def ReadFemResp2(dct_file, dat_file):
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip')
    return df

def Validate(resp):
    #print(resp.pregnum.value_counts().sort_index())
    preg = nsfg.ReadFemPreg()
    preg_count = nsfg.MakePregMap(preg)
    for index, pregnum in resp.pregnum.iteritems():
        caseid = resp.caseid[index]
        indices = preg_count[caseid]
        #print(caseid, indices, pregnum)
        if len(indices) != pregnum:
            print("Mismatch in pregnancy and respondent tables - exiting.")
            return False
    return True

def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    resp = ReadFemResp2("2002FemResp.dct", "2002FemResp.dat.gz")
    assert(Validate(resp))

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
