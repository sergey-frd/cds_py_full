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


import random
#from random import randint
import math
#-------------------------------------------------------------------------------
#
#########################################################################################
def load_nb_us(\
        data,\
        con,\
        cur\
        ):

    DB_TABLE = 'User_Neighb'
    data['P_User_Neighb'] = dict() 

    with con:
        con.row_factory = lite.Row
        cur = con.cursor()    

        cur.execute("SELECT  \
            User_Neighb.ID_User,\
            User_Neighb.ID_Country,\
            User_Neighb.ID_City,\
            User_Neighb.ID_Neighborhoods,\
            User_Neighb.Neighborhood \
            FROM User_Neighb ")

        con.commit()

        rows = cur.fetchall()

        nn=0
        for line in rows:
            nn=nn+1

            ti_key = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]

            ti_val = \
                line["ID_User"]+','+ \
                line["ID_Country"]+','+ \
                line["ID_City"]+','+ \
                line["ID_Neighborhoods"]+','+ \
                line["Neighborhood"]

            data['P_User_Neighb'][ti_key] = ti_val 

