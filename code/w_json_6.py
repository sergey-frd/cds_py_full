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


from db_cds_lib_1       import *

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

    data['base']['Digital_Signage_Cost_Min'] = 1000 
    data['base']['Digital_Signage_Cost_Max'] = 7000 

    data['base']['Time_Interval_Counter'] = 4 
    data['base']['Time_Interval_People'] = 10
    data['base']['Time_Slot_Cost'] = 10

    data['base']['Dig_Sign_Max_Time_Interv_Price'] = 10000000
    data['base']['Dig_Sign_Time_Interv_SQR'] = 0.9

    data['base']['CASE_DB_PRINT_TBL'] = 'nY' 
    data['base']['CASE_DB_PRINT_ALL'] = 'nY' 


## data['Country'] = dict()  
## data['aCountry'] = dict()  
## data['City'] = dict()  
## data['aCity'] = dict()  
## data['Neighborhood'] = dict()  
## data['aNeighborhood'] = dict()  
## data['Digital_Signage'] = dict()
#  
## data['User'] = dict()  
## data['User_Clip'] = dict()  
## data['User_Clip_Budget'] = dict()  
## data['User_Clip_Neighborhood'] = dict()  

## data['Time_Interval_dSign_People'] = dict()  
## data['Time_Interval_Price'] = dict()  
## data['Time_Interval_Slots'] = dict() 

## data['Owner'] = dict()  
## data['D_Sign_Owner'] = dict()  
## data['Digital_Signage_Cost'] = dict()  
#--------------------------------------------
data = {}  

gen_Base(data)
gen_Country_City_Neighborhood_D_Sign(data)
gen_User_Clip(data)
gen_Time_Slots(data)
gen_Owner_D_Sign(data)
gen_Neighb_User_Clips_dSign(data)
gen_Neighb_dSign_Owner(data)

#-----------------------------------------------
if  data['base']['CASE_DB_PRINT_TBL'] == 'Y':

    do_CASE_DB_PRINT_TBL(data)

#-----------------------------------------------
if  data['base']['CASE_DB_PRINT_ALL'] == 'Y':

    do_CASE_DB_PRINT_TBL(data)

#-----------------------------------------------






#-----------------------------------------------
#--------------------------------------------


#--------------------------------------------
out_data = {}  
