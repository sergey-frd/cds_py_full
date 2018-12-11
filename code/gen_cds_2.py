#------------------------------------------------------------------------------
#  File name: gen_cds_1.py
#------------------------------------------------------------------------------
# Usage:
#TODO

#--------------------------------------------------
#  File version: 3 $
#--------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------

## from lib_py_utils        import *
## #from scan_utils         import *
## from scan_utils2         import *

from difflib             import *
from pprint              import *



#-------------------------------------------------------------------------------
def gen_city():

    for d in xrange(1, 10):
        i = random.randint(1, 10)
        print d,i
#-------------------------------------------------------------------------------
def get_conf_json_all(data,dict_conf):

    #print "-----------------------------"
    for section in data:
        #print "section=", section
        if section == 'comment':
            continue

        dict_conf[section]=dict()
        for option in data[section]:
            if option != '':
                #str_opt=str(option)
                str_opt = option

                if option == 'comment':
                    continue

                #print section,"   option=", option

                #if type(data[section][option]) is str:
                if type(data[section][option]) != list: 
                    #print section,option,'type=',type(data[section][option])
                    val=data[section][option]
                    str_val=str(val)
                    if val != '':

                        dict_conf[section][str_opt]=dict()
                        if  str_opt in os.environ:
                            #print section,option + ': ', os.getenv(str_opt)

                            str_opt.replace('\\','/')
                            dict_conf[section][str_opt] = os.getenv(str_opt)
                        else:
                            #print section,str_opt + ': ',str_val
                            str_val.replace('\\','/')
                            dict_conf[section][str_opt]=str_val
                else:
                    #print '*** type is list: ', section,option,data[section][option]
                    dict_conf[section][option]=data[section][option]

#-------------------------------------------------------------------------------
# main module with import feature
#
def akaMain(argv):


    argc = len(argv)

    i=1

    CONF_GEN_CDS        =sys.argv[i]; i=i+1
    #CONF_DOXY4UG  ='c:\\Git\\w01\cpss\\tools\\DoxyGen\\conf_doxy4ug.ini'

    CONF_GEN_CDS   =os.path.normpath(CONF_GEN_CDS)

    print "CONF_GEN_CDS         : ",CONF_GEN_CDS  


    #if  'CONF_XML_FUNCDESCR' in os.environ:
    #    #print 'in os.environ: CONF_XML_FUNCDESCR' + ': ', os.getenv('CONF_XML_FUNCDESCR')
    #    CONF_XML_FUNCDESCR = os.getenv('CONF_XML_FUNCDESCR')
    #else:
    #    #pwd = os.path.abspath('')
    #    #print 'pwd =', pwd
    #    CONF_XML_FUNCDESCR = os.path.join(\
    #        cpssRoot, \
    #        'mainLuaWrapper', \
    #        'scripts', \
    #        'xml_funcdescr.json')
    #
    #print "CONF_GEN_CDS=",CONF_GEN_CDS  

    data = ''
    Search_list = list()
    if os.path.exists(CONF_GEN_CDS):
        with open(CONF_GEN_CDS) as f:
            data = json.load(f)
            #print data

        #dict_conf=dict()
        #get_conf_json_all(data,dict_conf)
        #
        #print "dict_conf = "
        #pprint (dict_conf)


        print "data = "

        pprint (data)

        ## #pprint (data["Country"])
        ## #pprint (data["Country"]["1"])
        ## #pprint (data["Country"]["1"])
        ## pprint (data["Country"]["1"]["Name"])
        ## #pprint (data["Country"]["1"]["City"]["1"])
        pprint (data["Country"]["1"]["City"]["1"]["Name"])
        #pprint (data["Country"]["1"]["City"]["1"]["Neighborhoods"])
        pprint (data["Country"]["1"]["City"]["1"]["Neighborhoods"]["5"])



        ##print '-- Search -- Search_list ---------------------------------------------------'
        #for Path in dict_conf['Search']['Search_list']:
        #    if Path != '':
        #        #print 'Path =', Path
        #        Search_list.append(os.path.normpath(Path)) 
        ##pprint (Search_list)
    else:
        print "Not Found CONF_XML_FUNCDESCR=",CONF_XML_FUNCDESCR  

    gen_city()

#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    akaMain(sys.argv)
    sys.exit(0)

