'''
Created on 18.02.2018

@author: Daniel
'''
import os
import re
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from SnapSort.RenameDialog import RenameDialog
from PyQt5.Qt import QSettings

class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        
        settings = QSettings()
        
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        selDirAction = menu.addAction("Select watched dir")
        renameAllAction = menu.addAction("Rename all Files")
        self.setContextMenu(menu)
        
        self.activated.connect(self.callRenameDialog)
        exitAction.triggered.connect(self.stopbuttonpressed)
        selDirAction.triggered.connect(self.showDirSelector)
        renameAllAction.triggered.connect(self.renameAllFiles)
        
        self.reactiondialog = RenameDialog()
        defaultWatchedDir = os.path.normcase(os.getcwd())   # Beim ersten Start: Überwachtes Verzeichnis = Arbeitsverzeichnis
        self.watchedDir = settings.value("WatchedDirectory", defaultWatchedDir) # Zuletzt verwendetes Verzeichnis wiederverwenden
        self.reactiondialog.watchedDir = self.watchedDir
        print("Watched directories: ", self.watchedDir)
        
        self.observer = Observer()
        self.handler = WatchdogHandler()
        self.observer.schedule(self.handler, self.watchedDir, False)
        self.observer.start()        
        
        self.reIndexDirectory()
                
        self.handler.newfile.connect(self.filesChanged)
    
    #===========================================================================
    # Nach Änderung des überwachten Verzeichnisses werden alle Dateien neu eingelesen
    # und daraus ein Index erstellt (separieren der Namensbestandteile und Ablegen in
    # einer Liste
    #===========================================================================
    def reIndexDirectory(self):
        print("Reading current directory...", end="")
        self.allFiles = self.getAllFiles()
        print("done")
        #print(self.allFiles)
        
                
        print("Indexing all files in current directory...", end="")
        self.reactiondialog.fileIndex = self.scanFilenames(self.watchedDir)
        print("done")
        #print(self.reactiondialog.fileIndex)
    
    #===========================================================================
    # Gibt eine Liste der Dateien in allen Unterverzeichnissen zurück
    # Die Dateien müssen einem bestimmten Schema entsprechend benannt sein. Der
    # Dateiname wird in drei Abschnitte Aufgeteilt: Datum, Abschnitt, Beschreibung
    # Zurückgegeben wird eine Liste der 3er Tupel
    #===========================================================================
    def scanFilenames(self, rootDir):
        listOfFilenames = list()
        for baseDir, subDir, files in os.walk(rootDir):
            for filename in files:
                if re.match(r"\d{4}(\-\d{2})?(\-?\d{2})? [A-Z]{3,5} .*\.[Pp][Dd][Ff]$", filename):  # Filter für Dateinamen. Zulässig ist auch kurzes Datum (z.B. nur Monat und Jahr oder nur Jahr)
                    filenameComponents = tuple(filename[:-4].split(" ", 2)) # Auftrennen anhand der Leerzeichen in drei Abschnitte, diese in Tupel speichern
                    print(filenameComponents)
                    listOfFilenames.append(filenameComponents)
        return listOfFilenames  # Liste von Tupeln zurückgeben
    
    #===========================================================================
    # Zeigt den Verzeichnisauswahldialog. Das ausgewählte Verzeichnis wird zum
    # neuen überwachten Verzeichnis. Watchdog wird entsprechend geändert.
    #===========================================================================
    def showDirSelector(self):
        print("selektor gewählt")
        fname = QtWidgets.QFileDialog.getExistingDirectory(None, "Überwachtes Verzeichnis wählen", self.watchedDir) # Zeigt den Dialog
        fname = os.path.normcase(fname)
        if (fname != self.watchedDir and fname): # Prüfung ob Verzeichnis gewählt wurde und ob es sich vom vorherigen unterscheidet
            self.observer.unschedule_all() # Watchdog anhalten
            print("Watchdog gestoppt")
            self.observer.schedule(self.handler, fname, False) # Watchdog neu starten
            self.watchedDir = fname
            self.reactiondialog.watchedDir = self.watchedDir
            
            settings = QSettings()
            settings.setValue("WatchedDirectory", self.watchedDir)  # neuen Verzeichnispfad speichern
            
            print("Überwache jetzt:", fname)
            self.reIndexDirectory() # Verzeichnis neu einlesen und Dateien indizieren            
        else:
            print("Verzeichnis nicht geändert")
    
    #===========================================================================
    # Gibt eine Liste aller .pdf Dateien im überwachten Verzeichnis zurück
    # --> Eingabedateien zur Verarbeitung
    #===========================================================================
    def getAllFiles(self):
        files = list()
        for f in os.listdir(self.watchedDir):
            if f.endswith(".pdf"):  #TODO: Filter für Großschreibung hinzufügen. Evtl. auf Datumsformat einschränken?
                files.append(f)
        return files
    
    #===========================================================================
    # Liest im überwachten Verzeichnis alle Ordnernamen ein, die den Kriterien
    # für Abschnittsbezeichnungen entsprechen (nur Großbuchstaben, max 5 Zeichen)
    #===========================================================================
    def getAllSectionDirs(self):
        sectionDirs = list()
        for d in os.scandir(self.watchedDir):
            if d.is_dir() and d.name.isupper() and (len(d.name) <=5):
                sectionDirs.append(d.name)
        print(sectionDirs)
        return sectionDirs
    
    #===========================================================================
    # Helferfunktion: Gibt die neu hinzugefügten Dateien als Liste zurück
    #===========================================================================
    def addedFiles(self, oldFileList, allFileList):
        oldFileList = set(oldFileList)
        return [f for f in allFileList if f not in oldFileList]
    
    #===========================================================================
    # Beendet die Applikation: Erst wird der Watchdog gestoppt, dann das Fenster
    # geschlossen
    #===========================================================================
    def stopbuttonpressed(self):
        self.observer.stop()
        self.observer.join()
        #self.close()
        self.hide()
        print("Exiting")
        sys.exit()
    
    #===========================================================================
    # Ruft den Dialog zum Umbennen auf, wenn das Tray-Icon einfach angeklickt wird
    #===========================================================================
    def callRenameDialog(self, reason):
        if reason == self.Trigger:          # Trigger bedeutet mit links angeklickt
            self.renameAllFiles()
    
    #===========================================================================
    # Zeigt den Dialog zum Umbennen
    #===========================================================================
    def renameAllFiles(self):
        self.reactiondialog.fileListWidget.clear()
        self.reactiondialog.updatedFiles(self.getAllFiles(), self.getAllSectionDirs())
        self.reactiondialog.show()
        self.reactiondialog.activateWindow()
        self.reactiondialog.setFocus()
        self.reactiondialog.dateEdit.selectAll()
        self.reactiondialog.dateEdit.setFocus()
    
    #===========================================================================
    # Handler für den Watchdog. Wird ausgeführt sobald Änderungen im überwachten
    # Verzeichnis erkannt wurden.
    #===========================================================================
    def filesChanged(self):
        print("File change detected in watched directory:")
        newFiles = self.addedFiles(self.allFiles, self.getAllFiles()) # Hilfsfunktion liefert nur neue Dateien
        print(newFiles)
        self.allFiles.extend(newFiles) # Liste aller Dateien um Neuzugang erweitern
        self.reactiondialog.watchedDir = self.watchedDir # FIXME: Sollte nicht notwendig sein
        self.reactiondialog.updatedFiles(newFiles, self.getAllSectionDirs())
        
        self.reactiondialog.show()
        self.reactiondialog.setFocus()
        
class WatchdogHandler(PatternMatchingEventHandler, QObject):
    patterns = ["*.pdf", "*.PDF"]
    newfile = QtCore.pyqtSignal(['QString'])
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def on_created(self, event):
        print(event.event_type, event.src_path) #TODO: Debugausgabe entfernen
        self.newfile.emit(event.src_path)   
    
    def on_modified(self, event):
        print(event.event_type, event.src_path)
        self.newfile.emit(event.src_path)

    def on_moved(self, event):
        print(event.event_type, event.src_path)
        self.newfile.emit(event.src_path)       