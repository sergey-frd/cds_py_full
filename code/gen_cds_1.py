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

#-------------------------------------------------------------------------------

## from lib_py_utils        import *
## #from scan_utils         import *
## from scan_utils2         import *

from difflib             import *
from pprint              import *


##from main_doxy4ug_lib_j import *
## from ug_api_cases       import *

#import pprint

#pp = pprint.PrettyPrinter(indent=2,width=100)
#import re, os, getopt, sys, time

#cpssRoot = "/home/serg/tmp/Marvell/cpss"
#
#integer_types = [ "int", "char", "short", "long" ]
#float_types = [ "float", "double" ]
#privateAPIStartsWith = ("prv", "pvr", "mv", "hws", "shmIpc", "gen")
#
#reName = re.compile(r"}\s*([a-zA-Z_]\w*);\r?\n?$")
#reTypedefInt = re.compile(r'typedef (signed |unsigned |short |long )*(int|char|short|long) ([a-zA-Z_][a-zA-Z_0-9]*);\r?\n?$')
#reStruct_field = re.compile(r"^\s*([a-zA-Z_]\w*)\s+([a-zA-Z_]\w*)(\s*\[(\d+)\])?;\r?\n?$")
#reStruct_comprex_field = re.compile(r"^\s*(struct|union)\s*\{\s*\.\.\.\s*\}\s*([a-zA-Z_]\w*);$")
#reStruct_comprex_field2 = re.compile(r"^\s*(struct|union)\s+[a-zA-Z_]\w*\s+([a-zA-Z_]\w*);$")
#reEnumItem = re.compile(r"\b([a-zA-Z_][a-zA-Z_0-9]*)\b(\s*=\s*\d+)?\s*,?")
#_reArrayParameter = re.compile(r"(\w+)\[(\w*)\]")
#_reCommentSection = re.compile(r'([A-Z\s]+):$')
#_reParamDescr = re.compile(r' {0,12}([a-zA-Z_][a-zA-Z_0-9]*) +- +(.*)$')
#
#reStructEmbedStart = re.compile(r"\s*(struct|union)(\s+[a-zA-Z_]\w*)?\s*{", 0)
#reStructEmbedMember = re.compile(r"\b([a-zA-Z_]\w*)\b\s*\*?\s*\b([a-zA-Z_]\w*)\s*;",0)
#reStructEmbedEnd = re.compile(r"}\s*([a-zA-Z_]\w*)\s*;",0)
#
#all_structs = dict()
#all_enums = dict()
#all_defs = dict() # [type] = "struct" || "enum" || "int"
#typeExcludeList = list()

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
        #pprint (data["Country"])
        #pprint (data["Country"]["1"])
        #pprint (data["Country"]["1"])
        pprint (data["Country"]["1"]["Name"])
        #pprint (data["Country"]["1"]["City"]["1"])
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


#-------------------------------------------------------------------------------
# main module stub to prevent auto execute
#

if __name__ == '__main__':
    akaMain(sys.argv)
    sys.exit(0)

