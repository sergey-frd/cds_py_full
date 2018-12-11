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

#-------------------------------------------------------------------------------
# 
# Get_Ti_Price(data,4,48,10)
# Get_Ti_Price(data,3,36,20)
# Get_Ti_Price(data,2,24,30)
# Get_Ti_Price(data,1,12,40)
# 
#-------------------------------------------------------------------------------
def Get_Ti_Price(\
    data,\
    ti_type,\
    base,\
    max):

    cur = 1
    ti_dict = dict()

    x = data['Base']['Dig_Sign_Max_Time_Interv_Price']
    koef_min = data['Base']['Dig_Sign_Time_Int_SQR_min']
    koef_max = data['Base']['Dig_Sign_Time_Int_SQR_max']


    koef = koef_max
    
    #koef = 0.6
    
    if ti_type == 1:
        koef = .9
    
    elif ti_type == 2:
        koef = .88
    
    elif ti_type == 3:
        koef = .86
    
    elif ti_type == 4:
        koef = .8

    steps  = max - cur
    res    = x
    result = res

    limit = max * 85/100

    nn = 0
    for i in xrange(1, steps+1):
        nn += 1
        d = max - i

        res = res ** koef

        ti_dict[i] = res + base

    return ti_dict

#-------------------------------------------------------------------------------

# Get_Price(data,4,250,48,1,10)
# Get_Price(data,3,100,36,1,20)
# Get_Price(data,2,30,24,1,30)
# Get_Price(data,1,10,12,1,40)
#-------------------------------------------------------------------------------
def Get_Price(\
    data,\
    ti_type,\
    people,\
    base,\
    cur,\
    max):


    x = data['Base']['Dig_Sign_Max_Time_Interv_Price']
    koef_min = data['Base']['Dig_Sign_Time_Int_SQR_min']
    koef_max = data['Base']['Dig_Sign_Time_Int_SQR_max']


    koef = koef_max
    
    #koef = 0.6
    
    if ti_type == 1:
        koef = .9
    
    elif ti_type == 2:
        koef = .88
    
    elif ti_type == 3:
        koef = .86
    
    elif ti_type == 4:
        koef = .8



    #if ti_type == 1:
    #    koef = .8
    #
    #elif ti_type == 2:
    #    koef = .85
    #
    #elif ti_type == 3:
    #    koef = .87
    #
    #elif ti_type == 4:
    #    koef = .89
    #

    print "---------------"
    steps  = max - cur
    res    = x
    result = res
    

    limit = max * 85/100


    print "ti_type=",ti_type
    print "koef=",koef
    print "limit=",limit

    nn = 0
    for i in xrange(1, steps+1):
        nn += 1
        d = max - i

        #if d < int(limit):
        #    koef = koef_min

            #if ti_type == 1:
            #    koef = koef_min
            #
            #elif ti_type == 2:
            #    koef = .95
            #
            #elif ti_type == 3:
            #    koef = .97
            #
            #elif ti_type == 4:
            #    koef = .99



            #print "koef=",d,koef

        #res = res ** 0.9
        #res = round(res ** koef + base)
        #res = int(res ** koef + base)
        res = res ** koef + base

        people_price = round(people/res,3)
        #people_price = int(people)
        peoples      = int(people_price * base)

        #if max - people_price > 10:
        #    res = res ** data['Base']['Dig_Sign_Time_Interv_SQR']
        #    res = res ** data['Base']['Dig_Sign_Time_Interv_SQR'] - 0.1
        #    people_price = round(people/res,3)



        if max > 100:
            if nn > 5:
                nn = 0
                print d,koef,base,max,people,round(res,3),people_price,peoples
        else:
            print d,koef,base,max,people,round(res,3),people_price,peoples

        result=int(res) + base

    #print "---------------"
    print d,koef,base,max,people,round(res,3),people_price,peoples
    #print "---------------"
    return result

#########################################################################################

def gen_nb_us_ds_md_ti_detail(\
        data,\
        con,\
        cur\
        ):

    print "-------------------"
    print         '4,250,48,1,10'
    Get_Price(data,4,250,48,1,10)


    print "-------------------"
    print         '3,100,36,1,20'
    Get_Price(data,3,100,36,1,20)


    print "-------------------"
    print         '2,30,24,1,30'
    Get_Price(data,2,30,24,1,30)


    print "-------------------"
    print         '1,10,12,1,40'
    Get_Price(data,1,10,12,1,40)

#-------------------------------------------------------------------------------
def Unpack_Ds_Val(Ds_Val):


    Dig_Sign_List   = Ds_Val.split(',')

    Dig_Sign        =     Dig_Sign_List[0]
    DS_Cost         = int(Dig_Sign_List[1])
    DS_Perc_Quality = int(Dig_Sign_List[2])

    return \
        Dig_Sign       ,      \
        DS_Cost        ,      \
        DS_Perc_Quality
        

#-------------------------------------------------------------------------------
def Unpack_User_Neighb_Ds_Md_Key(undm_key):

    undm_list          = undm_key.split(',')

    ID_User            = undm_list[0]
    ID_User_Media      = undm_list[1]
    ID_Country         = undm_list[2]
    ID_City            = undm_list[3]
    ID_Neighborhoods   = undm_list[4]
    ID_Digital_Signage = undm_list[5]
    ID_Owner           = undm_list[6]

    return \
        ID_User           ,      \
        ID_User_Media     ,      \
        ID_Country        ,      \
        ID_City           ,      \
        ID_Neighborhoods  ,      \
        ID_Digital_Signage,      \
        ID_Owner

#-------------------------------------------------------------------------------
def Unpack_User_Md_Val(umi_val):

    umi_val_list  = umi_val.split(',')

    ID_User_Media = umi_val_list[0]
    Media_Name    = umi_val_list[1]
    Media_Cost    = umi_val_list[2]
    Media_Slots   = umi_val_list[3]

    return  ID_User_Media,\
            Media_Name,      \
            Media_Cost,      \
            Media_Slots 

#-------------------------------------------------------------------------------
def Unpack_Neighb_Ds_Ti_Key(usdmt_val):

    usdmt_val_list = usdmt_val.split(',')

    ID_Country            = usdmt_val_list[0]
    ID_City               = usdmt_val_list[1]
    ID_Neighborhoods      = usdmt_val_list[2]
    ID_Digital_Signage    = usdmt_val_list[3]
    ID_Owner              = usdmt_val_list[4]
    ID_Time_Interval      = usdmt_val_list[5]
    Neighborhood          = usdmt_val_list[6]
    Dig_Sign              = usdmt_val_list[7]
    Owner_Name            = usdmt_val_list[8]
    DS_Cost               = usdmt_val_list[9]
    DS_Perc_Quality       = usdmt_val_list[10]
    TI_Price              = usdmt_val_list[11]
    TI_D_Sign_People      = usdmt_val_list[12] 
    DS_TI_Price           = usdmt_val_list[13]
    TI_Slots              = usdmt_val_list[14]
    TI_Slots_Busy         = usdmt_val_list[15]
    TI_Slots_Free         = usdmt_val_list[16]
    TI_List_Prices        = usdmt_val_list[17]  

    return \
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
        TI_List_Prices

#-------------------------------------------------------------------------------
def Unpack_User_Md_Key(umi_key):

    umi_key_list   = umi_key.split(',')

    ID_User        = umi_key_list[0]
    ID_User_Media  = umi_key_list[1]

    return ID_User,      \
           ID_User_Media  

#-------------------------------------------------------------------------------
def Unpack_Udl_List(udl):

    udl_list = udl.split(',')
    tpk                     = udl_list[0]
    ID_Time_Interval        = udl_list[1]
    DS_TI_Price             = udl_list[2]
    TI_D_Sign_People        = udl_list[3]
    Dig_Sign                = udl_list[4]
    Owner_Name              = udl_list[5]
    ID_User                 = udl_list[6]
    ID_User_Media           = udl_list[7]
    ID_Country              = udl_list[8]
    ID_City                 = udl_list[9]
    ID_Neighborhoods        = udl_list[10]
    ID_Digital_Signage      = udl_list[11]
    ID_Owner                = udl_list[12]

    return \
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
        ID_Owner


#-------------------------------------------------------------------------------
def Unpack_User_Nb__Ds_Md_List(undm_val):

    UsNeigDsMd_vl_list = undm_val.split(',')

    ID_User              = UsNeigDsMd_vl_list[0]
    ID_User_Media        = UsNeigDsMd_vl_list[1]
    ID_Country           = UsNeigDsMd_vl_list[2]
    ID_City              = UsNeigDsMd_vl_list[3]
    ID_Neighborhoods     = UsNeigDsMd_vl_list[4]
    ID_Digital_Signage   = UsNeigDsMd_vl_list[5]
    ID_Owner             = UsNeigDsMd_vl_list[6]
    Neighborhood         = UsNeigDsMd_vl_list[7]
    Nic_User             = UsNeigDsMd_vl_list[8]
    Dig_Sign             = UsNeigDsMd_vl_list[9]
    Owner_Name           = UsNeigDsMd_vl_list[10]
    Media_Name           = UsNeigDsMd_vl_list[11]
    Media_Cost           = UsNeigDsMd_vl_list[12]
    Media_Slots          = UsNeigDsMd_vl_list[13]
    Media_Total_Slots    = UsNeigDsMd_vl_list[14]
    DS_Cost              = UsNeigDsMd_vl_list[15]
    DS_Perc_Quality      = UsNeigDsMd_vl_list[16]
    UM_DS_COST           = UsNeigDsMd_vl_list[17]
    DS_Cost_Perc         = UsNeigDsMd_vl_list[18]
    DS_Media_Cost        = UsNeigDsMd_vl_list[19]
    DS_Media_Total_Slots = UsNeigDsMd_vl_list[20]


    return \
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
        DS_Media_Total_Slots 


#-----------------------------------------------------------
#----------------------------------------------------------------
#-----------------------------------------------------------
def Create_Ds_key(\
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage):

    Ds_key = \
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage

    return Ds_key
#-----------------------------------------------------------
def Create_Ow_Ds_key(\
    ID_Owner,
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage):

    Ow_Ds_key = \
        ID_Owner           +','+\
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage

    return Ow_Ds_key
#-------------------------------------------------------------------------------
def Create_Usdm_Key(\
    ID_User      ,
    ID_User_Media,
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage,
    ID_Owner):

    usdm_key = \
        ID_User            +','+\
        ID_User_Media      +','+\
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage +','+\
        ID_Owner 

    return usdm_key
#-------------------------------------------------------------------------------
def Create_Usdmt_Key(\
    ID_Country,
    ID_City,
    ID_Neighborhoods,
    ID_Digital_Signage,
    ID_Time_Interval):

    usdmt_key = \
        ID_Country         +','+\
        ID_City            +','+\
        ID_Neighborhoods   +','+\
        ID_Digital_Signage +','+\
        ID_Time_Interval 


    return usdmt_key

#-------------------------------------------------------------------------------
def Create_Umip_Val(\
    tpk                 ,
    ID_Time_Interval    ,
    DS_TI_Price         ,
    TI_D_Sign_People    ,
    Dig_Sign            ,
    Owner_Name          ,
    ID_User             ,   
    ID_User_Media       ,   
    ID_Country          ,   
    ID_City             ,   
    ID_Neighborhoods    ,   
    ID_Digital_Signage  ,   
    ID_Owner            ):

    umip_val = \
        tpk                 +','+\
        ID_Time_Interval    +','+\
        DS_TI_Price         +','+\
        TI_D_Sign_People    +','+\
        Dig_Sign            +','+\
        Owner_Name          +','+\
        ID_User             +','+\
        ID_User_Media       +','+\
        ID_Country          +','+\
        ID_City             +','+\
        ID_Neighborhoods    +','+\
        ID_Digital_Signage  +','+\
        ID_Owner          

    return umip_val


#-------------------------------------------------------------------------------
def Load_P_User_Md_Ds(data, con, cur):


    data['Owner_Money']= dict()
#    data['Owner_Ds_Money']= dict()
#    data['Owner_Ds_Ti_Money']= dict()
#
#    data['User_Md_Owner_List']= dict()
#    data['User_Md_Owner_Ds_List']= dict()
#
#    data['User_Md_Owner_Paid_List']= dict()
#    data['User_Md_Owner_Paid_Ds_List']= dict()
#    data['User_Md_Owner_Ds_TI_Paid_List']= dict()
#
#    data['User_Md_Paid']= dict()
#
#    data['User_Md_Ds_List']= dict()
#    data['User_Md_Ds_Paid']= dict()
#
#    data['User_Md_Ds_Ti_Paid_List']= dict()
#
#    Min_4_Piople_Price = float(data['Base']['Min_4_Piople_Price'])
#    Time_Interval_Counter = data['Base']['Time_Interval_Counter']
#
#    umi_keys = data['User_Md'].keys()
#    umi_keys.sort()
#
#    UsNeigDsMd_keys = data['P_User_Neighb_Ds_Md_Ti'].keys()
#    UsNeigDsMd_keys.sort()                                 
#
#    usdmt_keys = data['P_Neighb_Ds_Ti'].keys()
#    usdmt_keys.sort()
#
#    owner_keys = data['Owner'].keys()
#    owner_keys.sort()
#
#    n = 0
#    for umi_key in umi_keys:
#        n += 1
#
#        ID_User,\
#        ID_User_Media = Unpack_User_Md_Key(umi_key) 
#
#        umi_val = data['User_Md'][umi_key]
#
#        ID_User_Media ,\
#        Media_Name    ,\
#        Media_Cost    ,\
#        Media_Slots   = Unpack_User_Md_Val(umi_val) 
#
#        #print n,\
#        #    ID_User,\
#        #    ID_User_Media ,\
#        #    Media_Name    ,\
#        #    Media_Cost    ,\
#        #    Media_Slots
#
#        data['User_Md_Paid'][umi_key] = 0
#
#        uu = 0
#        for undm_key in UsNeigDsMd_keys:
#            uu += 1
#
#            UsNeigDsMd_ID_User            ,\
#            UsNeigDsMd_ID_User_Media      ,\
#            ID_Country         ,\
#            ID_City            ,\
#            ID_Neighborhoods   ,\
#            ID_Digital_Signage ,\
#            ID_Owner           = Unpack_User_Neighb_Ds_Md_Key(undm_key) 
#
#            if   ID_User      != UsNeigDsMd_ID_User       : continue
#            elif ID_User_Media!= UsNeigDsMd_ID_User_Media : continue
#
#            Ow_Ds_key = Create_Ow_Ds_key(\
#                ID_Owner,
#                ID_Country,
#                ID_City,
#                ID_Neighborhoods,
#                ID_Digital_Signage)
#
#            Ds_key = Create_Ds_key(\
#                ID_Country,
#                ID_City,
#                ID_Neighborhoods,
#                ID_Digital_Signage)
#
#            data['Owner_Money'][ID_Owner]     = 0
#            data['Owner_Ds_Money'][Ow_Ds_key] = 0
#            data['User_Md_Ds_Paid'][undm_key] = 0
#
#            if not data['User_Md_Owner_List'].has_key(umi_key):
#                data['User_Md_Owner_List'][umi_key]=list()
#
#            if not ID_Owner in data['User_Md_Owner_List'][umi_key]:
#                data['User_Md_Owner_List'][umi_key].append(ID_Owner)
#
#
#            if not data['User_Md_Owner_Ds_List'].has_key(umi_key):
#                data['User_Md_Owner_Ds_List'][umi_key]=list()
#
#            if not ID_Owner in data['User_Md_Owner_Ds_List'][umi_key]:
#                data['User_Md_Owner_Ds_List'][umi_key][ID_Owner] = list()
#
#            if not Ds_key in data['User_Md_Owner_Ds_List'][umi_key][ID_Owner]:
#                data['User_Md_Owner_Ds_List'][umi_key][ID_Owner].append(Ds_key)
#
#
#
#
#
#
#
#            if not data['User_Md_Ds_List'].has_key(umi_key):
#                data['User_Md_Ds_List'][umi_key]=list()
#
#            if not Ow_Ds_key in data['User_Md_Ds_List'][umi_key][]:
#                data['User_Md_Ds_List'][umi_key].append(undm_key)
#
#
#
#            ID_Time_Interval = 0
#            for ID_Time_Interval in xrange(1, Time_Interval_Counter + 1):
#
#                undmt_key = \
#                    undm_key +','+\
#                    str(ID_Time_Interval)
#
#                data['User_Md_Ds_Ti_Paid_List'][undmt_key] = list()
#
#                uondmt_key = \
#                    umi_key +','+\
#                    Ow_Ds_key +','+\
#                    str(ID_Time_Interval)
#
#                data['User_Md_Owner_Ds_TI_Paid_List'][uondmt_key] = list()
#                data['Owner_Ds_Ti_Money'][uondmt_key] = 0
#
#
#    #print "data[User_Md_Ds_List][1,1001] = "
#    #pprint (data['User_Md_Ds_List']['1,1001'])
#
#
#-------------------------------------------------------------------------------
def Load_P_User_Md_Ow_Ds_Ti(data, con, cur):


    data['Us_Md_Ow_Ds_Ti']= dict()


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

        ID_User,\
        ID_User_Media = Unpack_User_Md_Key(umi_key) 

        umi_val = data['User_Md'][umi_key]

        ID_User_Media ,\
        Media_Name    ,\
        Media_Cost    ,\
        Media_Slots   = Unpack_User_Md_Val(umi_val) 

        #print n,\
        #    ID_User,\
        #    ID_User_Media ,\
        #    Media_Name    ,\
        #    Media_Cost    ,\
        #    Media_Slots

        #data['User_Md_Paid'][umi_key] = 0

        uu = 0
        for undm_key in UsNeigDsMd_keys:
            uu += 1

            UsNeigDsMd_ID_User            ,\
            UsNeigDsMd_ID_User_Media      ,\
            ID_Country         ,\
            ID_City            ,\
            ID_Neighborhoods   ,\
            ID_Digital_Signage ,\
            ID_Owner           = Unpack_User_Neighb_Ds_Md_Key(undm_key) 

            if   ID_User      != UsNeigDsMd_ID_User       : continue
            elif ID_User_Media!= UsNeigDsMd_ID_User_Media : continue

            Ow_Ds_key = Create_Ow_Ds_key(\
                ID_Owner,
                ID_Country,
                ID_City,
                ID_Neighborhoods,
                ID_Digital_Signage)

            Ds_key = Create_Ds_key(\
                ID_Country,
                ID_City,
                ID_Neighborhoods,
                ID_Digital_Signage)


            if not data['Us_Md_Ow_Ds_Ti'].has_key(umi_key):
                data['Us_Md_Ow_Ds_Ti'][umi_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Media_Cost'] = Media_Cost
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List'] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'] = dict()


            if not ID_Owner in data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List']:
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_List'].append(ID_Owner)
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'][ID_Owner] = 0
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'][ID_Owner] = dict()

            if not Ds_key in data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner]:
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_List'][ID_Owner].append(Ds_key)
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner][Ds_key] = list()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key] = dict()
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner][Ds_key] = 0


                Ds_Val = data['Digital_Signage'][Ds_key]
                
                Dig_Sign        ,\
                DS_Cost         ,\
                DS_Perc_Quality = Unpack_Ds_Val(Ds_Val)
                
                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Price'][ID_Owner][Ds_key] = DS_Cost

                data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Total_Cost'][ID_Owner] += DS_Cost


                iID_Time_Interval = 0
    
                for iID_Time_Interval in xrange(1, Time_Interval_Counter + 1):
    
                    ID_Time_Interval = str(iID_Time_Interval)

                    #undmt_key = \
                    #    undm_key +','+\
                    #    str(ID_Time_Interval)
    
                    data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_List'][ID_Owner][Ds_key].append(ID_Time_Interval)

                    undm_val = data['P_User_Neighb_Ds_Md_Ti'][undm_key]
                    #print uu,undm_key,"=>",undm_val


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


                    i = 0
                    for tp in TI_Prices_list:
                        i += 1

                        if tp == '':
                            continue
                        tpk = int(TI_Slots)-i
                        #print tpk,tp




                        if int(TI_Slots_Busy) > tpk:
                            continue

                        fti = float(tp)
            
                        if Clip_Budget_Start < fti:
                            continue


                        people_price = round(float(tp),3)
    



                        #if people_price < Min_4_Piople_Price :
                        #    continue

                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Price'][ID_Owner][Ds_key][ID_Time_Interval] = people_price
                        data['Us_Md_Ow_Ds_Ti'][umi_key]['Ow_Ds_Ti_Total_Price'][ID_Owner][Ds_key] += people_price

                        break



    #print "data[Digital_Signage] = "
    #pprint (data['Digital_Signage'])
    
    #print "data[Us_Md_Ow_Ds_Ti] = "
    #pprint (data['Us_Md_Ow_Ds_Ti'])
    
    print "data[Us_Md_Ow_Ds_Ti][1,1001] = "
    pprint (data['Us_Md_Ow_Ds_Ti']['1,1001'])

