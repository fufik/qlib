#!/bin/env python
from qlib import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QMessageBox, QLineEdit,QFormLayout,QLabel
from PyQt5.QtCore import pyqtSlot, QRegExp
from PyQt5.QtGui import QRegExpValidator
import sys
import math
class Win(QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.ui = uic.loadUi('form.ui', self)
        self.ui.show()

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
        self.b_CCNOT.op = "CCNOT"
        self.b_CCNOT.toggled.connect(self.onClicked)
        self.b_Fourier.op = "Fourier"
        self.b_Fourier.toggled.connect(self.onClicked)
        
        self.line_out.setReadOnly(True)
        rx = QRegExp('[0-9|,|.|-|j|+]*')
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
        self.b_CCNOT.setEnabled(False)
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
            for i in range(n):
                self.sa_layout.removeRow(i)

            if rb.op == "R": 
                rx = QRegExp('[0-9|.|-]*')
                validator = QRegExpValidator(rx, self)
                par = QLineEdit()
                par.setValidator(validator)
                self.sa_layout.addRow("Тета",par)

        
    def act_f(self):
        ins = self.line_in.text()
        c = [complex(i) for i in ins.split(',')]
        q = np.array([c],dtype=complex)
        n = len(q[0])
        q = qregister(q.transpose())
        res = qregister(np.array([[1]],dtype=complex))
        if self.operator == "X":
            op = op_X**(int(log(n,2)))
            res = op @ q
        elif self.operator == "Y":
            op = op_Y**(int(log(n,2)))
            res = op @ q
        elif self.operator == "Z":
            op = op_Z**(int(log(n,2)))
            res = op @ q
        elif self.operator == "H":
            op = op_H**(int(log(n,2)))
            res = op @ q
        elif self.operator == "R":
            try:
                angle = float(self.sa_layout.itemAt(0,1).widget().text())
            except:
                self.line_out.setText("Неправильно установлен коэффициент Тета")
                return
            op_R =  qoperator(matrix.genpshift(angle,1))
            op = op_R**(int(log(n,2)))
            res = op @ q



        answer = ', '.join([str(e) for e in (res.vector.transpose()[0]) ])
        self.line_out.setText(answer)

    def line_in_f(self):
        le = self.sender()
        t = self.line_in.text() 
        if t != "":
            r = self.checkparse(t)
            #print(r)
            if r > 1:
                if r==2:
                    self.unblock1()
                    self.block2()
                else:
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
        self.b_CCNOT.setEnabled(False)
        self.b_Fourier.setEnabled(False)
    
    def unblock1(self):
        self.b_X.setEnabled(True)
        self.b_Y.setEnabled(True)
        self.b_Z.setEnabled(True)
        self.b_H.setEnabled(True)
        self.b_R.setEnabled(True)
    
    def unblock2(self):
        self.b_CNOT.setEnabled(True)
        self.b_CCNOT.setEnabled(True)
        self.b_Fourier.setEnabled(True)


    def checkparse(self,ins: str):
        try:
            c = [complex(i) for i in ins.split(',')]
        except:
            return 0 # impossible operand
        #print(c)
        values = np.array(c,dtype=complex)
        x =  math.log(len(values),2)
        #print(x)
        if x > 0:
            if x%1 == 0:
                return len(values)
        return 0


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
