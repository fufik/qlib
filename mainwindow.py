#!/bin/env python
from qlib import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox, QLineEdit,QFormLayout,QLabel,QSpinBox
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QRegExpValidator
import sys
import math
class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('form.ui', self)
        self.ui.show()
        self.LE_mode = False        #False -- coefficients, True -- qbits
        self.rb_qbit.mode = True
        self.rb_coef.mode = False
        self.rb_qbit.toggled.connect(self.changeMode)
        self.rb_coef.toggled.connect(self.changeMode)


        self.sa_layout = QFormLayout()
        self.scrollAreaWidgetContents.setLayout(self.sa_layout)
        
        self.operator = ""
        self.b1 = False
        self.b_X.op = "X"
        self.b_X.toggled.connect(self.onClicked)
        self.b_Y.op = "Y"
        self.b_Y.toggled.connect(self.onClicked)
        self.b_Z.op = "Z"
        self.b_Z.toggled.connect(self.onClicked)
        self.b_H.op = "H"
        self.b_H.toggled.connect(self.onClicked)
        self.b_R.op = "R"
        self.b_R.toggled.connect(self.onClicked)
        self.b_CNOT.op = "CNOT"
        self.b_CNOT.toggled.connect(self.onClicked)
        self.b_Fourier.op = "Fourier"
        self.b_Fourier.toggled.connect(self.onClicked)
        
        #self.line_out.setReadOnly(True)
        rx = QRegExp('[0-9|,|.|-|j|+|a-z]*')
        validator = QRegExpValidator(rx, self)
        self.line_in.setValidator(validator)
        self.line_in.textChanged.connect(self.line_in_f)
        self.but_ACT.clicked.connect(self.act_f)
        #BLOCKING
        self.b_X.setEnabled(False)
        self.b_Y.setEnabled(False)
        self.b_Z.setEnabled(False)
        self.b_H.setEnabled(False)
        self.b_CNOT.setEnabled(False)
        self.b_R.setEnabled(False)
        self.b_Fourier.setEnabled(False)

    def onClicked(self):
        rb = self.sender()
        if rb.isChecked():
            self.b1=True
            if self.line_in.text() != "":
                self.but_ACT.setEnabled(True)
            self.operator = rb.op

            #cleaning scrollarea widgets
            n = self.sa_layout.rowCount()
            print(n)
            while self.sa_layout.count():
                c = self.sa_layout.takeAt(0)
                if c.widget():
                    c.widget().deleteLater()
            if rb.op == "H":
                rx = QRegExp('[0-9|,]*')
                validator = QRegExpValidator(rx, self)
                par = QLineEdit()
                par.setValidator(validator)
                par.setPlaceholderText("Введите 0 для всех кубитов")
                self.sa_layout.insertRow(0,"Кубит",par)
            if rb.op == "R": 
                rx = QRegExp('[0-9|a-z|.|-]*')
                validator = QRegExpValidator(rx, self)
                par = QLineEdit()
                par.setValidator(validator)
                self.sa_layout.insertRow(0,"Тета",par)
            if rb.op == "CNOT":
                rx = QRegExp('[0-9|,]*')
                validator = QRegExpValidator(rx, self)
                par = QLineEdit()
                par.setPlaceholderText("Номера управляющих кубитов")
                par2 = QLineEdit()
                par2.setPlaceholderText("Номера изменяемых кубитов")
                par.setValidator(validator)
                par2.setValidator(validator)
                self.sa_layout.insertRow(0,"C",par)
                self.sa_layout.insertRow(1,"NOT",par2)

        
    def act_f(self):
        ins = self.line_in.text()
        if not self.LE_mode: 
            c = ins.split(',')
            q = sp.Matrix(c) 
            n = int(log(len(q),2)) #length in qbits
            q = qregister(q) #input qregister
            res = qregister(sp.Matrix([1]))
        else:
            arg = list()
            for c in ins:
                if c == '0':
                    arg.append(qbit_0)
                elif c == '1':
                    arg.append(qbit_1)
                elif c=='+':
                    arg.append(qbit_sp)
                elif c=='-':
                    arg.append(qbit_sn)

            q = qregister(*arg)   
            n = len(q)
            res = qregister(sp.Matrix([1]))
        print("QR:",q)
        if self.operator == "X":
            op = op_X**n
            print("OP: ",op)
            res = op @ q
        elif self.operator == "Y":
            op = op_Y**n
            res = op @ q
        elif self.operator == "Z":
            op = op_Z**n
            res = op @ q
        elif self.operator == "H":
            if self.sa_layout.itemAt(0,1).widget().text() == "":
                op = op_H**n
                res = op @ q
            else:
                try:
                    s = self.sa_layout.itemAt(0,1).widget().text()
                    qbits = [int(i) for i in s.split(',')]
                except:
                    self.line_out.setText("Ошибка обработки параметров")
                    return
         
                for i in qbits:
                    if i > n:
                        self.line_out.setText("Превышение размера курегистра")
                        return

                for i in range(len(qbits)):
                    qbits[i] -=1

                l = list()
                for i in range(n):
                    l.append(op_I)
                for i in qbits:
                    l[i] = op_H
                
                op = op_I**0
                for i in l:
                    op = op*i
                res = op @ q
        elif self.operator == "Fourier":
            res = fourier(q)
        elif self.operator == "R":
            try:
                angle = float(self.sa_layout.itemAt(0,1).widget().text())
            except:
                self.line_out.setText("Неправильно установлен коэффициент Тета")
                return
            op_R =  qoperator(matrix.genpshift(angle,1))
            op = op_R**n
            res = op @ q
        elif self.operator == "CNOT":
            try:
                s = self.sa_layout.itemAt(0,1).widget().text()
                Cs = [int(i) for i in s.split(',')]
            except Exception as e:
                print(e)
                self.line_out.setText("Ошибка обработки параметров C")
                return
            try:
                s = self.sa_layout.itemAt(1,1).widget().text()
                NOTs = [int(i) for i in s.split(',')]
            except:
                self.line_out.setText("Ошибка обработки параметров NOT")
                return
            z = Cs + NOTs
            for i in z:
                if i > n:
                    self.line_out.setText("Превышение размеров курегистра")
                    return
            for i in range(len(Cs)):
                Cs[i] -=1
            for i in range(len(NOTs)):
                NOTs[i] -=1
            list_1 = list()
            list_2 = list()
            for i in range(n):
                list_1.append(op_I)
                list_2.append(op_I)
            for i in Cs:
                list_1[i] = (qbit_0 @ qbit_0)
                list_2[i] = (qbit_1 @ qbit_1)
            for i in NOTs:                 
                list_2[i] = op_X

            op_l = op_I**0 #1
            op_r = op_I**0
            for i in list_1:
                op_l = op_l * i
            for i in list_2:
                op_r = op_r * i
            op = op_l + op_r #operator is ready
            res = op @ q

        print(res)
        answer = (', '.join([str(e) for e in (res.vector.transpose()) ])).replace('I','j')
        self.line_out.setText(answer)

    def line_in_f(self):
        le = self.sender()
        t = self.line_in.text() 
        if t != "":
            r = self.checkparse(t)
            #print(r)
            if r > 0:
                if r>=1 and r<2:
                    self.unblock1()
                    self.block2()
                if r>=2:
                    self.unblock1()
                    self.unblock2()
            else:
                self.block1()
                self.block2()
            if self.b1:
                self.but_ACT.setEnabled(True)
        else:
            self.block1()
            self.block2()
            self.but_ACT.setEnabled(False)

    def block1(self):
        self.b_X.setEnabled(False)
        self.b_Y.setEnabled(False)
        self.b_Z.setEnabled(False)
        self.b_H.setEnabled(False)
        self.b_R.setEnabled(False)
    
    def block2(self):
        self.b_CNOT.setEnabled(False)
        self.b_Fourier.setEnabled(False)
    
    def unblock1(self):
        self.b_X.setEnabled(True)
        self.b_Y.setEnabled(True)
        self.b_Z.setEnabled(True)
        self.b_H.setEnabled(True)
        self.b_R.setEnabled(True)
    
    def unblock2(self):
        self.b_CNOT.setEnabled(True)
        self.b_Fourier.setEnabled(True)


    def checkparse(self,ins: str):
        if self.LE_mode == True:
            arg = list()
            for c in ins:
                if c == '0':
                    arg.append(qbit_0)
                elif c == '1':
                    arg.append(qbit_1)
                elif c=='+':
                    arg.append(qbit_sp)
                elif c=='-':
                    arg.append(qbit_sn)
            return len(arg)
        
        #else
        try:
            c = ins.split(',')
        except:
            return 0 # impossible operand
        #print(c)
        x =  math.log(len(c),2)
        #print(x)
        if x > 0:
            if x%1 == 0:
                return x
        return 0

    def changeMode(self):
        rb = self.sender()
        if rb.mode!=self.LE_mode:
            self.line_in.setText("")
            self.line_out.setText("")
        self.LE_mode = rb.mode
        if rb.mode == False:
            rx = QRegExp('[0-9|a-z|,|.|-|j|+]*')
            validator = QRegExpValidator(rx, self)
            self.line_in.setValidator(validator)
        else:
            rx = QRegExp('[0|1|-|+]*')
            validator = QRegExpValidator(rx, self)
            self.line_in.setValidator(validator)

    #@pyqtSlot()
    #def forth_butt_f(self):
        #global Note_cur
        #Note_cur += 1
        #self.put_note()
        #return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Win()
    sys.exit(app.exec_())
