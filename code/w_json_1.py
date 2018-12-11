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
data['people'] = []  
data['people'].append({  
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({  
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({  
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})


print "data = "
pprint (data)

CONF_GEN_CDS = 'data_cds_1.json'
#with open(CONF_GEN_CDS, 'w', encoding='utf8') as outfile:  
#with open(CONF_GEN_CDS, 'w', encoding='utf-8') as outfile:  
with open(CONF_GEN_CDS, 'w') as outfile:  
    #json.dump(data, sort_keys=True, indent=4, outfile)
    json.dump(data,  outfile)
    #json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False),  outfile) 

data_r = ''
Search_list = list()
if os.path.exists(CONF_GEN_CDS):
    with open(CONF_GEN_CDS) as f:
        data_r = json.load(f)
        #print data_r
        print "data_r = "
        pprint (data_r)
