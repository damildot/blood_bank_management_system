from PyQt5.QtWidgets import*
import sqlite3 as sl
from suds.client import Client
import sys
import re
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sqlite3
import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import date
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("first_1.ui",self)
        self.dont.setHidden(True)
        self.trya.setHidden(True)
        self.sign_up.clicked.connect(self.gotoscreen2)
        self.sign_in.clicked.connect(self.login)
    
    def login(self):            
        self.i_num =  int(self.tc_edit.text())
        password =  self.psw_edit.text()
        if len(self.tc_edit.text())==0 or len(password)==0 :#databasede olmama durumu da kontrol edilebilir
            self.dont.setHidden(False)
            self.trya.setHidden(False)
            return False        
        else:
            q1=("""SELECT Password FROM Person WHERE i_num= ? """)
            cur.execute(q1,(self.i_num,))
            res=cur.fetchone()
            if res[0] == password:
                widget.setCurrentIndex(widget.currentIndex()+2)
                screen3.profile("main")
                return True
        conn.commit()
    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class Screen2(QDialog):
    def __init__(self):
        super(Screen2,self).__init__()
        loadUi("signupwidget.ui",self)
        self.fillall.setHidden(True)
        self.disease.setHidden(True)
        self.l_donation.setHidden(True)
        self.disease_is=None
        self.signinup.clicked.connect(self.data_filled_complete)
        self.returnto.clicked.connect(self.turnmain) 
        self.birthdate.dateTimeChanged.connect(self.blood_donated)        
        self.radonation.toggled.connect(self.blood_donated)
    def turnmain(self):
        #burda ilk sayfadaki verileri silme kodu eklenecek
        widget.setCurrentIndex(widget.currentIndex()-1)
    def data_filled_complete(self):
        self.blood_donated()
        try:
            if self.tc_validation()==True:
                if self.phone_validation()==True:
                    if self.mail_validate()==True:
                        if self.val_disease()==True or self.val_disease2()==True:
                            if self.pwd_validation()==True:
                                self.fill_label()
                                print(self.birthdate.date().toString())
                                widget.setCurrentIndex(widget.currentIndex()+1)  
                            else:
                                self.fillall.setText("Please fill the password column correctly.")
                                self.fillall.setHidden(False)
                        else:
                            self.fillall.setText("Please fill the disease column correctly.")
                            self.fillall.setHidden(False)
                    else:
                        self.fillall.setText("Please fill the mail column correctly.")
                        self.fillall.setHidden(False)
                else:
                    self.fillall.setText("Please fill the phone column correctly.")
                    self.fillall.setHidden(False)
            else:
                self.fillall.setText("Please fill the name, surname, identity and birthdate column correctly.")
                self.fillall.setHidden(False)
        except:
            self.fillall.setText("Please fill the columns correctly.")
            self.fillall.setHidden(False)
#disease validation
    def val_disease(self):
        if self.radihave.isChecked():
            self.fillall.setHidden(False)
            if len(self.disease.text())!=0:
                self.disease_is=self.disease.text()
                return True
            else:return False
        else:
            return False
    
    def val_disease2(self):
        if self.radiob.isChecked():
            self.disease_is="Any"
            return True
        else:
            return False
#blood_donated?
    def blood_donated(self):
        self.possible_date=self.birthdate.date().addYears(18)
        self.l_donation.setMinimumDate(self.possible_date)
        if self.radonation.isChecked():
            self.l_donation.setHidden(False)
#mail validation
    def mail_validate(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'
        email=self.mail.text()
        if (re.fullmatch(regex, email)):
            return True
        else:
            return False 
#phone_validation
    def phone_validation(self):
        number=self.phone.text()
        if len(number)==11:
            value= number[0]=="0" and number[1]=="5" and number.isdigit()
            return value
        else:
            return False
#tc validation
    def tc_validation(self):
        self.TCURL="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
        client=Client(self.TCURL)
        year=self.birthdate.date().year
        args={"TCKimlikNo":self.inum.text(),"Ad":self.name.text(),"Soyad":self.surname.text(),"DogumYili": year}
        return client.service.TCKimlikNoDogrula(**args)==True
#pwd validation
    def pwd_validation(self):
        pwd=len(self.password.text())>4 and self.password.text()==self.password_again.text()
        return pwd==True
#is data filled validation

    def fill_label(self):
        self.data_liste = [self.name.text(), self.surname.text(), int(self.inum.text()), int(self.phone.text()), self.gender.currentText(),self.mail.text(),self.birthdate.date().toString(),self.l_donation.date().toString(),self.b_group.currentText(),self.weight.value(),self.disease_is,self.adress.currentText(),self.password.text()]
        a=tuple(self.data_liste)
        with conn:
            q2=("""INSERT INTO Person VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""")
            cur.execute(q2,a)
            conn.commit()

class Screen3(QDialog,QCalendarWidget):
    def __init__(self):
        super(Screen3,self).__init__()
        loadUi("page3.ui",self)
        self.cuser.clicked.connect(self.gotoscreenmain)
        self.donate.clicked.connect(self.donated)
        #self.update.clicked.connect()
    def profile(self,where):
        self.where=where
        if self.where=="main":
            a=int(mainwindow.tc_edit.text())
        elif self.where=="second":
            a=int(screen2.inum.text())
        cur.execute("SELECT * FROM Person WHERE i_num=?", (a,))
        rows = cur.fetchone()
        self.namedb=rows[0]
        self.surnamedb=rows[1]
        self.i_numdb=rows[2]
        self.teldb=rows[3]
        self.genderdb=rows[4]
        self.maildb=rows[5]
        self.bdatedb=rows[6]
        self.l_donatedb=rows[7]
        self.b_groupdb=rows[8]
        self.weightdb=rows[9]
        self.diseasedb=rows[10]
        self.adressdb=rows[11]
        self.passworddb=rows[12]
        self.name.setText(self.namedb)
        self.surname.setText(self.surnamedb)
        self.inum.setText(str(self.i_numdb))
        self.phone.setText(str(self.teldb))
        self.gender.setText(self.genderdb)
        self.mail.setText(self.maildb)
        self.bdate.setText(self.bdatedb)
        self.l_donation.setText(self.l_donatedb)
        self.b_group.setText(self.b_groupdb)
        self.weight.setValue(self.weightdb)
        self.disease.setText(self.diseasedb)
        self.adress.setCurrentText(self.adressdb)
    

    def donated(self):
        #burda screen2den aldım ama dbden çekilenler eşitlenecek
        if screen2.weight.value()>=50:
            if (QDate.currentDate()>screen2.birthdate.date().addYears(18)):
                self.calendarw()
            else:
                self.label_check.setText("Your age is not suitable for blood donation!") 
        else:
            self.label_check.setText("Your weight is not suitable for blood donation!")
    def calendarw(self):
        self.pos_donation=QDate.currentDate()
        gender=screen2.gender.currentText()
        if gender == "Male":
            if QDate.currentDate()>screen2.l_donation.date().addDays(90) or screen2.birthdate.date().addYears(18)==screen2.l_donation.date():
                self.pos_donation=QDate.currentDate()
                screen2.l_donation.setDate(self.pos_donation)
                self.label_check.setText("Your donation saved successfully")            
            else:
                self.label_check.setText("You can check the date you can donate blood from the calendar on the home page.")
                self.pos_donation=screen2.l_donation.date().addDays(90)
        else:
            if QDate.currentDate()>screen2.l_donation.date().addDays(120) or screen2.birthdate.date().addYears(18)==screen2.l_donation.date():
                self.pos_donation=QDate.currentDate()
                screen2.l_donation.setDate(self.pos_donation)
                self.label_check.setText("Your donation saved successfully")
            else:
                self.label_check.setText("You can check the date you can donate blood from the calendar on the home page.")
                self.pos_donation=screen2.l_donation.date().addDays(120)
        self.calendarWidget.setSelectedDate(self.pos_donation)

    def gotoscreenmain(self):
        widget.setCurrentIndex(widget.currentIndex()-2)
    #bilgileri değiştirirken kullanılabilir
    def gotoscreen2(self):        
        widget.setCurrentIndex(widget.currentIndex()-1) 
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()

mainwindow=MainWindow() 
screen2=Screen2() #sign_ıp
screen3=Screen3()   #profile
widget.addWidget(mainwindow)
widget.addWidget(screen2)
widget.addWidget(screen3)
conn=sl.connect("database.db")
cur=conn.cursor()
widget.setFixedHeight(750)
widget.setFixedWidth(1000)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")