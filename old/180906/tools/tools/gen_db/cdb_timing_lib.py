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
def Handle_User_Md(data, con, cur):



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
        #umi_dict[umi_val] = dict()
        data['umi_dict'][umi_val] = dict()
        #User_Neighb_Ds_Md_Dict = dict()

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 

        uu = 0
        for undm_key in data['User_Md_Ds_List'][umi_key]:
            uu += 1

            UsNeigDsMd_ID_User            ,\
            UsNeigDsMd_ID_User_Media      ,\
            ID_Country                    ,\
            ID_City                       ,\
            ID_Neighborhoods              ,\
            ID_Digital_Signage            ,\
            ID_Owner                      = Unpack_User_Neighb_Ds_Md_Key(undm_key) 

            undm_val = data['P_User_Neighb_Ds_Md_Ti'][undm_key]
            print uu,undm_key,"=>",undm_val

            undm_ID_User              ,\
            undm_ID_User_Media        ,\
            undm_ID_Country           ,\
            undm_ID_City              ,\
            undm_ID_Neighborhoods     ,\
            undm_ID_Digital_Signage   ,\
            undm_ID_Owner             ,\
            Neighborhood              ,\
            Nic_User                  ,\
            Dig_Sign                  ,\
            Owner_Name                ,\
            Media_Name                ,\
            Media_Cost                ,\
            Media_Slots               ,\
            Media_Total_Slots         ,\
            DS_Cost                   ,\
            DS_Perc_Quality           ,\
            UM_DS_COST                ,\
            DS_Cost_Perc              ,\
            DS_Media_Cost             ,\
            DS_Media_Total_Slots = Unpack_User_Nb__Ds_Md_List(undm_val)

            data['User_Neighb_Ds_Md_Dict'][undm_key] = DS_Media_Cost

            iID_Time_Interval = 0

            for iID_Time_Interval in xrange(1, Time_Interval_Counter + 1):

                ID_Time_Interval = str(iID_Time_Interval)

                usdmt_key = Create_Usdmt_Key(\
                    ID_Country,
                    ID_City,
                    ID_Neighborhoods,
                    ID_Digital_Signage,
                    ID_Time_Interval)

                usdmt_val      = data['P_Neighb_Ds_Ti'][usdmt_key]

                ID_Country         ,\
                ID_City            ,\
                ID_Neighborhoods   ,\
                ID_Digital_Signage ,\
                ID_Owner           ,\
                ID_Time_Interval   ,\
                Neighborhood       ,\
                Dig_Sign           ,\
                Owner_Name         ,\
                DS_Cost            ,\
                DS_Perc_Quality    ,\
                TI_Price           ,\
                TI_D_Sign_People   ,\
                DS_TI_Price        ,\
                TI_Slots           ,\
                TI_Slots_Busy      ,\
                TI_Slots_Free      ,\
                TI_List_Prices     = Unpack_Neighb_Ds_Ti_Key(usdmt_val)

                TI_Prices_list = TI_List_Prices.split(';')

                #print "---------------------------------------------"
                ##print "Neighborhood = ",Neighborhood
                ##print "umi_key = ",umi_key
                #print "umi_val = ",umi_val
                #print "undm_val = ",undm_val
                #print "ID_Digital_Signage = ",ID_Digital_Signage
                #print "Dig_Sign = ",Dig_Sign
                #print "ID_Time_Interval = ",ID_Time_Interval
                #print "TI_Slots = ",TI_Slots
                #print "TI_Slots_Busy = ",TI_Slots_Busy
                #print "DS_TI_Price = ",DS_TI_Price
                #print "TI_D_Sign_People = ",TI_D_Sign_People
                #print "---------------------------------------------"

                i = 0
                for tp in TI_Prices_list:
                    i += 1

                    if tp == '':
                        continue
                    tpk = int(TI_Slots)-i
                    #print tpk,tp

                    if int(TI_Slots_Busy) > tpk:
                        continue

                    #people_price = round(float(TI_D_Sign_People)/float(tp),3)
                    people_price = round(float(tp),3)

                    if people_price < Min_4_Piople_Price :
                        continue

                    umip_val = Create_Umip_Val(str(tpk),\
                        ID_Time_Interval,\
                        DS_TI_Price,\
                        TI_D_Sign_People,\
                        Dig_Sign,\
                        Owner_Name,\
                        UsNeigDsMd_ID_User,\
                        UsNeigDsMd_ID_User_Media,\
                        ID_Country,\
                        ID_City,\
                        ID_Neighborhoods,\
                        ID_Digital_Signage,\
                        ID_Owner)

                    if not data['umi_dict'][umi_val].has_key(people_price):
                        data['umi_dict'][umi_val][people_price]=list()

                    if not umip_val in data['umi_dict'][umi_val][people_price]:
                        data['umi_dict'][umi_val][people_price].append(umip_val)
                        #print i,tpk,people_price,'+++',umip_val

            ### break
        print '============================================='

        print 'Media_Cost=',Media_Cost
        print 'Clip_Budget_Start=',Clip_Budget_Start
        print 'Clip_Budget_End=',Clip_Budget_End
        tik_keys = data['umi_dict'][umi_val].keys()
        tik_keys.sort(reverse=True)

        tMedia_Cost =  float(Media_Cost)
        tPeople =  0
        flag_break = 0


        ##print "data[umi_dict] = "
        ##pprint (data['umi_dict'])
        ##
        ##print 'tik_keys=',tik_keys

        print '============================================='
        for ti in tik_keys:
            umi_dct_list = data['umi_dict'][umi_val][ti]
            #print ti,'=>',data['umi_dict'][umi_val][ti]

            fti = float(ti)

            if Clip_Budget_Start < fti:
                continue

            print fti,'=>'

            for udl in umi_dct_list:

                tpk               ,\
                ID_Time_Interval  ,\
                DS_TI_Price       ,\
                TI_D_Sign_People  ,\
                Dig_Sign          ,\
                Owner_Name        ,\
                ID_User           ,\
                ID_User_Media     ,\
                ID_Country        ,\
                ID_City           ,\
                ID_Neighborhoods  ,\
                ID_Digital_Signage,\
                ID_Owner          = Unpack_Udl_List(udl) 

                usdm_key = Create_Usdm_Key(\
                    ID_User      ,
                    ID_User_Media,
                    ID_Country,
                    ID_City,
                    ID_Neighborhoods,
                    ID_Digital_Signage,
                    ID_Owner)

                undm_val = data['P_User_Neighb_Ds_Md_Ti'][undm_key]

                ID_User              ,\
                ID_User_Media        ,\
                ID_Country           ,\
                ID_City              ,\
                ID_Neighborhoods     ,\
                ID_Digital_Signage   ,\
                ID_Owner             ,\
                Neighborhood         ,\
                Nic_User             ,\
                Dig_Sign             ,\
                Owner_Name           ,\
                Media_Name           ,\
                Media_Cost           ,\
                Media_Slots          ,\
                Media_Total_Slots    ,\
                DS_Cost              ,\
                DS_Perc_Quality      ,\
                UM_DS_COST           ,\
                DS_Cost_Perc         ,\
                DS_Media_Cost        ,\
                DS_Media_Total_Slots = Unpack_User_Nb__Ds_Md_List(undm_val)


                #tPrice =  fti   * float(TI_D_Sign_People)
                tPrice =  fti
                tMedia_Cost   -=  float(tPrice)
                #tPeople       +=  float(tPrice)*float(TI_D_Sign_People)
                tPeople       +=  float(tPrice)


                if Clip_Budget_End >= tMedia_Cost:
                    flag_break = 1
                    break

                #print '   ',udl
                print '   ',\
                    ID_Neighborhoods,\
                    ID_Digital_Signage,\
                    ID_Time_Interval,\
                    tpk,\
                    'tMedia_Cost:',tPrice,'=>',tMedia_Cost,tPeople,DS_Media_Cost

                #if Clip_Budget_End >= float(Media_Cost) - tMedia_Cost:


            if flag_break == 1:
                break

        print '============================================='
        print 'Delta_Media_Cost=', float(Media_Cost) - tMedia_Cost
        print 'len(tik_keys)=',len(tik_keys)


        if n >= 1:
            break      

