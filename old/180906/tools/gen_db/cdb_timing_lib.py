#!/usr/bin/python
#

import getopt, fnmatch, string, glob
import sys
import re
import os
import subprocess
import csv
import time
import shutil
#-------------------------------------------------------------------------------
import sqlite3
import sqlite3 as lite

from xlwt import Workbook,easyxf

import   getopt, fnmatch, string, glob, subprocess
import commands

import time

import filecmp
import os.path
import shutil

import getopt, time
import ConfigParser

import json

from pprint              import *

#-------------------------------------------------------------------------------

from cdb_gen_nb_ds_lib       import *
from cdb_gen_nb_ds_ow_lib    import *

from cdb_gen_nb_us_md        import *

from cdb_gen_nb_us           import *
from cdb_gen_nb_us_ds        import *
from cdb_gen_nb_us_ds_md     import *
from cdb_gen_nb_us_ds_md_ti  import *

from cdb_load_nb_us_ds_md_ti  import *
from cdb_optim_plan_lib       import *
from cdb_optim_lib            import *


#-------------------------------------------------------------------------------
def Handle_User_Md_Ow(data, con, cur):



    data['umi_dict']= dict()
    data['User_Neighb_Ds_Md_Dict']= dict()

    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End = data['Base']['Clip_Budget_End']
    Clip_Budget_Start = data['Base']['Clip_Budget_Start']

    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    n = 0
    for umi_key in umi_keys:
        n += 1

        #umi_dict = dict()
        umi_val = data['User_Md'][umi_key]

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 




        umiow_list = data['User_Md_Owner_List'][umi_key]
        umiow_list.sort()

        now = 0
        for ID_Owner in umiow_list:
            now += 1


            umiow_list = data['User_Md_Owner_Ds_List'][umi_key][ID_Owner]
            umiow_list.sort()

            nowd = 0
            for Ds_key in umiow_list:
                nowd += 1







#-------------------------------------------------------------------------------
def Handle_User_Md_Ow_Ds_Ti_Paid(data, con, cur):

    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
    Clip_Budget_End = data['Base']['Clip_Budget_End']
    Clip_Budget_Start = data['Base']['Clip_Budget_Start']


    umi_keys = data['User_Md'].keys()
    umi_keys.sort()

    UsNeigDsMd_keys = data['P_User_Neighb_Ds_Md_Ti'].keys()
    UsNeigDsMd_keys.sort()                                 

    usdmt_keys = data['P_Neighb_Ds_Ti'].keys()
    usdmt_keys.sort()

    owner_keys = data['Owner'].keys()
    owner_keys.sort()

    n = 0
    for umi_key in umi_keys:
        n += 1
        #print n,"umi_key = ",umi_key
        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 


        Us_Md_Ow_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'].keys()
        Us_Md_Ow_Sum_keys.sort(reverse=True)


        #print "Us_Md_Ow_Sum_keys = ",Us_Md_Ow_Sum_keys

        for Us_Md_Ow_Sum in Us_Md_Ow_Sum_keys:
            ID_Owner = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Sum'][Us_Md_Ow_Sum] 
            print '   ',ID_Owner,"Us_Md_Ow_Sum = ",Us_Md_Ow_Sum

            Us_Md_Ow_Ds_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner].keys()
            Us_Md_Ow_Ds_Sum_keys.sort(reverse=True)

            for Us_Md_Ow_Ds_Sum in Us_Md_Ow_Ds_Sum_keys:
                Ds_key = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Sum'][ID_Owner][Us_Md_Ow_Ds_Sum] 

                print '      ',ID_Owner,Ds_key,"Us_Md_Ow_Ds_Sum = ",Us_Md_Ow_Ds_Sum


                Us_Md_Ow_Ds_Ti_Sum_keys = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key].keys()
                Us_Md_Ow_Ds_Ti_Sum_keys.sort(reverse=True)

                for Media_Cost_Ow_Ds_Ti in Us_Md_Ow_Ds_Ti_Sum_keys:
                    ID_Time_Interval = data['Us_Md_Ow_Ds_Ti'][umi_key]['Us_Md_Ow_Ds_Ti_Sum'][ID_Owner][Ds_key][Media_Cost_Ow_Ds_Ti] 

                    print '         ',ID_Owner,Ds_key,ID_Time_Interval,"Media_Cost_Ow_Ds_Ti = ",Media_Cost_Ow_Ds_Ti



        #-------------------------------------------
        if n >= 1:
            break   



