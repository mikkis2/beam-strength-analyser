'''
Created on 8.3.2018

@author: MJwork
'''
import sys
from PyQt5.QtWidgets import QApplication
from gui import GUI

def main():
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    pass
main()