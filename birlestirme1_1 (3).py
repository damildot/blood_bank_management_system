from PyQt5.QtWidgets import*
import sqlite3 as sl
from suds.client import Client
import sys
import re
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sqlite3
import datetime
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from datetime import date
from dateutil.relativedelta import relativedelta
from resources import*
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("first_1.ui",self)
        self.dont.setHidden(True)
        self.trya.setHidden(True)
        self.sign_up.clicked.connect(self.gotoscreen2)
        self.sign_in.clicked.connect(self.login)
    
    def login(self):
        #databasede olmama durumu da kontrol edilebilir
        try:
            i_num =  int(self.tc_edit.text())
            password =  self.psw_edit.text()
            q1=("""SELECT Password FROM Person WHERE i_num= ? """)
            cur.execute(q1,(i_num,))
            res=cur.fetchone()
            if res[0] == password:
                widget.setCurrentIndex(widget.currentIndex()+2)
                screen3.profile("main")
                return True
            elif len(self.tc_edit.text())==0 or len(password)==0 :
                self.dont.setHidden(False)
                self.trya.setHidden(False)
                return False
            conn.commit()
        except:
            self.dont.setHidden(False)
            self.trya.setHidden(False)
        self.tc_edit.clear()
        self.psw_edit.clear()
    def gotoscreen2(self):
        widget.setCurrentIndex(widget.currentIndex()+1)        
        self.tc_edit.clear()
        self.psw_edit.clear()

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
        self.clearing()
        widget.setCurrentIndex(widget.currentIndex()-1)
    def clearing(self):
        self.name.clear()
        self.surname.clear()
        self.inum.clear()
        self.phone.clear()
        self.mail.clear()
        self.disease.clear()
        self.password.clear()
        self.password_again.clear()
        screen2.adress.setCurrentText("NULL")
    def data_filled_complete(self):
        self.blood_donated()
        try:
            if self.tc_validation()==True:
                if self.phone_validation()==True:
                    if self.mail_validate()==True:
                        if self.val_disease()==True or self.val_disease2()==True:
                            if self.pwd_validation()==True:
                                self.fill_label()
                                screen3.profile("second") 
                                widget.setCurrentIndex(widget.currentIndex()+1) 
                                self.clearing()
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
#fill 3rd page
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
        year=self.birthdate.date().toPyDate().year
        args={"TCKimlikNo":self.inum.text(),"Ad":self.name.text(),"Soyad":self.surname.text(),"DogumYili": year}
        return client.service.TCKimlikNoDogrula(**args)==True
#pwd validation
    def pwd_validation(self):
        pwd=len(self.password.text())>4 and self.password.text()==self.password_again.text()
        return pwd==True
#is data filled validation
    def fill_label(self):
        self.data_liste = [self.name.text(), self.surname.text(), int(self.inum.text()), int(self.phone.text()), 
        self.gender.currentText(),self.mail.text(),self.birthdate.date().toPyDate(),self.l_donation.date().toPyDate(),
        self.b_group.currentText(),self.weight.value(),self.disease_is,self.adress.currentText(),self.password.text()]
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
        self.identity=0
        self.show=True
        self.show_stock()
        self.donate.clicked.connect(self.can_donate)
        self.update.clicked.connect(self.update_btn)    
    def profile(self,where):
        self.where=where
        if self.where=="main":
            a=int(mainwindow.tc_edit.text())
        elif self.where=="second":
            a=int(screen2.inum.text())
        else:
            a=self.i_numdb
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
        self.tel=self.phone.text()
        if len(self.tel)==10:
            value= self.tel[0]=="5" and self.tel.isdigit()
            return value
        else:
            return False

    def update_val(self):                   
        self.tel=self.phone.text()
        self.mailv=self.mail.text()
        self.weightv=self.weight.value()
        self.diseasev=self.disease.text()
        self.addressv=self.adress.currentText()
        q3= ''' UPDATE Person
              SET tel = ? ,
                  mail = ? ,
                  Weight = ?,
                  Disease = ? ,
                  Address = ?
              WHERE i_num = ?'''
        self.data_changed=[int(self.tel),self.mailv,self.weightv,self.diseasev,self.addressv,int(self.i_numdb)]
        self.data_changed=tuple(self.data_changed)
        print(self.data_changed)
        with conn:
            cur.execute(q3,self.data_changed)
            conn.commit()
        self.profile(where="third")
    def update_btn(self):
        if self.phone_validation()==True:
            if self.mail_validate()==True:
                    self.update_val()
            else:
                self.mail.setText(self.maildb)
        else:
            self.phone.setText(str(self.teldb))
    def show_stock(self):
        cur.execute("""SELECT Samount FROM Stock""")
        rows=cur.fetchall()
        a,b,c,d,e,f,g,h=rows
        self.apo.display(a[0])
        self.ane.display(b[0])
        self.bpo.display(c[0])
        self.bne.display(d[0])
        self.abpo.display(e[0])
        self.abne.display(f[0])
        self.spo.display(g[0])
        self.sne.display(h[0])

    def can_donate(self):
        self.load_data_table()
        if type(self.bdatedb)==str:
            y=int(self.bdatedb[0:4])
            m=int(self.bdatedb[5:7])
            d=int(self.bdatedb[8:])
            self.bdatedb=datetime.date(y,m,d)
        else:
            pass
        if type(self.l_donatedb)==str:
            y2=int(self.l_donatedb[0:4])
            m2=int(self.l_donatedb[5:7])
            d2=int(self.l_donatedb[8:])
            self.l_donatedb=datetime.date(y2,m2,d2)
        else:
            pass
        if self.weightdb>=50:
            if (date.today()>self.bdatedb+relativedelta(years=18)):
                self.calendarw()
            else:
                self.label_check.setText("Your age is not suitable for blood donation!")
        else:
            self.label_check.setText("Your weight is not suitable for blood donation!")
    def calendarw(self):
        self.pos_donation= date.today()
        if self.genderdb == "Male":
            if date.today()>self.l_donatedb+relativedelta(days=90) or self.bdatedb+relativedelta(years=18)==self.l_donatedb:
                screen2.l_donation.setDate(self.pos_donation)
                q4="""UPDATE Person SET lastDonateBlood = ? WHERE i_num= ?"""
                data=(self.pos_donation,self.i_numdb)
                cur.execute(q4,data)
                self.l_donatedb=str(self.pos_donation)
                self.label_check.setText("Your donation saved successfully")                
                self.l_donation.setText(self.l_donatedb)
                self.donate_fill()
                self.stock(self.b_groupdb)
                self.show=True
                self.load_data_table()
            else:
                self.label_check.setText("You can check the date you can donate blood from the calendar on the home page.")
                self.pos_donation=self.l_donatedb+relativedelta(days=90)
        else:
            if date.today()>self.l_donatedb+relativedelta(days=120) or self.bdatedb+relativedelta(years=18)==self.l_donatedb:
                screen2.l_donation.setDate(self.pos_donation)
                q4="""UPDATE Person SET lastDonateBlood = ? WHERE i_num= ?"""
                data=(self.pos_donation,self.i_numdb)
                cur.execute(q4,data)
                self.l_donatedb=str(self.pos_donation)
                self.label_check.setText("Your donation saved successfully")
                self.l_donation.setText(self.l_donatedb)
                self.donate_fill()
                self.stock(self.b_groupdb)
                self.show=True
                self.load_data_table()
            else:
                self.label_check.setText("You can check the date you can donate blood from the calendar on the home page.")
                self.pos_donation=self.l_donatedb+relativedelta(days=120)
        x=self.pos_donation.strftime("%Y-%m-%d")
        y3=int(x[0:4])
        m3=int(x[5:7])
        d3=int(x[8:])
        self.datenew=QDate(y3, m3, d3)
        self.calendarWidget.setSelectedDate(self.datenew)

    def load_data_table(self):
        if self.show==True:
            cur.execute('''SELECT * FROM Donate''')
            rows = cur.fetchall()
            for row in rows:
                inx = rows.index(row)
                self.tableWidget.insertRow(inx)
                self.tableWidget.setItem(inx, 0, QTableWidgetItem(row[0]))
                self.tableWidget.setItem(inx, 1, QTableWidgetItem(row[1]))
                self.tableWidget.setItem(inx, 2, QTableWidgetItem(row[3]))
        self.show=False

    def donate_fill(self):
        cur.execute("SELECT DId FROM Donate")
        rows = cur.fetchall()
        self.identity = rows[-1][0]+1
        self.data_liste = [self.b_groupdb,self.l_donation.text(),self.identity,self.adressdb,self.i_numdb]
        c=tuple(self.data_liste)
        with conn:
            q3=("""INSERT INTO Donate VALUES(?,?,?,?,?)""")
            cur.execute(q3,c)
            conn.commit()
    def stockupdate(self):
        with conn:
            q6="""UPDATE Stock SET Samount = ? WHERE Sbloodgroup= ?"""
            data=(self.a,self.group)
            cur.execute(q6,data)
    def stock(self,group):
        self.group=group
        if self.group=="A Rh+":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.apo.display(self.a)
            self.stockupdate()
        elif self.group=="B Rh+":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.bpo.display(self.a)
            self.stockupdate()
        elif self.group=="B Rh-":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.bne.display(self.a)
            self.stockupdate()
        elif self.group=="A Rh-":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.ane.display(self.a)  
            self.stockupdate()      
        elif self.group=="AB Rh+":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.abpo.display(self.a)
            self.stockupdate()
        elif self.group=="AB Rh-":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.abne.display(self.a)
            self.stockupdate()
        elif self.group=="0 Rh+":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.spo.display(self.a)
            self.stockupdate()
        elif self.group=="0 Rh-":
            cur.execute("SELECT Samount FROM Stock WHERE Sbloodgroup=?", (self.group,))
            rows=cur.fetchone()
            self.a=rows[0]+1
            self.sne.display(self.a)
            self.stockupdate()
        else:
            return False

    def gotoscreenmain(self):
        mainwindow.tc_edit.clear()
        mainwindow.psw_edit.clear()
        widget.setCurrentIndex(widget.currentIndex()-2)
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
conn=sl.connect("database.db")
cur=conn.cursor()
mainwindow=MainWindow() 
screen2=Screen2() #sign_ıp
screen3=Screen3()   #profile
widget.addWidget(mainwindow)
widget.addWidget(screen2)
widget.addWidget(screen3)

widget.setFixedHeight(750)
widget.setFixedWidth(1000)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")