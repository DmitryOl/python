#!/usr/bin/env python3
import cgi
import html

import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


form = cgi.FieldStorage()
action = form.getfirst("action", "")
text = form.getfirst("text", "")
 

# word = input("Vvedi slovo:")
found = {}
num = 0 


def word_in_text(word):
    found = {} 
    num = 0 
    for letter in word.upper():
        if letter == '\n':
            letter = " новая строка"
        elif letter == ' ':
            letter = " пробел"
        elif letter == '\t':
            letter = " табуляция"
        found.setdefault(letter, 0)
        found[letter] += 1
        num += 1
    return found, num


########### --------- считывание из файла
if action == "startfile":
    txt = "/usr/lib/cgi-bin/py/w.txt"
    #txt = "c:/PyPro/my/w.txt"
    with open(txt, "r", encoding="utf-8") as f: 
        for word in f: 
            text += word
        found, num = word_in_text(text)
######### ------------ ###############

########### --------- считывание из формы
if action == "publish":
    text = form.getfirst("text", "")
    text = html.escape(text)

    found,num = word_in_text(text)
######### ------------ ###############

pub = '''
<form action="/cgi/py/wordsep.py">
    <textarea name="text">Введи свой текст:</textarea>
    <input type="hidden" name="action" value="publish">
    <input type="submit">
</form>
<form action="/cgi/py/wordsep.py">
    <input type="hidden" name="action" value="startfile">
    <input type="submit" value="считать из файла">
</form>
'''

print("Content-Type: text/html\n")
print("""<!DOCTYPE HTML>
    <html>
    <head>
    <meta charset="utf-8">
    <title> подсчет символов </title>
    </head>
    <body>""") 

print("<h1>Подсчет символов в тексте!</h1>")

# data = {(i[0], i[1].replace('\n', '<br>')) for i in text}

print("<p>Ваш текст: {}</p>".format(text.replace('\n' , '<br>')))


#print("<p>TEXT_1: {}</p>".format(text1))
#print("<p>TEXT_2: {}</p>".format(text2))

print("{}".format(pub))
for k, v in sorted(found.items()):
    print(' <b>{k} : {v}</b> ,'.format(k=k,v=v))
print('<br><b>"{}": количество символов</b>'.format(num))

print("""</body>
</html>""")
