#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt

from core import YouTubeDownloader


DOWNLOADS_DIR = './Downloads'

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

class MainComponent(QWidget):
    
    def __init__(self):
        super().__init__()
        self.plot()

    def plot(self):
        self.header_section = QHBoxLayout()   
        search_field = QLineEdit()
        get_link_btn = QPushButton("Get Links")
        self.header_section.addWidget(search_field)
        self.header_section.addWidget(get_link_btn)

        self.content_section = QGridLayout()
        self.content_section.setSpacing(10)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.header_section)
        self.main_layout.addLayout(self.content_section)
        self.setLayout(self.main_layout)

        get_link_btn.clicked.connect(lambda: self.populate_content(query=search_field.text()))

        self.setWindowTitle('MisterFerry - YouTube Downloader')
        self.resize(600, 400)
        self.show()

    def download(self, path, filename):
        sender = self.sender()
        text = sender.text()
        sender.setText('Downloading...')
        sender.setEnabled(False)
        index = int(text.split(' ')[-1])
        self.streams[index-1].download(path, filename)
        sender.setText('Downloaded')
        sender.setEnabled(True)

    def populate_content(self, query):
        sender = self.sender()
        sender.setEnabled(False)

        for i in range(self.content_section.count()):
            self.content_section.itemAt(i).widget().close()
        
        try:
            downloader = YouTubeDownloader(query)
        except Exception as e:
            print(e)
            no_results = QLabel('No results found')
            self.content_section.addWidget(no_results, 1, 1)
            sender.setEnabled(True)
            return False

        streams = downloader.get_streams()
        self.streams = streams
        if len(streams):
            title = QLabel('Title: ' + downloader.yt.title)
            self.content_section.addWidget(title, 1, 1)

        print(streams)
        for i, stream in enumerate(streams):
            description = QLabel(
                'Format: ' + str(stream.mime_type) + ' ' \
                'Resolution: ' + str(stream.resolution) + ' ' \
                'Size: ' + str(stream.filesize/1000000) + ' MB'
            )
            download_btn = QPushButton('Download '+ str(i+1))
            download_btn.clicked.connect(
                lambda: self.download(
                   DOWNLOADS_DIR, filename='_'.join((downloader.yt.title).split(' '))
                )
            )
            self.content_section.addWidget(description, i+2, 1)
            self.content_section.addWidget(download_btn, i+2, 2)
        sender.setEnabled(True)   
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainComponent()
    sys.exit(app.exec_())
