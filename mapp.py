from multiprocessing.sharedctypes import Value
import sys
import jss
import requests
import os
import re
import xml.etree.ElementTree as ET
from concurrent import futures

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from qtwidgets import PasswordEdit

class Dialog(QDialog):
    """Dialog."""

    def fetchPotd(self,username,password,serial):
        self.potdfield.setText("Fetching...")
        self.potdfield.repaint()
        app.processEvents()
        if not os.path.exists(os.path.expanduser('~/Library/Preferences/com.github.sheagcraig.python-jss.plist')) and (self.usernamefield.text() == '' or self.passwordfield.text() == ''):
            self.potdfield.setText("Need credentials!")
            return

        jss_url = "https://jamf-api.disney.com:8443"
        #print(username, password)
        os.system("defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_user {}".format(username))
        os.system("defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_pass {}".format(password))
        os.system("defaults write ~/Library/Preferences/com.github.sheagcraig.python-jss.plist jss_url {}".format(jss_url))

        jss_prefs = jss.JSSPrefs()
        j= jss.JSS(jss_prefs)
        j.ssl_verify = False

        try:
            mycomputer = j.Computer(serial)
            allxml = str(mycomputer)
            tree = ET.fromstring(allxml)
            try:
                checkinxml = ET.tostring(tree[0][23]).decode()
            except:
                checkinxml = "No Check-In data available!"
            checkin = re.sub('<[^<]+?>', '', checkinxml)
            self.lastcheckin.setText(checkin)
            for child in tree[8]:
                if child[1].text == "PotD":
                    potd = child[4].text
                    self.potdfield.setText(potd)
                    break
        except jss.exceptions.GetError as e:
            if "Unauthorized" in str(e):
                self.potdfield.setText("Bad Credentials!")
            else:
                self.potdfield.setText("SN not found!")
            return
        except requests.exceptions.ConnectionError:
            self.potdfield.setText("Connect to DGN!")


        

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('MacAdmin Password Picker')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()
        self.passwordfield = PasswordEdit()
        self.usernamefield = QLineEdit()
        serialnumberfield = QLineEdit()
        self.potdfield = QLineEdit()
        self.lastcheckin = QLabel()
        bigfont = self.potdfield.font()
        bigfont.setPointSize(32)
        self.potdfield.setFont(bigfont)
        self.potdfield.setReadOnly(True)
        formLayout.addRow('Serial Number:', serialnumberfield)
        formLayout.addRow('PotD:', self.potdfield)
        formLayout.addRow('Last Check-In:', self.lastcheckin)
        btn = QtWidgets.QPushButton()
        btn.setText("Fetch PotD")
        formLayout.addWidget(btn)
        formLayout.addRow('Jamf 3ID:', self.usernamefield)
        formLayout.addRow('Password:', self.passwordfield)
        dlgLayout.addLayout(formLayout)
        btn.clicked.connect(lambda: self.fetchPotd(self.usernamefield.text(),self.passwordfield.text(), serialnumberfield.text()))
        self.setLayout(dlgLayout)
    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())