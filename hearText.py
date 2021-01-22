
from gtts import gTTS 
import time
import playsound
import speech_recognition as sr
import sqlite3
# import Os module to start the audio file
import os 
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QVBoxLayout, QHBoxLayout, QHeaderView,QTableWidget

#conn = sqlite3.connect('tts.db')
#cursor = conn.cursor()

#cursor.execute ("DROP TABLE  story")
#print("Table dropped... ")
#


#CREATE TABLE story (
#   title TEXT NOT NULL,
#   content TEXT NOT NULL
#);
#conn.commit()
#conn.close()

#
#command1 = """CREATE TABLE IF NOT EXISTS
#story(title TEXT, content TEXT)"""
#cursor.execute(command1)

#print("Table created... ")
#
#conn.commit()
#conn.close()

class Ui_MainWindow(object):

    def messageBox(self,title,message):
        mess=QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setIcon(QMessageBox.Information)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    
    #def speak(text):
        #with open(text, 'r', encoding='utf-8') as filetospeak:
            #s = gTTS(filetospeak.read(), "it")
            #s.save(text[:-4] + ".mp3")
 
        #os.system(text[:-4] + ".mp3")
 

    def insert_data(self):
        conn = sqlite3.connect('tts.db')
        cursor = conn.cursor()

        te = self.title_edit.text()
        pt = self.plainTextEdit.toPlainText()
      

        #cursor.execute("INSERT INTO story (title, content) VALUES (te, pt)");
        cursor.execute('''INSERT INTO story VALUES (?,?)''', (te, pt))
        #cursor.execute(sql,(int(sid), te, pt))

        #cursor.fetchall()
        self.messageBox("Add Story", " Story Saved")
        conn.commit()
        conn.close()
        self.loadData()

        #cursor.execute("SELECT * FROM story WHERE story_id = 1")

    def search(self):
        conn = sqlite3.connect('tts.db')
        cursor = conn.cursor()

        se = self.id_edit.text()
        #cursor.execute('''SELECT * FROM story  ''' )
        cursor.execute("SELECT * FROM story WHERE title=?", [se])
        col = cursor.fetchone()

        title = col[0]
        con = col[1]

        self.title_edit.setText(title)
        self.plainTextEdit.appendPlainText(con)

        #conn.commit()
        #conn.close()


    #def loadtext(self):
        #f = open("The Shepherd Boy and the Wolf.txt", "r")
        #s=(f.read())

        #print(s)

        #self.plainTextEdit.appendPlainText(s)


    
    def listen(self):
        s=self.plainTextEdit.toPlainText()   

        #language = 'en'
        tts = gTTS(text= s, lang='en') 
        filename = 'voice.mp3'
        tts.save(filename) 

        # Play the converted file 
        #os.system("start voice.mp3") 
        playsound.playsound(filename)
        self.loadData()


    def loadData(self):
       
        row = 0
       
        conn = sqlite3.connect('tts.db')
        cursor = conn.cursor()
            
        cursor.execute("SELECT * FROM story ORDER BY title ASC" )
        result = cursor.fetchall()
            
        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                  
    
    def cell_click(self,columnCount,rowCount):

        
        conn = sqlite3.connect('tts.db')
        cursor = conn.cursor()

        item = self.tableWidget.selectedItems()
        i = (item[0].text())


        if rowCount != (0):
            return

        else:
            cursor.execute ("SELECT * from story WHERE title=?", [i] )
            col = cursor.fetchone()
            #print (col)           
            title = col[0]
            story = col[1]

        self.title_edit.setText(title)
        self.plainTextEdit.setPlainText(story)
          

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(840, 580)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 120, 551, 241))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet("background-color: qlineargradient(\
            spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 \
            rgba(255, 255, 255, 255));color: rgb(87, 255, 208);")
        self.plainTextEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.plainTextEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.plainTextEdit.setObjectName("plainTextEdit")


        #TABLE
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(610, 120, 205, 270))
        self.tableWidget.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        #self.tableWidget.setRowCount(100)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.loadData()
        self.tableWidget.cellClicked.connect(self.cell_click)
        #self.tableWidget.cellClicked.connect(self.cell_click)
        
        #BACKGROUND LABEL
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(QtCore.QRect(0, 0, 840, 580))
        self.background_label.setText("")
        self.background_label.setPixmap(QtGui.QPixmap("background.jpg"))
        self.background_label.setScaledContents(True)
        self.background_label.setObjectName("background_label")
        
        #HEADER FRAME
        self.header_frame = QtWidgets.QFrame(self.centralwidget)
        self.header_frame.setGeometry(QtCore.QRect(10, 10, 621, 80))
        self.header_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        
        #HEADER LABEL (HEAR YOUR TEXT)
        self.hear_label = QtWidgets.QLabel(self.header_frame)
        self.hear_label.setGeometry(QtCore.QRect(130, 30, 411, 21))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.hear_label.setFont(font)
        self.hear_label.setStyleSheet("color: rgb(87, 255, 208);")
        self.hear_label.setObjectName("hear_label")

        #ENTER YOUR TEXT BELOW LABEL
        self.enter_text_label = QtWidgets.QLabel(self.centralwidget)
        self.enter_text_label.setGeometry(QtCore.QRect(150, 100, 371, 21))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        self.enter_text_label.setFont(font)
        self.enter_text_label.setStyleSheet("color: rgb(87, 255, 208);")
        self.enter_text_label.setObjectName("enter_text_label")
        
        
        #LISTEN BUTTON
        self.listen_btn = QtWidgets.QPushButton(self.centralwidget)
        self.listen_btn.setGeometry(QtCore.QRect(50, 380, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.listen_btn.setFont(font)
        self.listen_btn.setStyleSheet("background-color: qlineargradient(spread:pad,\
         x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.listen_btn.setObjectName("listen_btn")
        self.listen_btn.clicked.connect(self.listen)

        #SAVE BUTTON
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(50, 430, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.save_btn.setFont(font)
        self.save_btn.setStyleSheet("background-color: qlineargradient(spread:pad,\
         x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.insert_data)
        
        
        #CLEAR BUTTON
        self.clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_btn.setGeometry(QtCore.QRect(240, 380, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.clear_btn.setFont(font)
        self.clear_btn.setStyleSheet("background-color: qlineargradient(spread:pad,\
            x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(lambda:self.plainTextEdit.clear())

        #LOAD TEXT BUTTON
        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setGeometry(QtCore.QRect(240, 430, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.load_btn.setFont(font)
        self.load_btn.setStyleSheet("background-color: qlineargradient(spread:pad,\
            x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.load_btn.setObjectName("load_btn")
        #self.load_btn.clicked.connect(self.loadtext)
        self.load_btn.clicked.connect(self.search)

        #EXIT BUTTON
        self.exit_btn = QtWidgets.QPushButton(self.centralwidget)
        self.exit_btn.setGeometry(QtCore.QRect(430, 380, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Gunship Expanded")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.exit_btn.setFont(font)
        self.exit_btn.setStyleSheet("background-color: qlineargradient(spread:pad, \
            x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 0, 0, 0), stop:1 rgba(255, 255, 255, 255));")
        self.exit_btn.setObjectName("exit_btn")
        self.exit_btn.clicked.connect(lambda:sys.exit())


        self.title_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.title_edit.setGeometry(QtCore.QRect(430, 430, 200, 41))
        self.title_edit.setText("")
        self.title_edit.setObjectName("title_edit")

        self.id_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.id_edit.setGeometry(QtCore.QRect(430, 480, 100, 41))
        self.id_edit.setText("")
        self.id_edit.setObjectName("id_edit")
        
        #font = QtGui.QFont()
        #font.setPointSize(12)
        #self.title#_edit.setFont(font)
        
        self.background_label.raise_()
        self.plainTextEdit.raise_()
        self.header_frame.raise_()
        self.listen_btn.raise_()
        self.enter_text_label.raise_()
        self.clear_btn.raise_()
        self.load_btn.raise_()
        self.exit_btn.raise_()
        self.save_btn.raise_()
        self.title_edit.raise_()
        self.id_edit.raise_()
        self.tableWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HEAR YOUR TEXT APP"))
        self.hear_label.setText(_translate("MainWindow", "HEAR YOUR TEXT"))
        self.listen_btn.setText(_translate("MainWindow", "Listen"))
        self.enter_text_label.setText(_translate("MainWindow", "Enter Text Below:"))
        self.clear_btn.setText(_translate("MainWindow", "CLEAR"))
        self.load_btn.setText(_translate("MainWindow", "LOAD"))
        self.exit_btn.setText(_translate("MainWindow", "EXIT"))
        self.save_btn.setText(_translate("MainWindow", "SAVE"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Title"))
        
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Story"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
