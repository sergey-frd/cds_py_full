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

data = {}  

#----------------------
data['Clip'] = dict()  
for d in xrange(0, 10):
    wn_key = 100 + d 
    #print "wn_key=>",wn_key
    if d == 0:
        data['Clip'][wn_key]='ALL'
    else:
        data['Clip'][wn_key] = 'Clip_' +str(d)

#----------------------
data['User'] = dict()  
for d in xrange(0, 10):
    wn_key = 100 + d 
    #print "wn_key=>",wn_key
    if d == 0:
        data['User'][wn_key]='ALL'
    else:
        data['User'][wn_key] = 'User_' +str(d)

#----------------------
data['Owner'] = dict()  
for d in xrange(0, 10):
    wn_key = 100 + d 
    #print "wn_key=>",wn_key
    if d == 0:
        data['Owner'][wn_key]='ALL'
    else:
        data['Owner'][wn_key] = 'Owner_' +str(d)

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

#-----------------------------------------------
data['D_Sign_Owner'] = dict()  

Dig_Sign_keys= data['Digital_Signage'].keys()
Dig_Sign_keys.sort()
#print "nb_keys = ",nb_keys

for DSK in Dig_Sign_keys:
    if DSK * 1000000000 - 100 == 0:
        continue
    for d in xrange(1, 10):
        data['D_Sign_Owner'][DSK] = random.randint(1, 9) +100

#-----------------------------------------------
data['User_Clip'] = dict()  

U_keys= data['User'].keys()
U_keys.sort()
#print "nb_keys = ",nb_keys

for UK in U_keys:

    if UK - 100 == 0:
        continue
    
    #if random.randint(1, 9) < 7:
    #    continue
        

    for d in xrange(1, 10):
        data['User_Clip'][UK] = random.randint(1, 9) +100


#-----------------------------------------------
print "data = "
pprint (data)

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
