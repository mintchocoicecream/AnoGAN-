import sys
from login import LoginClass
from PyQt5.QtWidgets import *
import PyQt5
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5 import uic
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginClass()
    win.show()
    sys.exit(app.exec_())