from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def __init__(self):
        self.setupUi(self)
        self.dot_pressed = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 250)
        MainWindow.setMinimumSize(QtCore.QSize(300, 250))
        MainWindow.setMaximumSize(QtCore.QSize(300, 250))

        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 300, 250))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.lcdNumber = QtWidgets.QLCDNumber(self.gridLayoutWidget)
        self.lcdNumber.setSizePolicy(sizePolicy)
        self.lcdNumber.setDigitCount(10)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        self.gridLayout.addWidget(self.lcdNumber, 0, 0, 1, 3)

        self.buttons = ['backspace', '1', '2', '3', 'multiply', '4', '5', '6', 'divide', '7', '8', '9', 'plus', 'dot', '0', 'minus', 'equal']
        self.buttons_text = ['C', '1', '2', '3', '*', '4', '5', '6', '/', '7', '8', '9', '+', '.', '0', '-', '=']
        self.button_funcs = [self.digits_beh]*len(self.buttons)
        for i in 4, 8, 12, 15, 16:
            self.button_funcs[i] = self.operators_beh
        self.button_funcs[0] = self.backspace_beh


        for i in range(3, 20):
            button_name = 'pushButton_' + self.buttons[i-3]
            setattr(self, button_name, QtWidgets.QPushButton(self.gridLayoutWidget))
            button = getattr(self, button_name)
            button.setSizePolicy(sizePolicy)
            button.setObjectName(button_name)
            self.gridLayout.addWidget(button, (i) // 4, (i) % 4, 1, 1)
            button.clicked.connect(self.button_funcs[i-3])

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Calculator"))

        for i in range(17):
            cur_button = getattr(self, 'pushButton_' + self.buttons[i])
            cur_button.setText(_translate("MainWindow", self.buttons_text[i]))

    def catch_field_value(self):
        if not hasattr(self, 'fieldValue') or type(self.fieldValue) != str:
            self.fieldValue = str(int(self.lcdNumber.value()))
        self.print_field_value = True
        self.sender_text = self.sender().text()

    def backspace_beh(self):
        self.catch_field_value()
        if len(self.fieldValue) > 1:
            self.fieldValue = self.fieldValue[:-1]
        else:
            self.fieldValue = '0'
            self.first_operand = ''
            self.dot_pressed = False
        if self.print_field_value: self.lcdNumber.display(self.fieldValue)

    def digits_beh(self):
        self.catch_field_value()
        if self.sender_text == ".":
            print('ok')
            if not self.dot_pressed:
                print('ok1')
                if self.fieldValue == '0':
                    self.fieldValue = '0.'
                else: self.fieldValue += self.sender_text
                self.dot_pressed = True

        elif self.fieldValue == '0':
            self.fieldValue = self.sender_text
        else:
            self.fieldValue += self.sender_text
        if self.print_field_value: self.lcdNumber.display(self.fieldValue)
        print('digit pressed')

    def operators_beh(self):
        self.catch_field_value()
        if not hasattr(self, 'first_operand') or self.first_operand == '':
            if self.sender_text != '=':
                self.operator = self.sender_text
            self.first_operand = self.fieldValue
            print('operator pressed')
        else:
            try:
                result = str(round(eval(self.first_operand+self.operator+self.fieldValue), 10))[:10]
            except:
                result = 'DB0'
            if self.sender_text != '=':
                self.operator = self.sender_text
            self.first_operand = result

        self.fieldValue = '0'
        self.print_field_value = False
        self.lcdNumber.display(self.first_operand)
        if self.print_field_value: self.lcdNumber.display(self.fieldValue)

class calculator(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    calc = calculator()
    calc.show()
    sys.exit(app.exec_())