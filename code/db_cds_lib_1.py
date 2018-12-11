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

import random
#from random import randint
import math

from difflib             import *
from pprint              import *

#-------------------------------------------------------------------------------
#def Check_Price:

    ## print "---------------"
    ## Get_Price(1,1,14)
    ## Get_Price(1,7,14)
    ## Get_Price(1,13,14)
    ## Get_Price(2,1,61)
    ## Get_Price(2,30,61)
    ## Get_Price(2,60,61)
    ## Get_Price(3,1,216)
    ## Get_Price(3,100,216)
    ## Get_Price(3,215,216)
    ## Get_Price(4,1,864)
    ## Get_Price(4,400,864)
    ## Get_Price(4,863,864)
    ## print "---------------"

    #print "ds_txt = ",data['Digital_Signage'][101101109108]



#-------------------------------------------------------------------------------
def gen_Country_City_Neighborhood_D_Sign(data):

    #----------------------
    data['Country'] = dict()  
    data['aCountry'] = dict()  
    data['Country'][100]='ALL'  
    data['Country'][101]='Israel'  
    data['Country'][102]='USA'  
    data['Country'][103]='Russia' 

    #data['Country']['Cites']=list() 
    #data['Country']['Cites'].append(101101) 
    #data['Country']['Cites'].append(101102) 
    #data['Country']['Cites'].append(101103) 

    data['City'] = dict()  
    data['aCity'] = dict()  
    data['City'][101100]='Israel_ALL'   
    data['City'][101101]='Haifa'   
    data['City'][101102]='TelAviv'   
    data['City'][101103]='Jerusalem'   

    #data['City'][101101]['Neighborhoods']=list() 
    #data['City'][101101]['Neighborhoods'].append(101101101)
    #data['City'][101101]['Neighborhoods'].append(101101102)

    data['Neighborhood'] = dict()  
    data['aNeighborhood'] = dict()  
    data['Neighborhood'][101101100]='Haifa_ALL'   
    data['Neighborhood'][101101101]='Bat_Galim'
    data['Neighborhood'][101101102]='Denia'
    data['Neighborhood'][101101103]='French_Carmel'
    data['Neighborhood'][101101104]='German_Colony'
    data['Neighborhood'][101101105]='Hadar_HaCarmel'
    data['Neighborhood'][101101106]='Kababir'
    data['Neighborhood'][101101107]='Kiryat_Eliezer'
    data['Neighborhood'][101101108]='Kiryat_Haim'
    data['Neighborhood'][101101109]='Kiryat_Shmuel'


    data['Digital_Signage'] = dict()  

    cn_keys= data['Country'].keys()
    cn_keys.sort()
    #print "cn_keys = ",cn_keys


    cy_keys= data['City'].keys()
    cy_keys.sort()
    #print "cy_keys = ",cy_keys

    nb_keys= data['Neighborhood'].keys()
    nb_keys.sort()
    #print "nb_keys = ",nb_keys


    for cn in cn_keys:
        data['aCountry'][data['Country'][cn]] = cn
        if cn - 100 == 0:
            continue
        #print cn, "=> ",data['Country'][cn]

        for cy in cy_keys:
            data['aCity'][data['City'][cy]] = cy
            if cy/1000 != cn:
                continue
            if cy - (cn*1000) - 100 == 0:
                continue
            #print '   ',cy, "=>",data['City'][cy]


            for nb in nb_keys:
                data['aNeighborhood'][data['Neighborhood'][nb]] = nb
                if nb/1000000 != cn:
                    continue

                if nb/1000 != cy:
                    continue

                if nb - (cy*1000) - 100 == 0:
                    continue
                #print '      ',nb, "=>",data['Neighborhood'][nb]

                for d in xrange(0, data['base']['D_Sign_Counter']+1):
                    ds_key = nb*1000 +100 +d 
                    #print "ds_key=>",ds_key

                    #if d == 0:
                    #    data['Digital_Signage'][ds_key]=data['City'][cy] +'_' + \
                    #        data['Neighborhood'][nb] + \
                    #        '_ALL'
                    #else:
                    #    data['Digital_Signage'][ds_key] = \
                    #        data['City'][cy] +'_' +\
                    #        data['Neighborhood'][nb] + '_' +str(d)

                    if d == 0:
                        data['Digital_Signage'][ds_key]=\
                            data['Neighborhood'][nb] + \
                            '_ALL'
                    else:
                        data['Digital_Signage'][ds_key] = \
                            data['Neighborhood'][nb] + '_' +str(d)

#-------------------------------------------------------------------------------
def gen_User_Clip(data):

    data['User'] = dict()  
    data['User_Clip'] = dict()  
    data['User_Clip_Budget'] = dict()  
    data['User_Clip_Neighborhood'] = dict()  

    nb_keys= data['Neighborhood'].keys()
    nb_keys.sort()

    for d in xrange(0, data['base']['User_Counter'] +1 ):
        wn_key = 100 + d 
        #print "wn_key=>",wn_key
        if d == 0:
            data['User'][wn_key]='ALL'
        else:
            data['User'][wn_key] = 'User_' +str(d)

            Rand_User_Clip_Counter  = random.randint(1, data['base']['User_Clip_Counter']+1 )
            #print "gen_User_Clip: Rand_User_Clip_Counter = ", Rand_User_Clip_Counter

            for j in xrange(1, Rand_User_Clip_Counter):
                uk = wn_key*1000 + 100 + j

                data['User_Clip'][uk] = 'User_' +str(d) + '_Clip_' + str(j)

                data['User_Clip_Budget'][uk] = \
                    1000 * random.randint(data['base']['Clip_Budget_Min'],\
                         data['base']['Clip_Budget_Max'] )
        


                for n in xrange(1, data['base']['User_Clip_Neighborhood_Counter'] ):
                
                    x = random.choice(nb_keys)
                
                    data['User_Clip_Neighborhood'][uk] = x

#-------------------------------------------------------------------------------
def gen_Time_Slots(data):

    data['Time_Interval_dSign_People'] = dict()  
    data['Time_Interval_Price'] = dict()  
    data['Time_Interval_Slots'] = dict() 

    save = 0
    Total_Slots = 0
    for d in xrange(1, data['base']['Time_Interval_Counter']+1):

        ti_key =   100 + d 
        if save == 0:
            ti_val =   data['base']['Time_Interval_People']
        else:
            ti_val = (save * d) +  (data['base']['Time_Interval_People']*2) 
        save = ti_val

        data['Time_Interval_Price'][ti_key] = d
        data['Time_Interval_dSign_People'][ti_key] = ti_val
        data['Time_Interval_Slots'][ti_key] = 24*60*6 / ti_val

        Total_Slots += data['Time_Interval_Slots'][ti_key]

        #print d,"Total_Slots = ",Total_Slots

    print "Total_Slots = ",Total_Slots

#-------------------------------------------------------------------------------
def gen_Owner_D_Sign(data):

    data['Owner'] = dict()  
    data['Digital_Signage_Cost'] = dict()  

    for d in xrange(0, data['base']['Owner_Counter'] + 1):
        wn_key = 100 + d 
        #print "wn_key=>",wn_key
        if d == 0:
            data['Owner'][wn_key]='ALL'
        else:
            data['Owner'][wn_key] = 'Owner_' +str(d)


    data['D_Sign_Owner'] = dict()  
    Dig_Sign_keys= data['Digital_Signage'].keys()
    Dig_Sign_keys.sort()
    #print "nb_keys = ",nb_keys

    for dsk in Dig_Sign_keys:
        if dsk * 1000000000 - 100 == 0:
            continue

        data['Digital_Signage_Cost'][dsk] = \
            int(round(random.randint(\
                data['base']['Digital_Signage_Cost_Min'],\
                data['base']['Digital_Signage_Cost_Max'])/1000)*1000)

        for d in xrange(1, data['base']['D_Sign_Counter']):
            data['D_Sign_Owner'][dsk] = random.randint(1, \
                data['base']['Owner_Counter']) +100

#-------------------------------------------------------------------------------
def Get_Price(\
    base,\
    cur,\
    max):

    x = data['base']['Dig_Sign_Max_Time_Interv_Price']
    steps = max - cur
    #delta = x / steps
    print "---------------"
    #print "base=",base
    #print "cur=",cur
    #print "max=",max
    #print "x=",x
    #print "steps=",steps
    #print "delta=",delta


    #res = base
    res = x
    result=res

    for i in xrange(1, steps+1):
        d = max - i
        #res = res ** 0.9
        res = res ** data['base']['Dig_Sign_Time_Interv_SQR']
        ### print d,"int(res)=",int(res)
        result=int(res) + base

    #for d in xrange(1, cur):
    #
    #    res = base + delta * steps
    #    ##res = d*d
    #    ##res = ((res + base) * res) - result
    #    #res = ((res + base) * res) - result
    #
    #    print d,"res=",res
    #
    #    if res > 1000000000:
    #        break
    #    result=res
    #    print d,res

    #print "---------------"
    print i,d,"result=",result
    #print "---------------"
    return result


#---------------------------------------------

def do_CASE_DB_PRINT_ALL(data):

    print "---------------"
    print "data = "
    pprint (data)

#---------------------------------------------
def do_CASE_DB_PRINT_TBL(data):

    print "---------------"
    print "data['base'] = "
    pprint (data['base'])

    print "---------------"
    print "data['Time_Interval_Price'] = "
    pprint (data['Time_Interval_Price'])
    
    print "---------------"
    print "data['Time_Interval_dSign_People'] = "
    pprint (data['Time_Interval_dSign_People'])
    
    print "---------------"
    print "data['Time_Interval_Slots'] = "
    pprint (data['Time_Interval_Slots'])

    print "---------------"
    print "data['aCountry'] = "
    pprint (data['aCountry'])
    
    print "---------------"
    print "data['aCity'] = "
    pprint (data['aCity'])
    
    
    print "---------------"
    print "data['aNeighborhood'] = "
    pprint (data['aNeighborhood'])
    
    print "---------------"
    print "data['Digital_Signage'] = "
    pprint (data['Digital_Signage'])
    
    
    print "---------------"
    print "data['D_Sign_Owner'] = "
    pprint (data['D_Sign_Owner'])
    
    print "---------------"
    print "data['Owner'] = "
    pprint (data['Owner'])
    
    print "---------------"
    print "data['User'] = "
    pprint (data['User'])
    
    #print "---------------"
    print "data['User_Clip'] = "
    pprint (data['User_Clip'])
    
    print "---------------"
    print "data['User_Clip_Budget'] = "
    pprint (data['User_Clip_Budget'])
    
    print "---------------"
    print "data['Neighborhood'] = "
    pprint (data['Neighborhood'])
    
    print "---------------"
    print "data['User_Clip_Neighborhood'] = "
    pprint (data['User_Clip_Neighborhood'])

    print "---------------"
    print "data['Digital_Signage_Cost'] = "
    pprint (data['Digital_Signage_Cost'])

    print "---------------"
    print "data['Neighb_User_Clips_dSign'] = "
    pprint (data['Neighb_User_Clips_dSign'])


    print "---------------"
    print "data['Neighb_User_Clips'] = "
    pprint (data['Neighb_User_Clips'])


    print "---------------"
    print "data['Neighb_Owner_dSign_Slots'] = "
    pprint (data['Neighb_Owner_dSign_Slots'])


    print "---------------"
    print "data['Neighb_Owner_dSign'] = "
    pprint (data['Neighb_Owner_dSign'])

    print "---------------"
    print "data['Neighb_Owner_Cost'] = "
    pprint (data['Neighb_Owner_Cost'])
    
    print "---------------"
    print "data['Neighb_Cost'] = "
    pprint (data['Neighb_Cost'])

    print "---------------"
    print "data['Neighb_Owner_Cost'] = "
    pprint (data['Neighb_Owner_Cost'])

    print "---------------"
    print "data['Neighb_Cost'] = "
    pprint (data['Neighb_Cost'])

    print "---------------"
    print "data['Neighb_Owner_Percent'] = "
    pprint (data['Neighb_Owner_Percent'])


    print "---------------"
    print "data['Neighb_Owner_dSign_Percent'] = "
    pprint (data['Neighb_Owner_dSign_Percent'])

    print "---------------"
    print "data['Neighb_Owner'] = "
    pprint (data['Neighb_Owner'])


#---------------------------------------------
def gen_Neighb_dSign_Owner(data):

    #print 'gen_Neighb_dSign_Owner STARTED' 

    data['Neighb_Owner_dSign'] = dict()
    data['Neighb_Owner_dSign_Slots'] = dict()

    ds_keys= data['Digital_Signage'].keys()
    ds_keys.sort() 

    nb_keys= data['Neighborhood'].keys()
    nb_keys.sort() 

    dso_keys= data['D_Sign_Owner'].keys()
    dso_keys.sort() 

    tip_keys= data['Time_Interval_Price'].keys()
    tip_keys.sort() 

    nn = 0
    for ds_key in ds_keys:

        ds_txt = data['Digital_Signage'][ds_key]
        if 'ALL' in ds_txt:
            continue

        nn += 1
        nb_key = ds_key/1000

        nb_txt = data['Neighborhood'][nb_key]
        #print "ds_key=",ds_key,"nb_key=",nb_key,nb_txt,own_key

        own_key = data['D_Sign_Owner'][ds_key]
        #print "ds_key=",ds_key,"own_key=",own_key
        #print "ds_key=",ds_key,"nb_key=",nb_key,nb_txt,own_key

        own_txt = data['Owner'][own_key]
        #print "ds_key=",ds_key,"ds_txt=",ds_txt,"nb_key=",nb_key,"nb_txt=",nb_txt,"own_key=",own_key,"own_txt=",own_txt

        ds_cost = data['Digital_Signage_Cost'][ds_key]

        #print "ds_key=",ds_key,"ds_txt=",ds_txt,"nb_key=",nb_key,\
        #    "nb_txt=",nb_txt,"own_key=",own_key,\
        #    "own_txt=",own_txt,"ds_cost=",ds_cost


        for tip_key in tip_keys:


            tip_price = data['Time_Interval_Price'][tip_key]
            tip_slots = data['Time_Interval_Slots'][tip_key]
            tip_people = data['Time_Interval_dSign_People'][tip_key]

            koef =  ds_cost * 1000 / data['base']['Digital_Signage_Cost_Max']

            new_price  = int(round(tip_price  * koef*100)/1000)
            new_people = int(round(tip_people * koef*100)/1000)


            busy_slots = tip_slots - random.randint(tip_slots/5,tip_slots-2  )
            free_slots = tip_slots - busy_slots

            #print "tip_key=",tip_key,"koef=",koef,"tip_price=",tip_price,\
            #    "new_price=",new_price
            #
            #print "tip_people=",tip_people,\
            #     "new_people=",new_people
            #
            #print "tip_slots=",tip_slots,\
            #     "busy_slots=",busy_slots,"free_slots=",free_slots

            Neighb_Owner_dSign_Slots_Key =\
                str(nb_key) +','+ \
                str(own_key) +','+ \
                str(ds_key) +','+ \
                str(tip_key)

            Neighb_Owner_dSign_Slots_Val =\
                nb_txt  +','+\
                own_txt +','+\
                ds_txt  +','+\
                str(new_price) +','+ \
                str(new_people) +','+ \
                str(busy_slots) +','+ \
                str(free_slots)
    
            data['Neighb_Owner_dSign_Slots'][Neighb_Owner_dSign_Slots_Key] = \
                Neighb_Owner_dSign_Slots_Val

        Neighb_Owner_dSign_Key =\
            str(nb_key) +','+ \
            str(own_key) +','+ \
            str(ds_key)

        Neighb_Owner_dSign_Val = \
            nb_txt+','+\
            own_txt+','+\
            ds_txt+','+\
            str(ds_cost)
            

        data['Neighb_Owner_dSign'][Neighb_Owner_dSign_Key] = \
            Neighb_Owner_dSign_Val


        #print 'gen_Neighb_dSign_Owner: Neighb_Owner_dSign Neighb_Owner_dSign_Key=',\
        #    Neighb_Owner_dSign_Key,\
        #    '=>',Neighb_Owner_dSign_Val 

        #if nn >= 3:
        #    break

        #for nb in nb_keys:
        #    dso_key = data['D_Sign_Owner'][nb]
        #    nb_txt = data['Neighborhood'][nb]



    #print 'gen_Neighb_dSign_Owner ENDED' 
#-------------------------------------------------------------------------------
def gen_Neighb_User_Clips_dSign(data):

    data['Neighb_User_Clips'] = dict()
    data['Neighb_User_Clips_dSign'] = dict()


    ds_keys= data['Digital_Signage'].keys()
    ds_keys.sort() 

    nb_keys= data['Neighborhood'].keys()
    nb_keys.sort() 

    us_keys= data['User'].keys()
    us_keys.sort() 

    usc_keys= data['User_Clip'].keys()
    usc_keys.sort() 

    uscn_keys= data['User_Clip_Neighborhood'].keys()
    uscn_keys.sort() 

    uscbn_keys= data['User_Clip_Budget'].keys()
    uscbn_keys.sort() 

    #dso_keys= data['D_Sign_Owner'].keys()
    #dso_keys.sort() 
    #
    #tip_keys= data['Time_Interval_Price'].keys()
    #tip_keys.sort() 

    nn = 0
    for us_key in us_keys:
        us_txt = data['User'][us_key]

        for usc_key in usc_keys:
            if usc_key/1000 != us_key:
                continue

            usc_txt = data['User_Clip'][usc_key]
            nb_key = data['User_Clip_Neighborhood'][usc_key]
            uc_Budget = data['User_Clip_Budget'][usc_key]

            nb_txt = data['Neighborhood'][nb_key]

            if 'ALL' in nb_txt:
                continue
            nn = 0
            for ds_key in ds_keys:


                ds_txt = data['Digital_Signage'][ds_key]
                if 'ALL' in ds_txt:
                    continue

                nn += 1
                nbdc_key = ds_key/1000

                if nbdc_key != nb_key:
                    continue

                uc_Slots = uc_Budget/ data['base']['Time_Slot_Cost']

                #print "us_key=",us_key,"us_txt=",us_txt,"usc_txt=",usc_txt,\
                #    "nb_key=",nb_key,\
                #    "uc_Budget=",uc_Budget,"uc_Slots=",uc_Slots,\
                #    "ds_key=",ds_key,"ds_txt=",ds_txt


                Neighb_User_Clips_Key = \
                     str(nb_key) +','+ \
                     str(us_key) +','+ \
                     str(usc_key)

                Neighb_User_Clips_Key_Val =\
                    nb_txt+','+\
                    us_txt+','+\
                    usc_txt+','+\
                    str(uc_Budget) +','+\
                    str(uc_Slots)

                Neighb_User_Clips_dSign_Key =\
                     str(nb_key) +','+\
                     str(us_key) +','+\
                     str(ds_key)

                Neighb_User_Clips_dSign_Val =\
                    nb_txt+','+\
                    us_txt+','+\
                    usc_txt+','+\
                    ds_txt

                data['Neighb_User_Clips'][Neighb_User_Clips_Key] = \
                Neighb_User_Clips_Key_Val

                data['Neighb_User_Clips_dSign'][Neighb_User_Clips_dSign_Key] = \
                    Neighb_User_Clips_dSign_Val

                #if nn >= 10:
                #    break

#---------------------------------------------

def gen_Neighb_Owner_Percent(data):


    data['Neighb_Owner_dSign_Percent'] = dict()
    data['Neighb_Owner_Cost'] = dict()
    data['Neighb_Owner_Percent'] = dict()
    data['Neighb_Cost'] = dict()


    nods_keys= data['Neighb_Owner_dSign'].keys()
    nods_keys.sort() 
    #nn = 0
    for nods_key in nods_keys:

        ds_key_list = nods_key.split(',')

        nb_key  = ds_key_list[0]
        own_key = ds_key_list[1]
        ds_key  = ds_key_list[2]

        Neighb_Owner_Key =\
            str(nb_key) +','+ \
            str(own_key)

        nods_val = data['Neighb_Owner_dSign'][nods_key]
        nods_val_list = nods_val.split(',')
        ds_cost  = int(nods_val_list[3])

        if not  data['Neighb_Owner_Cost'].has_key(Neighb_Owner_Key):
            data['Neighb_Owner_Cost'][Neighb_Owner_Key] = 0

        data['Neighb_Owner_Cost'][Neighb_Owner_Key] += ds_cost

        if not  data['Neighb_Cost'].has_key(nb_key):
            data['Neighb_Cost'][nb_key] = 0

        data['Neighb_Cost'][nb_key] += ds_cost
        #---------------------------------------------

        noc_keys= data['Neighb_Owner_Cost'].keys()
        noc_keys.sort() 

        for noc_key in noc_keys:

            ds_key_list = noc_key.split(',')

            nb_key  = ds_key_list[0]
            own_key = ds_key_list[1]

            nb_cost = data['Neighb_Cost'][nb_key]

            noc_cost = data['Neighb_Owner_Cost'][noc_key]
            N_Own_Perc = noc_cost *100 / nb_cost

            noc_val = \
                str(noc_cost) +','+\
                str(N_Own_Perc)

            data['Neighb_Owner_Percent'][noc_key] = noc_val


    #---------------------------------------------



    nods_keys= data['Neighb_Owner_dSign'].keys()
    nods_keys.sort() 
    nn = 0
    for nods_key in nods_keys:

        ds_key_list = nods_key.split(',')

        nb_key  = ds_key_list[0]
        own_key = ds_key_list[1]
        ds_key  = ds_key_list[2]

        Neighb_Owner_Key =\
            str(nb_key) +','+ \
            str(own_key)

        Neighb_Owner_dSign_Val = data['Neighb_Owner_dSign'][nods_key]

        #print 'gen_Neighb_Owner_Percent: Neighb_Owner_dSign nods_key=',\
        #    nods_key,\
        #    '=>',Neighb_Owner_dSign_Val 

        nods_val_list = Neighb_Owner_dSign_Val.split(',')
        
        nb_txt  = nods_val_list[0]
        own_txt  = nods_val_list[1]
        ds_txt  = nods_val_list[2]
        ds_cost  = int(nods_val_list[3])
        
        noc_cost = data['Neighb_Owner_Cost'][Neighb_Owner_Key]
        
        nods_Percent = ds_cost *100/noc_cost
        
        data['Neighb_Owner_dSign_Percent'][nods_key] = \
            Neighb_Owner_dSign_Val  +','+ \
            str(nods_Percent)

    #print "---------------"
    #print "data['Neighb_Owner_dSign_Percent'] = "
    #pprint (data['Neighb_Owner_dSign_Percent'])

#---------------------------------------------
def gen_Neighb_Owner(data):


    #print "---------------"
    #print "data['Neighb_Owner_dSign'] = "
    #pprint (data['Neighb_Owner_dSign'])
    #
    #print "---------------"
    #print "data['Neighb_Owner_Cost'] = "
    #pprint (data['Neighb_Owner_Cost'])  
     
    #print "---------------"
    #print "data['Owner'] = "
    #pprint (data['Owner'])

    data['Neighb_Owner'] = dict()  

    Dig_Sign_keys= data['D_Sign_Owner'].keys()
    Dig_Sign_keys.sort()

    for dsk in Dig_Sign_keys:
        if dsk * 1000000000 - 100 == 0:
            continue

        dsk_val = Dig_Sign_keys= data['D_Sign_Owner'][dsk]
        nb = dsk/1000
        #print "Digital_Signage: dsk = ",dsk,'=>',dsk_val,nb,'=>',dsk_val
        #print "Neighb_Owner: dsk = ",nb,'=>',dsk_val

        if not  data['Neighb_Owner'].has_key(nb):
            data['Neighb_Owner'][nb] = list()

        if not dsk_val in data['Neighb_Owner'][nb]:
            data['Neighb_Owner'][nb].append(dsk_val)

        #val = data['Neighb_Owner'][nb]
        #data['Neighb_Owner'][nb] = val.sort()

    #print "---------------"
    #print "data['Neighb_Owner'] = "
    #pprint (data['Neighb_Owner'])

#---------------------------------------------
def Planning_Neighb_User_Owner_Percent(data):

    print "---------------"
    print "data['Neighb_User_Clips'] = "
    pprint (data['Neighb_User_Clips'])

    #data['Neighb_Owner'] =
    #{101101101L: [102, 101, 103]
    # 101101102L: [102, 101, 103]
    # 101101103L: [102, 101],
    # 101101104L: [102, 101],
    # 101101105L: [101, 102, 103]
    # 101101106L: [103, 102, 101]
    # 101101107L: [101, 103, 102]
    # 101101108L: [102, 101, 103]
    # 101101109L: [102, 103]} 

    #-----------------------------------------------
    #data['Neighb_User_Clips'] = 
    #{'101101103,103,103102': 'French_Carmel,User_3,User_3_Clip_2,9000,900',
    # '101101106,101,101102': 'Kababir,User_1,User_1_Clip_2,4000,400',
    # '101101109,103,103101': 'Kiryat_Shmuel,User_3,User_3_Clip_1,1000,100'}

    #data['Neighb_Owner_Percent'] = 
    #{'101101101,101': '8000,61',
    # '101101101,102': '5000,38',
    # '101101102,101': '5000,83',
    # '101101102,102': '1000,16',
    # '101101103,101': '3000,50',
    # '101101103,102': '3000,50',
    # '101101104,101': '8000,61',
    # '101101104,102': '5000,38',
    # '101101105,101': '5000,45',
    # '101101105,102': '6000,54',
    # '101101106,101': '7000,70',
    # '101101106,102': '3000,30',
    # '101101107,101': '8000,61',
    # '101101107,102': '5000,38',
    # '101101108,101': '11000,91',
    # '101101108,102': '1000,8',
    # '101101109,101': '4000,33',
    # '101101109,102': '8000,66'}

    usnc_keys= data['Neighb_User_Clips'].keys()
    usnc_keys.sort() 

    nn = 0
    for Neighb_User_Clips_Key in usnc_keys:

        Neighb_User_Clips_Val = \
            data['Neighb_User_Clips'][Neighb_User_Clips_Key]

        #print 'Neighb_User_Clips_Key =',Neighb_User_Clips_Key
        print Neighb_User_Clips_Key,'=>',Neighb_User_Clips_Val


        usnc_val_list = Neighb_User_Clips_Key.split(',')
        nb_key  = int(usnc_val_list[0])
        us_key  = int(usnc_val_list[1])
        usc_key = int(usnc_val_list[2])

        Neighb_Owner_list = data['Neighb_Owner'][nb_key]
        #print Neighb_User_Clips_Key,'Neighb_Owner_list =',Neighb_Owner_list

        for own in Neighb_Owner_list:
            #if nb != nb_key:
            #print nb_key,'=>',own

            Neighb_Owner_Perc_Key =\
                str(nb_key) +','+ str(own)

            #print 'Neighb_Owner_Perc_Key =',Neighb_Owner_Perc_Key

            if data['Neighb_Owner_Percent'].has_key(Neighb_Owner_Perc_Key):
                Neighb_Owner_Perc_val =\
                    data['Neighb_Owner_Percent'][Neighb_Owner_Perc_Key]

                print Neighb_Owner_Perc_Key,'=>',Neighb_Owner_Perc_val


#-------------------------------------------------------------------------------
def gen_JSON(data):
    
    CONF_GEN_CDS = 'data_cds_10.json'
    #with open(CONF_GEN_CDS, 'w', encoding='utf8') as outfile:  
    #with open(CONF_GEN_CDS, 'w', encoding='utf-8') as outfile:  
    with open(CONF_GEN_CDS, 'w') as outfile:  
        #json.dump(data, sort_keys=True, indent=4, outfile)
        json.dump(data,  outfile)
        #json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False),  outfile) 
    
    #data_r = ''
    #Search_list = list()
    #if os.path.exists(CONF_GEN_CDS):
    #    with open(CONF_GEN_CDS) as f:
    #        data_r = json.load(f)
    #        #print data_r
    #        print "data_r = "
    #        pprint (data_r)
