#!/usr/bin/env python3
import rrdtool
import os.path
from time import time

rrdDir = "/home/dmitry/py/RRD/"
rrdName = "rand"
rrdPath = rrdDir+rrdName


def rrd_update(name, val):

    if not os.path.exists("%s.rrd" % rrdPath):
        print("rrd {0} have \n".format(name))
        rrd_create(name)

    # rrdtool update имя_ррд.rrd время:значение_DS1[:значение_DS2[:...]]
    rrdtool.update( 
        rrdPath+".rrd", "{0}:{1}".format(time(), val)
    )
    
    print("rrd {0} со значением:{1}:{2} добавлено".format(name,time(),val))



def rrd_create(rname):
    
    if os.path.exists("%s.rrd" % rrdPath):
        print("est takaya")
        return()

    rrdtool.create(
        "{0}{1}.rrd".format(rrdDir, rname) ,
       "--step", "300", 
       "DS:DS:GAUGE:600:U:U",# DS - data sourse : ds name : GAUGE - temp : 600 - time sec : 
       "RRA:LAST:0.5:1:288", # текущие показания сутки (288 - 5 мин)
       # AVERAGE -  среднее из точек данных сохраняется.
       "RRA:AVERAGE:0.5:12:11340",# Средние показания за час 40 суток(40*288)
       "RRA:AVERAGE:0.5:288:1095",# средние за сутки 288 : 3 года 3*365
       "RRA:MAX:0.5:12:11340",# max за час (12*5):40 суток (40*288=11340)
       "RRA:MAX:0.5:288:1095",# max за cутки (288*5):3 года 3*365=1095 
       "RRA:MIN:0.5:12:11340",# min за час: 40 суток
       "RRA:MIN:0.5:288:1095",# min за сутки: 3 года
    )
    
    # RRA:{AVERAGE | MIN | MAX | LAST}:xff:steps:rows
    # RRA - round robin archives : LAST - last data points is used :
    # xff - interval may be made up from *UNKNOWN* :
    # steps - определяет, сколько из этих первичных точек данных используется для 
    #создания консолидированной точки данных, которая затем поступает в архив.
    # rows - defines how many generations of data values are kept

    print ("{0}: CREATING RRD for \"{1}.rrd\"\n".format(rrdDir, rname))


def rrd_graph():
    rrdEnd = str(int(time())) # конец графика "сейчас"
    rrdStart = 86400 # 60*60*24 = 1день 
    rrdLineGraph = "AREA" # отрисовка графика линии(LINE) колонки(AREA)
    rrdTitle = "\'{0} {1}, 1 ~ 100\'".format(rrdName, rrdLineGraph) # название графика
    
    # {название, предел , цвет}
    rrdValue = {"CRIT":[0,"#FF0000"], 
                "WARN":[20,"#FFFF00"], 
                "OK":[40,"#00FF00"],
                "LWARN":[60,"#819FF7"],
                "LCRIT":[80,"#0040FF"]}
    my_list=[]
    for name in rrdValue:
            #"CDEF:CRIT=test,0,GE,test,UNKN,IF"
            my_list.append('CDEF:{0}=test,{1},GE,test,UNKN,IF'.format(name, rrdValue[name][0]))
            # 'AREA:CRIT#FF0000:\"CRIT\"',
            my_list.append('{2}:{0}{1}:\"{0}\"'.format(name, rrdValue[name][1], rrdLineGraph))

    rrdtool.graph(
    "/home/dmitry/py/%s.png"%rrdName, # путь по которому создаем рисунок
    "--imgformat", "PNG", # формат рисунка
    "--width", "881", # Ширина
    "--height", "331", # высота
    "--end", rrdEnd, # конец графика "сейчас"
    "--start", "{} - {}".format(rrdEnd, rrdStart), # начало графика "сейчас - 60*60*24 = день назад"
    "--title", rrdTitle, # шапка - название графика
    'DEF:test={0}{1}.rrd:DS:AVERAGE'.format(rrdDir, rrdName), 
    # DEF:имя переменной="путь где БД":имяDS:функция консолидации
        my_list
        )

# rrd_update(rrdName,15)
rrd_graph()