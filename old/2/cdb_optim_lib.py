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
def Get_Price(\
    data,\
    base,\
    cur,\
    max):

    x = data['Base']['Dig_Sign_Max_Time_Interv_Price']

    steps = max - cur
    print "---------------"
    res = x
    result=res

    for i in xrange(1, steps+1):
        d = max - i
        #res = res ** 0.9
        res = res ** data['Base']['Dig_Sign_Time_Interv_SQR']
        ### print d,"int(res)=",int(res)
        result=int(res) + base

    #print "---------------"
    print i,d,"result=",result
    #print "---------------"
    return result

#-------------------------------------------------------------------------------

def Optim_Plan(data, con, cur): 

    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    def random_opt(domain, costf):
     best=999999999
     bestr=None

     for i in xrange(0, 1000):
      # Выбрать случаиное решение
      r = [random.randint(0, domain[i]) for i in xrange(len(domain))]

      ##slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
      ##len_slots = len(slots)
      w_domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
      #w_domain = domain
      #print 'w_domain=',w_domain
      
      #------------------------------------
      r = list()
      for j in xrange(len(domain)):
          x = random.choice(w_domain)
          #x = random.randint(0, w_domain[j])
          r.append(x)
          #print j,'x->',x,'w_domain->', w_domain,'r==>', r
          w_domain.remove(x)

      # Get the cost
      cost = costf(r)

      # Сравнить со стоимостью наилучшего наиденного к этому моменту решения
      if cost < best:
       best = cost
       bestr = r
       print '-->bestr=',bestr,cost

     return bestr, best

    #-------------------------------------------------------------------------------
    def dorm_cost_(vec):

     #print '-->vec=',vec
     cost=0

     # Создаем список отсеков, т.е. первые 2 места - 0 отсек и т.д.
     slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
     #print '-->slots=',slots

     # Цикл по студентам, i - порядковый номер студента
     for i in xrange(len(vec)):
      x = int(vec[i])
      #print 'x->',x
      #print 'slots[x]->',slots[x]
      dorm = dorms[slots[x]]
      pref = prefs[i][1]
      #print i,x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm

      # Стоимость основного пожелания равна 0, альтернативного – 1
      # Если комната не входит в список пожеланий, стоимость увеличивается на 3

      #if pref[0] == dorm: cost += 0; print i,'+= 0 cost=',cost
      #elif pref[1] == dorm: cost += 1; print i,'+= 1 cost=',cost
      #else: cost += 3; print i,'+= 3 cost=',cost

      if pref[0] == dorm: cost += 0
      elif pref[1] == dorm: cost += 1
      else: cost += 3

      #print i,'cost=',cost
      # Удалить выбранный отсек
      # Это самое важное действие тут,
      # прошу особо обратить на него внимание и учесть, что элементы сдвигаются

      ###del slots[x]

      #k = 0
      #for ix in slots:
      #  if ix == slots[x]:
      #      del slots[k]
      #      print ix,'del slots[k] =',slots[k]
      #      break
      #  k += 1
      #
      #print i,x,'->slots=',slots

     #print '*=>cost=',cost
     return cost
    #-------------------------------------------------------------------------------


    #    Целевая функция работает следующим 
    #    образом.  Создается начальный список 
    #    отсеков, и уже использованные отсеки из 
    #    него удаляются.  Стоимость вычисляется 
    #    путем сравнения комнаты, в которую 
    #    студент помещен, с двумя его 
    #    пожеланиями.  Стоимость не изменяется, 
    #    если студенту досталась та комната, в 
    #    которую он больше всего хотел 
    #    поселиться; увеличивается на 1, если это 
    #    второе из его пожеланий; и увеличивается 
    #    на 3, если он вообще не хотел жить в этой 
    #    комнате.  

    def dorm_cost(vec):

     cost=0

     # Создаем список отсеков, т.е. первые 2 места - 0 отсек и т.д.
     slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

     # Цикл по студентам, i - порядковый номер студента
     for i in xrange(len(vec)+2):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        #print x, '->', slots[x],'->', prefs[i][0], pref, '->', dorm

        # Стоимость основного пожелания равна 0, альтернативного – 1
        # Если комната не входит в список пожеланий, стоимость увеличивается на 3
        if pref[0] == dorm: cost += 0
        elif pref[1] == dorm: cost += 1
        else: cost += 3

        # Удалить выбранный отсек
        # Это самое важное действие тут,
        # прошу особо обратить на него внимание и учесть, что элементы сдвигаются
        del slots[x]

     return cost

    #-------------------------------------------------------------------------------
    print '***************************************'
    print '***************************************'


    data_opt = dict() 
     
    data_opt['user'] = dict()  
    data_opt['0'] = 'Toby'    
    data_opt['1'] = 'Steve'   
    data_opt['2'] = 'Karen'   
    data_opt['3'] = 'Sarah'   
    data_opt['4'] = 'Dave'    
    data_opt['5'] = 'Jeff'    
    data_opt['6'] = 'Fred'    
    data_opt['7'] = 'Suzie'   
    data_opt['8'] = 'Laura'   
    data_opt['9'] = 'James' 

    data_opt['user_prior'] = dict()  
    data_opt['0,0'] = 'Toby'    
    data_opt['0,1'] = 'Toby'    
    data_opt['1,0'] = 'Steve'   
    data_opt['1,1'] = 'Steve'   
    data_opt['2,0'] = 'Karen'   
    data_opt['2,1'] = 'Karen'   
    data_opt['3,0'] = 'Sarah'   
    data_opt['3,1'] = 'Sarah'   
    data_opt['4,0'] = 'Dave'    
    data_opt['4,1'] = 'Dave'    
    data_opt['5,0'] = 'Jeff'    
    data_opt['5,1'] = 'Jeff'    
    data_opt['6,0'] = 'Fred'    
    data_opt['6,1'] = 'Fred'    
    data_opt['7,0'] = 'Suzie'   
    data_opt['7,1'] = 'Suzie'   
    data_opt['8,0'] = 'Laura'   
    data_opt['8,1'] = 'Laura'   
    data_opt['9,0'] = 'James' 
    data_opt['9,1'] = 'James' 



    data_opt['slot'] = dict()  
    data_opt['0'] = 'slot_0'    
    data_opt['1'] = 'slot_1' 

    data_opt['rms'] = dict()  

    data_opt['0'] = 'Zeus'    
    data_opt['1'] = 'Athena'   
    data_opt['2'] = 'Hercules'   
    data_opt['3'] = 'Bacchus'   
    data_opt['4'] = 'Pluto'    
              

    data_opt['rms_slot_indx'] = dict()  
    data_opt['0'] = '0,0,Zeus,slot_0'    
    data_opt['1'] = '0,1,Zeus,slot_1'    
    data_opt['2'] = '1,0,Athena,slot_0'   
    data_opt['3'] = '1,1,Athena,slot_1'   
    data_opt['4'] = '2,0,Hercules,slot_0'   
    data_opt['5'] = '2,1,Hercules,slot_1'   
    data_opt['6'] = '3,0,Bacchus,slot_0'   
    data_opt['7'] = '3,1,Bacchus,slot_1'   
    data_opt['8'] = '4,0,Pluto,slot_0'    
    data_opt['9'] = '4,1,Pluto,slot_1'    

    data_opt['rms_slot_dict'] = dict()  

    data_opt['0,0'] = '0'
    data_opt['0,1'] = '1'
    data_opt['1,0'] = '2'
    data_opt['1,1'] = '3'
    data_opt['2,0'] = '4'
    data_opt['2,1'] = '5'
    data_opt['3,0'] = '6'
    data_opt['3,1'] = '7'
    data_opt['4,0'] = '8'
    data_opt['4,1'] = '9'


#    ***************************************
#    ***************************************
#    domain= [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
#
#    prefs=
'Toby,Bacchus'
'Toby,Hercules'
'Steve,Zeus'
'Steve,Pluto'
'Karen,Athena'
'Karen,Zeus'
'Sarah,Zeus'
'Sarah,Pluto'
'Dave,Athena'
'Dave,Bacchus'
'Jeff,Hercules'
'Jeff,Pluto'
'Fred,Pluto'
'Fred,Athena'
'Suzie,Bacchus'
'Suzie,Hercules'
'Laura,Bacchus'
'Laura,Hercules'
'James,Hercules'
'James,Athena'

#    dorms= ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']
#    dormss= ['0 Zeus', '1 Athena', '2 Hercules', '3 Bacchus', '4 Pluto']
#    slots=
#    [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
#    slotss= ['0 0 Zeus', '1 0 Zeus', '2 1 Athena', '3 1 Athena', '4 2 Hercules', '5 2 Hercules', '6 3 Bacchus', '7 3 Bacchus', '8 4 Pluto', '9 4 Pluto']
#    ***************************************
#    -->bestr= [5, 1, 0, 6, 9, 2, 3, 7, 4, 8] 16
#    -->bestr= [6, 5, 2, 3, 7, 9, 8, 4, 1, 0] 15
#    -->bestr= [9, 1, 7, 4, 2, 0, 8, 6, 5, 3] 14
#    -->bestr= [5, 0, 4, 1, 2, 8, 3, 7, 9, 6] 12
#    -->bestr= [3, 8, 2, 0, 6, 4, 9, 7, 1, 5] 8
#    -->bestr= [7, 1, 0, 3, 2, 9, 8, 4, 6, 5] 6
#    random_optimize dorm_cost result= [7, 1, 0, 3, 2, 9, 8, 4, 6, 5] score= 6
#    ***************************************
#    i= 0 stud -> Toby -> pref -> ('Bacchus', 'Hercules') ; x= 7 slots[x]= 3 -> room -> Bacchus
#    i= 1 stud -> Steve -> pref -> ('Zeus', 'Pluto') ; x= 1 slots[x]= 0 -> room -> Zeus
#    i= 2 stud -> Karen -> pref -> ('Athena', 'Zeus') ; x= 0 slots[x]= 0 -> room -> Zeus
#    i= 3 stud -> Sarah -> pref -> ('Zeus', 'Pluto') ; x= 3 slots[x]= 1 -> room -> Athena
#    i= 4 stud -> Dave -> pref -> ('Athena', 'Bacchus') ; x= 2 slots[x]= 1 -> room -> Athena
#    i= 5 stud -> Jeff -> pref -> ('Hercules', 'Pluto') ; x= 9 slots[x]= 4 -> room -> Pluto
#    i= 6 stud -> Fred -> pref -> ('Pluto', 'Athena') ; x= 8 slots[x]= 4 -> room -> Pluto
#    i= 7 stud -> Suzie -> pref -> ('Bacchus', 'Hercules') ; x= 4 slots[x]= 2 -> room -> Hercules
#    i= 8 stud -> Laura -> pref -> ('Bacchus', 'Hercules') ; x= 6 slots[x]= 3 -> room -> Bacchus
#    i= 9 stud -> James -> pref -> ('Hercules', 'Athena') ; x= 5 slots[x]= 2 -> room -> Hercules
#---------------


    # Двухместные комнаты
    dorms = ['Zeus','Athena','Hercules','Bacchus','Pluto']
    dormss = ['0 Zeus','1 Athena','2 Hercules','3 Bacchus','4 Pluto']

    # Люди и два пожелания у каждого (основное, второстепенное)
    prefs = [('Toby', ('Bacchus', 'Hercules')),
        ('Steve', ('Zeus', 'Pluto')),
        ('Karen', ('Athena', 'Zeus')),
        ('Sarah', ('Zeus', 'Pluto')),
        ('Dave', ('Athena', 'Bacchus')), 
        ('Jeff', ('Hercules', 'Pluto')), 
        ('Fred', ('Pluto', 'Athena')), 
        ('Suzie', ('Bacchus', 'Hercules')), 
        ('Laura', ('Bacchus', 'Hercules')), 
        ('James', ('Hercules', 'Athena'))]

    #  список отсеков, т.е. первые 2 места - 0 отсек и т.д.
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    slotss = ['0 0 Zeus', '1 0 Zeus', '2 1 Athena', '3 1 Athena', '4 2 Hercules', '5 2 Hercules', '6 3 Bacchus', '7 3 Bacchus', '8 4 Pluto', '9 4 Pluto']

    # [9, 8, 7, 6,..., 1]
    #domain = [i for i in xrange(9, 0, -1)]
    domain = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

    print 'domain=',domain

    print 'prefs='
    pprint (prefs)

    print 'dorms=',dorms
    print 'dormss=',dormss

    print 'slots='
    pprint (slots)

    print 'slotss=',slotss

    #i = 0
    #for pr in prefs:
    #    print i,pr[i]
    #    i += 1

    print '***************************************'
    result, score = random_opt(domain, dorm_cost_)
    print 'random_optimize dorm_cost result=',result, 'score=',score

    print '***************************************'
    i = 0
    for x in result:
        dorm = dorms[slots[int(x)]]
        pref = prefs[i][1]
        #print i,int(x), '->', slots[int(x)],'->', prefs[i][0], pref, '->', dorm
        print 'i=',i,'stud ->', prefs[i][0],'-> pref ->', pref , '; x=', int(x), 'slots[x]=',slots[int(x)],'-> room ->', dorm; 
        i += 1

    print "---------------"
