import sys
from PyQt5 import QtWidgets, QtGui

from SnapSort.TrayIcon import TrayIcon

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("Leitisoft")
    app.setOrganizationDomain("leitschuh.net")
    app.setApplicationName("SnapSort")
    
    app.setQuitOnLastWindowClosed(False)
    w = QtWidgets.QWidget()
    wait_window = TrayIcon(QtGui.QIcon("SnapSort/ressources/images/icon_systray.png"), w)
    wait_window.show()
    
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    main()