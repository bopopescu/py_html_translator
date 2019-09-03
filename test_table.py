import sys
from PyQt5              import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QLabel, QGridLayout)
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


def window():
    app = QApplication(sys.argv)
    win = QWidget()

    l1 = QLabel("Name")
    nm = QtWidgets.QLineEdit()

    l2 = QLabel("Address")
    add1 = QtWidgets.QLineEdit()
    add2 = QtWidgets.QLineEdit()
    fbox = QtWidgets.QFormLayout()
    fbox.addRow(l1, nm)
    vbox = QVBoxLayout()

    vbox.addWidget(add1)
    vbox.addWidget(add2)
    fbox.addRow(l2, vbox)
    hbox = QHBoxLayout()

    r1 = QtWidgets.QRadioButton("Male")
    r2 = QtWidgets.QRadioButton("Female")
    hbox.addWidget(r1)
    hbox.addWidget(r2)
    hbox.addStretch()
    fbox.addRow(QLabel("sex"), hbox)
    fbox.addRow(QPushButton("Submit"), QPushButton("Cancel"))

    win.setLayout(fbox)

    win.setWindowTitle("PyQt")
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    window()