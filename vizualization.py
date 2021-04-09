import json
import pandas as pd
import matplotlib.pyplot as plt
import sys
from functools import reduce

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

tl  = dict()
tl['shortSchoolName'] = 'Iskolák'
tl['location'] = 'Települések'

colist=['moccasin','orange','red','green','purple','brown',
'plum','palevioletred','grey','slateblue','salmon','tomato',
'peru','skyblue','orchid','turquoise']

COLOR = 'black'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['axes.facecolor'] = 'lavender'
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR
plt.rcParams['figure.facecolor'] = 'lavender'

file = open('grades2015.json')
ls = json.load(file)
file.close()

locations = set()
schools = set()
ids = set()
county = set()
jsList = []
loc = ["Urban", "Rural"]
urbanLoc = set()
ruralLoc = set()
urban = []
rural = []
hun = []

#Lehet rovidebben is
for s in ls['results']:
    jsList.append(s)
for s in jsList:
    locations.add(s['location'])
    schools.add(s['schoolName'])
    if s['nationality'] == "Maghiara":
        county.add(s['county'])
        ids.add(s['name'])
        hun.append(s)
    if s['medium'] == loc[0]:
        urbanLoc.add(s['location'])
        urban.append(s)
    if s['medium'] == loc[1]:
        ruralLoc.add(s['location'])
        rural.append(s)

locations = sorted(locations)
schools = sorted(schools)
ids = sorted(ids)
county = sorted(county)
urbanLoc = sorted(urbanLoc)
ruralLoc = sorted(ruralLoc)
ids = map(str, ids) 

topics = [  "Válassz opciót!",
            "Diákok eloszlása nemzetiségeik alapján (Pie chart)", #1
            "A diákok megyénkénti részvételi eloszlálsa nemzetiségekre lebontva (Pie chart)", #2
            "Magyar diákok város/falu részvételi aránya  (Pie chart)", #3
            "Magyar diákok város/falu részvételi aránya megyékre lebontva  (Pie chart)", #4
            "Az átmenő valamint nem átmenő diákok aránya (Pie chart)", #5
            "Az átmenő valamint nem átmenő magyar diákok aránya (Pie chart)", #6
            "Az átmenő valamint nem átmenő magyar diákok aránya(falu/város) (Pie chart)", #7 
            "Magyar diákok matematika átlaga illetve román diákok matematika átlaga (Bar chart)", #8
            "Az első 20 legnagyobb átlaggal rendelkező iskola megyénként(város) (Bar chart)", #9
            "Az első 20 legnagyobb átlaggal rendelkező iskola megyénként(falu) (Bar chart)", #10
            "Az első 20 legnagyobb átlaggal rendelkező magyar diák megyénként(város) (Bar chart)", #11
            "Az első 20 legnagyobb átlaggal rendelkező magyar diák megyénként(falu) (Bar chart)", #12
            "Az első 20 legnagyobb átlaggal rendelkező diák iskolánként (Bar chart)", #13
            "Adott magyar diák jegyei (Bar chart)" #14 
            ]

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        self.setFixedSize(1500,750)
        self.setWindowTitle("Képességvizsga eredményeinek vizualizálása")

        self.canvas = FigureCanvas(self.figure)
        
        self.toolbar = NavigationToolbar(self.canvas, self)

        font = QFont()
        font.setPointSize(font.pointSize() + 3)
        
        self.cb = QComboBox(self)
        self.cb.addItems(topics)
        self.cb.setFont(font)
        self.cb.currentTextChanged.connect(self.selectionChange)

        self.cbTopic2 = QComboBox(self)
        self.cbTopic2.addItems(county)
        self.cbTopic2.setFont(font)
        self.cbTopic2.setVisible(False)
        self.cbTopic2.currentTextChanged.connect(self.selectionChange)

        self.cbTopic7 = QComboBox(self)
        self.cbTopic7.addItems(loc)
        self.cbTopic7.setFont(font)
        self.cbTopic7.setVisible(False)
        self.cbTopic7.currentTextChanged.connect(self.selectionChange)

        self.cbSch = QComboBox(self)
        self.cbSch.addItems(schools)
        self.cbSch.setFont(font)
        self.cbSch.setVisible(False)
        self.cbSch.currentTextChanged.connect(self.selectionChange)

        self.cbId = QComboBox(self)
        self.cbId.addItems(ids)
        self.cbId.setFont(font)
        self.cbId.setVisible(False)
        self.cbId.currentTextChanged.connect(self.selectionChange)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.cb)
        layout.addWidget(self.cbSch)
        layout.addWidget(self.cbId)
        layout.addWidget(self.cbTopic2)
        layout.addWidget(self.cbTopic7)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def selectionChange(self):
        self.cbId.setVisible(False)
        self.cbSch.setVisible(False)
        self.cbTopic2.setVisible(False)
        self.cbTopic7.setVisible(False)
        text = self.cb.currentText()

        if text == topics[1]:
            self.topic1()
        if text == topics[2]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic2(tmp)
        if text == topics[3]:
            self.topic3()
        if text == topics[4]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic4(tmp)
        if text == topics[5]:
            self.topic5()
        if text == topics[6]:
            self.topic6()
        if text == topics[7]:
            self.cbTopic7.setVisible(True)
            tmp = self.cbTopic7.currentText()
            self.topic7(tmp)
        if text == topics[8]:
            self.topic8()
        if text == topics[9]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic9_10(urban, tmp, topics[9])
        if text == topics[10]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic9_10(rural, tmp, topics[10])
        if text == topics[11]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic11_12(urban, tmp, topics[11])
        if text == topics[12]:
            self.cbTopic2.setVisible(True)
            tmp = self.cbTopic2.currentText()
            self.topic11_12(rural, tmp, topics[12])
        if text == topics[13]:
            self.cbSch.setVisible(True)
            tmp = self.cbSch.currentText()
            self.topic13(tmp)
        if text == topics[14]:
            self.cbId.setVisible(True)
            tmp = self.cbId.currentText()
            self.currentStudent(tmp)

    def topic1(self):
        self.figure.clear()

        count = dict()
        for school in jsList:
            if school['nationality'] in count:
                count[school['nationality']] += 1
            else:
                 count[school['nationality']] = 1
        
        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=0, colors=['palevioletred', 'mediumpurple'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True},textprops={
            'fontsize':12,
            'fontfamily': "Comic Sans MS"
        })
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title="Nemzetiségenkénti eloszlás",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[1], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic2(self, cty):
        self.figure.clear()

        count = dict()
        for school in jsList:
            if school['county'] == cty:
                if school['nationality'] in count:
                    count[school['nationality']] += 1
                else:
                    count[school['nationality']] = 1

        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=0, colors=['palevioletred', 'mediumpurple'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) 
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title=cty + " megye",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[2], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic3(self):
        self.figure.clear()

        count = dict()
        for school in jsList:
            if school['nationality'] == "Maghiara":
                if school['medium'] in count:
                    count[school['medium']] += 1
                else:
                     count[school['medium']] = 1

        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=0, colors=['palevioletred', 'mediumpurple'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) #'style' : 'Comic Sans MS'
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title="Város/falu részvételi arány",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[3], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic4(self, cty):
        self.figure.clear()

        count = dict()
        for school in jsList:
            if school['nationality'] == "Maghiara":
                if school['county'] == cty:
                    if school['medium'] in count:
                        count[school['medium']] += 1
                    else:
                        count[school['medium']] = 1

        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=90, colors=['palevioletred', 'mediumpurple'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) #'style' : 'Comic Sans MS'
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title=cty + " megye",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[4], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic5(self):
        self.figure.clear()

        count = dict()
        count = dict()
        count['Átment'] = 0
        count['Nem ment át'] = 0

        for school in jsList:
            if school['native lang'] != "":
                if school['mathematics'] < 5 or school['romanian'] < 5 or school['native lang'] < 5 or school['avg'] < 5:
                    count['Nem ment át'] += 1
                else:
                    count['Átment'] += 1
            else:
                if school['mathematics'] < 5 or school['romanian'] < 5 or school['avg'] < 5:
                    count['Nem ment át'] += 1
                else:
                    count['Átment'] += 1
        
        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=90, colors=['g','r'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) #'style' : 'Comic Sans MS'
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.110, right=0.735)

        ax.legend(
          title="Átmenési arány",
          loc="center left",
          labels = ['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[5], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic6(self):
        self.figure.clear()

        count = dict()
        count['Átment'] = 0
        count['Nem ment át'] = 0

        for school in jsList:
            if school['nationality'] == "Maghiara":
                if school['native lang'] != "":
                    if school['mathematics'] < 5 or school['romanian'] < 5 or school['native lang'] < 5 or school['avg'] < 6:
                        count['Nem ment át'] += 1
                    else:
                        count['Átment'] += 1
                else:
                    if school['mathematics'] < 5 or school['romanian'] < 5 or school['avg'] < 6:
                        count['Nem ment át'] += 1
                    else:
                        count['Átment'] += 1

        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=90, colors=['g','r'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) #'style' : 'Comic Sans MS'
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title="Átment/Nem ment át",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[6], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic7(self, loc):
        self.figure.clear()

        count = dict()
        count['Átment'] = 0
        count['Nem ment át'] = 0

        for school in jsList:
            if school['medium'] == loc:
                if school['nationality'] == "Maghiara":
                    if school['native lang'] != "":
                        if school['mathematics'] < 5 or school['romanian'] < 5 or school['native lang'] < 5 or school['avg'] < 6:
                            count['Nem ment át'] += 1
                        else:
                            count['Átment'] += 1
                    else:
                        if school['mathematics'] < 5 or school['romanian'] < 5 or school['avg'] < 6:
                            count['Nem ment át'] += 1
                        else:
                            count['Átment'] += 1

        ax = self.figure.add_subplot(111)
        wedges, texts, autotexts = ax.pie(count.values(), labels=count.keys(), autopct='%1.1f%%',startangle=90, colors=['g','r'],
        wedgeprops={"edgecolor":"k",'linewidth': 1, 'linestyle': '-', 'antialiased': True}) #'style' : 'Comic Sans MS'
        plt.subplots_adjust(top=0.880, bottom = 0.110, left = 0.220, right=0.735)

        ax.legend(
          title=loc,
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(count.keys(), count.values())],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(1, 0, 0.5, 1))

        ax.axis('equal')
        plt.title(topics[7], {
            'fontsize':15,
            'fontfamily': "Comic Sans MS"
        })
        plt.plot()

        self.canvas.draw()

    def topic8(self):
        self.figure.clear()

        count = dict()
        count['Magyar diákok'] = []
        count['Román diákok'] = []

        for school in jsList:
            if school['nationality'] == "Maghiara":
                count['Magyar diákok'].append(school['mathematics'])
            if school['nationality'] == "Romana":
                count['Román diákok'].append(school['mathematics'])

        cl = ['palevioletred', 'mediumpurple']

        ls = []
        for k,v in count.items():
            ls.append(len(count[k]))
            count[k] = reduce(lambda a, b: a + b, count[k]) / len(count[k])

        ls1 = list(count.keys())
        ls2 = list(count.values())
        
        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(left=0.145, bottom = 0.13, right=0.920, top=0.85)
        for j in range(len(count)):
            ax.barh(ls1[j], ls2[j], edgecolor='black', color=cl[j], lw=2)

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
 
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)
        
        for tick in ax.get_xticklabels():
            tick.set_fontname("Comic Sans MS")
        for tick in ax.get_yticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(11)

        ax.grid(b = True, color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.1)
                
        ax.invert_yaxis()
        ax.set_xlim([1,10])
        
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                    str(round((i.get_width()), 2)),
                    fontsize = 13, fontweight ='bold',
                    color ='maroon')

        plt.title(topics[8], {
                'fontsize':15,
                'fontfamily': "Comic Sans MS"
        })

        ax.legend(
          title="Diákok száma",
          title_fontsize=12,
          loc="center left",
          labels=['%s %d' % (x, y) for x, y in zip(ls1, ls)],
          prop={'size': 11, 'family':"Comic Sans MS"},
          bbox_to_anchor=(0.8, 0, 0.5, 1))

        self.canvas.draw()

    def topic9_10(self, loc, cty, tlt):
        self.figure.clear()

        count = dict()
        for school in loc:
            if school['county'] == cty:
                if school['schoolName'] in count:
                    count[school['schoolName']].append(school['avg'])
                else:
                     count[school['schoolName']] = []

        for k,v in count.items():
            if count[k] != []:
                count[k] = reduce(lambda a, b: a + b, count[k]) / len(count[k])
            else:
                count[k] = 0
        count = { k:v for k,v in count.items() if v != 0 }
        count = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
        count = {k: count[k] for k in list(count)[:20]}

        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(left=0.335, bottom = 0.13, right=0.920, top=0.85)
        ax.barh(list(count.keys()), list(count.values()), edgecolor='black', color='mediumpurple', lw=2)

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
 
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)
        
        for tick in ax.get_xticklabels():
            tick.set_fontname("Comic Sans MS")
        for tick in ax.get_yticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(11)

        ax.grid(b = True, color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.1)
                
        ax.invert_yaxis()
        ax.set_xlim([1,10])
        
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                    str(round((i.get_width()), 2)),
                    fontsize = 10, fontweight ='bold',
                    color ='maroon')

        plt.title(tlt, {
                'fontsize':15,
                'fontfamily': "Comic Sans MS"
        })

        plt.plot()

        self.canvas.draw()

    def topic11_12(self, loc, cty, tlt):
        self.figure.clear()

        students = []
        for school in loc:
            if school['nationality'] == "Maghiara":
                if school["county"] == cty:
                    students.append(school)

        students = sorted(students, key = lambda i: i['avg'], reverse=True)
        students = students[:20]
        names = []
        avgs = []
        for i in students:
            names.append(str(i['name']))
            avgs.append(i['avg'])

        
        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(left=0.180, bottom = 0.13, right=0.920, top=0.85)
        barlist = ax.barh(names, avgs,  edgecolor='black', color='mediumpurple', lw=2)

        for i in range(len(avgs)):
            if avgs[i] < 5:
               barlist[i].set_color('r')
               barlist[i].set_edgecolor('k')
            else:
               barlist[i].set_color('g')
               barlist[i].set_edgecolor('k')

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
 
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)
        
        for tick in ax.get_xticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(11)
        for tick in ax.get_yticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(13)

        ax.grid(b = True, color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.1)
                
        ax.invert_yaxis()
        ax.set_xlim([1,10])
        
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                    str(round((i.get_width()), 2)),
                    fontsize = 12, fontweight ='bold',
                    color ='maroon')

        plt.title(tlt, {
                'fontsize':15,
                'fontfamily': "Comic Sans MS"
        })            
        plt.plot()

        self.canvas.draw()

    def topic13(self, sch):
        self.figure.clear()

        students = []
        for school in jsList:
            if school["schoolName"] == sch:
                students.append(school)

        students = sorted(students, key = lambda i: i['avg'], reverse=True)
        students = students[:20]
        names = []
        avgs = []
        for i in students:
            names.append(str(i['name']))
            avgs.append(i['avg'])

        
        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(left=0.180, bottom = 0.13, right=0.920, top=0.85)
        barlist = ax.barh(names, avgs,  edgecolor='black', color='mediumpurple', lw=2)

        for i in range(len(avgs)):
            if avgs[i] < 5:
               barlist[i].set_color('r')
               barlist[i].set_edgecolor('k')
            else:
               barlist[i].set_color('g')
               barlist[i].set_edgecolor('k')

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
 
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)
        
        for tick in ax.get_xticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(11)
        for tick in ax.get_yticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(13)

        ax.grid(b = True, color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.1)
                
        ax.invert_yaxis()
        ax.set_xlim([1,10])
        
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                    str(round((i.get_width()), 2)),
                    fontsize = 12, fontweight ='bold',
                    color ='maroon')

        plt.title(sch, {
                'fontsize':15,
                'fontfamily': "Comic Sans MS"
        })            
        plt.plot()

        self.canvas.draw()

    def currentStudent(self, id):
        self.figure.clear()

        lst = []
        sbj = ['Romanian', 'Mathematics', 'Hungarian', 'Average']
    
        m = next(d for d in hun if str(d['name']) == id)

        lst.append(m['romanian'])
        lst.append(m['mathematics'])
        lst.append(m['native lang'])
        lst.append(m['avg'])

        ax = self.figure.add_subplot(111)
        plt.subplots_adjust(left=0.110, bottom = 0.260, right=0.665, top=0.815)
        barlist = ax.barh(sbj, lst, edgecolor='black', color='mediumpurple', lw=2)

        passed = True
        for i in range(len(lst) - 1):
            if lst[i] < 5:
                barlist[i].set_color('r')
                barlist[i].set_edgecolor('k')
                passed = False
            else:
                barlist[i].set_color('g')
                barlist[i].set_edgecolor('k')
        if passed == True:
            barlist[3].set_color('g')
            barlist[3].set_edgecolor('k')
        else:
            barlist[3].set_color('r')
            barlist[3].set_edgecolor('k')

        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
 
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        
        ax.xaxis.set_tick_params(pad = 5)
        ax.yaxis.set_tick_params(pad = 10)
        
        for tick in ax.get_xticklabels():
            tick.set_fontname("Comic Sans MS")
        for tick in ax.get_yticklabels():
            tick.set_fontname("Comic Sans MS")
            tick.set_fontsize(11)

        ax.grid(b = True, color ='grey',
                linestyle ='-.', linewidth = 0.5,
                alpha = 0.1)
                
        ax.invert_yaxis()
        ax.set_xlim([1,10])
        
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                    str(round((i.get_width()), 2)),
                    fontsize = 12, fontweight ='bold',
                    color ='maroon')

        plt.title(m['schoolName'] + " tanulója", {
                'fontsize':15,
                'fontfamily': "Comic Sans MS"
        })            
        plt.plot()            
        plt.plot()

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())