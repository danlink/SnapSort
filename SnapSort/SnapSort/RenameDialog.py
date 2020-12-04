'''
Created on 18.02.2018

@author: Daniel
'''
import os
from datetime import date
from PyQt5 import QtWidgets, QtCore

from gui.renameDialog_ui import Ui_Mainwin
import ModifyDate
from PyQt5.Qt import QSettings

class RenameDialog(QtWidgets.QMainWindow, Ui_Mainwin):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        settings = QSettings()
        if settings.value("Geometry"):  # Sind Vorgaben in der Registry vorhanden?
            self.restoreGeometry(settings.value("Geometry"))    # Dann Größe und Position des Fensters wiederherstellen
        
#         self.watchedDir = os.getcwd()
                
        self.renameButton.clicked.connect(self.renameSelectedFile)
        
        self.dateEdit.setText(date.today().isoformat())
        self.dateEdit.textChanged.connect(self.updatePreview)
        
        self.descriptionSuggestions.hide()
        
        self.descriptionEdit.textEdited.connect(self.updatePreview)
        self.descriptionEdit.textEdited.connect(self.runCompletion)
        
        self.sectionBox.currentIndexChanged.connect(self.updatePreview)
        
        self.lastModifiedComponent = "Y"
        
    def closeEvent(self, *args, **kwargs):
        settings = QSettings()
        settings.setValue("Geometry", QtCore.QVariant(self.saveGeometry()))
        print("geschlossen")
        return QtWidgets.QMainWindow.closeEvent(self, *args, **kwargs)
            
    def keyPressEvent(self, e):
        if (e.key() == QtCore.Qt.Key_Return) & (e.modifiers() == QtCore.Qt.ControlModifier):
            self.renameSelectedFile()

        if (e.key() == QtCore.Qt.Key_Down):
            currentRow = self.descriptionSuggestions.currentRow()
            if self.descriptionSuggestions.usedRows > currentRow:
                self.descriptionSuggestions.setCurrentCell(currentRow + 1, 0)
                self.transferSuggestion(currentRow + 1)
        
        if (e.key() == QtCore.Qt.Key_Up):
            currentRow = self.descriptionSuggestions.currentRow()
            if currentRow > 0:
                self.descriptionSuggestions.setCurrentCell(currentRow - 1, 0)
                self.transferSuggestion(currentRow - 1)
        
        if (e.key() == QtCore.Qt.Key_F1):
            self.dateEdit.setFocus()
            self.dateEdit.selectAll()
        
        if (e.key() == QtCore.Qt.Key_F2):
            self.sectionBox.setFocus()
            
        if (e.key() == QtCore.Qt.Key_F3):
            self.descriptionEdit.setFocus()
            
#         if (e.key() == QtCore.Qt.Key_PageUp) & (e.modifiers() == QtCore.Qt.ControlModifier):
#             currentRow = self.fileListWidget.currentRow()
#             if currentRow > 0:
#                 self.fileListWidget.setCurrentRow(currentRow - 1)
#          
#         if (e.key() == QtCore.Qt.Key_PageDown) & (e.modifiers() == QtCore.Qt.ControlModifier):
#             currentRow = self.fileListWidget.currentRow()
#             if currentRow < self.fileListWidget.usedRows:
#                 self.fileListWidget.setCurrentRow(currentRow + 1)
        
        if (e.key() == QtCore.Qt.Key_J) & (e.modifiers() == QtCore.Qt.ControlModifier):
            self.descriptionEdit.setText(SnapSort.ModifyDate.changeYear(self.descriptionEdit.text(), self.dateEdit.text(), 0))
            self.lastModifiedComponent = "Y"
        
        if (e.key() == QtCore.Qt.Key_M) & (e.modifiers() == QtCore.Qt.ControlModifier):
            self.descriptionEdit.setText(SnapSort.ModifyDate.changeMonth(self.descriptionEdit.text(), self.dateEdit.text(), 0))
            self.lastModifiedComponent = "M"
            
        if (e.key() == QtCore.Qt.Key_Q) & (e.modifiers() == QtCore.Qt.ControlModifier):
            self.descriptionEdit.setText(SnapSort.ModifyDate.changeQuarter(self.descriptionEdit.text(), self.dateEdit.text(), 0))
            self.lastModifiedComponent = "Q"
            
        if (e.key() == QtCore.Qt.Key_PageUp):
            if self.lastModifiedComponent == "Y":
                self.changeDescriptionYear(+1)
            elif self.lastModifiedComponent == "M":
                self.changeDescriptionMonth(+1)
            elif self.lastModifiedComponent == "Q":
                self.changeDescriptionQuarter(+1)
        
        if (e.key() == QtCore.Qt.Key_PageDown):
            if self.lastModifiedComponent == "Y":
                self.changeDescriptionYear(-1)
            elif self.lastModifiedComponent == "M":
                self.changeDescriptionMonth(-1)
            elif self.lastModifiedComponent == "Q":
                self.changeDescriptionQuarter(-1)
                
        if (e.key() == QtCore.Qt.Key_Escape):
            self.close()
    
    def changeDescriptionYear(self, delta):
        self.descriptionEdit.setText(SnapSort.ModifyDate.changeYear(self.descriptionEdit.text(), delta=delta))
    
    def changeDescriptionMonth(self, delta):
        self.descriptionEdit.setText(SnapSort.ModifyDate.changeMonth(self.descriptionEdit.text(), delta=delta))
    
    def changeDescriptionQuarter(self, delta):
        self.descriptionEdit.setText(SnapSort.ModifyDate.changeQuarter(self.descriptionEdit.text(), delta=delta))
    
    def runCompletion(self):
        typedSnippet = self.descriptionEdit.text()
        completionMatches = [s for s in self.fileIndex if typedSnippet.casefold() in s[2].casefold()]
        
        if len(self.descriptionEdit.text()) > 1:
            self.descriptionSuggestions.clear()
            i = 0
            for completionEntry in completionMatches:
                completionLine = "{section:>5} | {description}".format(section=completionEntry[1], description=completionEntry[2])
                print(completionLine)
                self.descriptionSuggestions.setItem(i, 0, QtWidgets.QTableWidgetItem(completionEntry[2]))
                self.descriptionSuggestions.setItem(i, 1, QtWidgets.QTableWidgetItem(completionEntry[1]))
                self.descriptionSuggestions.usedRows = i
                i += 1
                if i > 4:
                    break
            if i > 0:
                self.descriptionSuggestions.show()
        else:
            self.descriptionSuggestions.hide()
            
    def transferSuggestion(self, row):
        self.descriptionEdit.setText(self.descriptionSuggestions.item(row, 0).text())
        
        sectionBoxRow = self.sectionBox.findText(self.descriptionSuggestions.item(row, 1).text())
        self.sectionBox.setCurrentIndex(sectionBoxRow)
            
    def renameSelectedFile(self):
        if self.fileListWidget.currentRow() < 0:
            print("Datei wählen")
            return
        
        srcName = self.fileListWidget.currentItem().text()
        destDir = self.sectionBox.currentText()
        destName = self.composeNewFilename()
        print("Alter Name: ", srcName)
        print("Neuer Name: ", destName, "in Sektion", destDir)
        destCompletePath = os.path.join(destDir, destName)
        self.fileListWidget.takeItem(self.fileListWidget.currentRow())
        
        self.fileIndex.append((self.dateEdit.text(), self.sectionBox.currentText(), self.descriptionEdit.text()))
        
        try:
            os.renames(os.path.join(self.watchedDir, srcName), os.path.join(self.watchedDir, destCompletePath))
            self.statusBar().showMessage("Erfolgreich umbenannt: " + destCompletePath, 3000)
        except IOError as e:
            print("Fehler beim Umbenennen:", e)
        
        self.descriptionEdit.setText("")
        self.descriptionSuggestions.clear()
        self.descriptionSuggestions.hide()
        self.dateEdit.selectAll()
        self.dateEdit.setFocus()
                
    def updatePreview(self):
        self.statusBar().showMessage(self.composeNewFilename())
        
    def composeNewFilename(self):
        documentDate = date.today().isoformat()
        if not self.dateEdit.text() == "":
            documentDate = self.dateEdit.text()
        newFileName = documentDate + " " + self.sectionBox.currentText() + " " + self.descriptionEdit.text() + ".pdf"
        return newFileName
        
    def updatedFiles(self, fileList, sectionDirList):
        self.sectionBox.clear()
        i = 0
        for f in fileList[::-1]:
            self.fileListWidget.addItem(f)
            self.fileListWidget.usedRows = i
            i += 1
        self.sectionBox.addItems(sectionDirList)
            
    def show(self, *args, **kwargs):
        self.fileListWidget.setCurrentRow(0)
        self.dateEdit.selectAll()
        self.dateEdit.setFocus()
        return QtWidgets.QDialog.show(self, *args, **kwargs)