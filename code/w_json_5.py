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
def gen_Base(data):

    data['base'] = dict()  
    data['base']['User_Counter'] = 10 
    data['base']['Owner_Counter'] = 10 
    data['base']['D_Sign_Counter'] = 10 
    data['base']['User_Clip_Counter'] = 5 
    data['base']['User_Clip_Neighborhood_Counter'] = 3 
    data['base']['Clip_Budget_Min'] = 1 
    data['base']['Clip_Budget_Max'] = 12 

    data['base']['Time_Interval_Counter'] = 4 
    data['base']['Time_Interval_People'] = 10

    data['base']['Dig_Sign_Max_Time_Interv_Price'] = 10000000
    data['base']['Dig_Sign_Time_Interv_SQR'] = 0.9

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

                for d in xrange(0, 10):
                    ds_key = nb*1000 +100 +d 
                    #print "ds_key=>",ds_key
                    if d == 0:
                        data['Digital_Signage'][ds_key]=data['City'][cy] +'_' + \
                            data['Neighborhood'][nb] + \
                            '_ALL'
                    else:
                        data['Digital_Signage'][ds_key] = \
                            data['City'][cy] +'_' +\
                            data['Neighborhood'][nb] + '_' +str(d)

#-------------------------------------------------------------------------------
def gen_User_Clip(data):

    data['User'] = dict()  
    data['User_Clip'] = dict()  
    data['User_Clip_Budget'] = dict()  
    data['User_Clip_Neighborhood'] = dict()  

    nb_keys= data['Neighborhood'].keys()
    nb_keys.sort()

    for d in xrange(0, data['base']['User_Counter'] ):
        wn_key = 100 + d 
        #print "wn_key=>",wn_key
        if d == 0:
            data['User'][wn_key]='ALL'
        else:
            data['User'][wn_key] = 'User_' +str(d)

            Rand_User_Clip_Counter  = random.randint(1, data['base']['User_Clip_Counter'] )
            print "gen_User_Clip: Rand_User_Clip_Counter = ", Rand_User_Clip_Counter

            for j in xrange(1, Rand_User_Clip_Counter):
                uk = wn_key*1000 + 100 + j

                data['User_Clip'][uk] = 'User_' +str(d) + '_Clip_' + str(j)

                data['User_Clip_Budget'][uk] = \
                    10 * random.randint(data['base']['Clip_Budget_Min'],\
                         data['base']['Clip_Budget_Max'] )
        


                for n in xrange(1, data['base']['User_Clip_Neighborhood_Counter'] ):
                
                    x = random.choice(nb_keys)
                
                    data['User_Clip_Neighborhood'][uk] = x

#-------------------------------------------------------------------------------
def gen_Time_Slots(data):

    data['Time_Interval_dSign'] = dict()  
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
        data['Time_Interval_dSign'][ti_key] = ti_val
        data['Time_Interval_Slots'][ti_key] = 24*60*6 / ti_val

        Total_Slots += data['Time_Interval_Slots'][ti_key]

        #print d,"Total_Slots = ",Total_Slots

    print "Total_Slots = ",Total_Slots

#-------------------------------------------------------------------------------
def gen_Owner_D_Sign(data):

    data['Owner'] = dict()  

    for d in xrange(0, data['base']['Owner_Counter']):
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
        for d in xrange(1, data['base']['D_Sign_Counter']):
            data['D_Sign_Owner'][dsk] = random.randint(1, data['base']['D_Sign_Counter'] -1) +100

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
#--------------------------------------------
data = {}  

#----------------------

gen_Base(data)
gen_Country_City_Neighborhood_D_Sign(data)
gen_User_Clip(data)
gen_Time_Slots(data)
gen_Owner_D_Sign(data)



#-----------------------------------------------

print "---------------"
#print "data = "
#pprint (data)

print "---------------"
print "data['base'] = "
pprint (data['base'])

print "---------------"
print "data['Time_Interval_Price'] = "
pprint (data['Time_Interval_Price'])

print "---------------"
print "data['Time_Interval_dSign'] = "
pprint (data['Time_Interval_dSign'])

print "---------------"
print "data['Time_Interval_Slots'] = "
pprint (data['Time_Interval_Slots'])

#print "---------------"
#print "data['aCountry'] = "
#pprint (data['aCountry'])
#
#print "---------------"
#print "data['aCity'] = "
#pprint (data['aCity'])
#
#
#print "---------------"
#print "data['aNeighborhood'] = "
#pprint (data['aNeighborhood'])
#
#print "---------------"
#print "data['Digital_Signage'] = "
#pprint (data['Digital_Signage'])
#
#
#print "---------------"
#print "data['D_Sign_Owner'] = "
#pprint (data['D_Sign_Owner'])
#
#print "---------------"
#print "data['Owner'] = "
#pprint (data['Owner'])
#
#print "---------------"
#print "data['User'] = "
#pprint (data['User'])
#
##print "---------------"
#print "data['User_Clip'] = "
#pprint (data['User_Clip'])
#
#print "---------------"
#print "data['User_Clip_Budget'] = "
#pprint (data['User_Clip_Budget'])
#
#print "---------------"
#print "data['Neighborhood'] = "
#pprint (data['Neighborhood'])
#
#print "---------------"
#print "data['User_Clip_Neighborhood'] = "
#pprint (data['User_Clip_Neighborhood'])

print "---------------"
Get_Price(1,1,14)
Get_Price(1,7,14)
Get_Price(1,13,14)
Get_Price(2,1,61)
Get_Price(2,30,61)
Get_Price(2,60,61)
Get_Price(3,1,216)
Get_Price(3,100,216)
Get_Price(3,215,216)
Get_Price(4,1,864)
Get_Price(4,400,864)
Get_Price(4,863,864)
print "---------------"

#print "ds_txt = ",data['Digital_Signage'][101101109108]

# 
# CONF_GEN_CDS = 'data_cds_1.json'
# #with open(CONF_GEN_CDS, 'w', encoding='utf8') as outfile:  
# #with open(CONF_GEN_CDS, 'w', encoding='utf-8') as outfile:  
# with open(CONF_GEN_CDS, 'w') as outfile:  
#     #json.dump(data, sort_keys=True, indent=4, outfile)
#     json.dump(data,  outfile)
#     #json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False),  outfile) 
# 
# data_r = ''
# Search_list = list()
# if os.path.exists(CONF_GEN_CDS):
#     with open(CONF_GEN_CDS) as f:
#         data_r = json.load(f)
#         #print data_r
#         print "data_r = "
#         pprint (data_r)
