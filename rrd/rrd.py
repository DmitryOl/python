#!/usr/bin/env python3
import rrdtool

rrdtool.graph(
   "/home/dmitry/py/rand.png", # поть по которому создаем рисунок
   "--imgformat", "PNG", # формат рисунка
   "--width", "881", # Ширина
   "--height", "331", # высота
   "--end", "now", # конец графика "сейчас"
   "--start", "end-86400", # начало графика "сейчас - 60*60*24 = день назад"
   "--title", "\'rand graph AREA, 1 ~ 100\'", # шапка - название графика
   "DEF:test=/home/dmitry/py/RRD/rand.rrd:DS:AVERAGE", 
   # DEF:имя переменной="путь где БД":имяDS:функция консолидации
   "CDEF:c=test,20,LT,test,UNKN,IF", # если < 20 то рисуем красным иначе нет
   "CDEF:w=test,20,GE,test,UNKN,IF", # если > 20 то рисуем желтым иначе нет
   "CDEF:n=test,40,GE,test,UNKN,IF", # если > 40 то рисуем зеленым иначе нет
   "CDEF:lw=test,60,GE,test,UNKN,IF", # если > 60 то рисуем светло-синим иначе нет
   "CDEF:lc=test,80,GE,test,UNKN,IF", # если > 80 то рисуем синим иначе нет
    #Зависим от положения больше меньше и положения разукрашки
    'AREA:c#FF0000:\"CRIT\"',
    'AREA:w#FFFF00:\"WARN\"',
    'AREA:n#00FF00:\"OK\"', 
    'AREA:lw#819FF7:\"LWARN\"', 
    'AREA:lc#0040FF:\"LCRIT\"'
    # "AREA:test#00FF00:Up times(%)",
    )
#idat1,UN,0,idat1,IF (замена неопределенного значения на 0)

#1day = 86400

# import cgi
# import html, sys, codecs
# 
# fname = '/home/dmitry/temper/RRD/rand.rrd'
# # period = day

# result = rrdtool.graph('/home/dmitry/temper/RRDimg/rand.png')



# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# print("Content-Type: text/html\n")
# print("""<!DOCTYPE HTML>
#     <html>
#     <head>
#     <meta charset="utf-8">
#     <title> RRD python </title>
#     </head>
#     <body>""") 

# print("<h1>RRD в Python!</h1>")

# print("""</body>
# </html>""")
