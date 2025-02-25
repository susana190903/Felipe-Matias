#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt5.QtCore import QEvent, QUrl, Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QMainWindow,
                             QWidget, QSlider, QVBoxLayout)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from functools import partial  
import pyautogui
pyautogui.click()

# Ruta del archivo.
VIDEO_PATH = "avi/Felicidad.avi"
MULTI_POEMA_PATH = "multi_poema.py"  # Ruta del script de poema.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Controles principales para organizar la ventana.
        self.widget = QWidget(self)
        self.layout = QVBoxLayout()

        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.state_changed)

        # Deslizadores para el volumen y transición del video.
        self.seek_slider = QSlider(Qt.Horizontal)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.media_player.volume())
        self.seek_slider.sliderMoved.connect(self.media_player.setPosition)
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        self.media_player.positionChanged.connect(self.seek_slider.setValue)
        self.media_player.durationChanged.connect(partial(self.seek_slider.setRange, 0))

        # Acomodar controles en la pantalla.
        self.layout.addWidget(self.video_widget)

        # Se utiliza installEventFilter() para capturar eventos
        # del mouse en el control de video.
        self.video_widget.installEventFilter(self)

        # Personalizar la ventana.
        self.setWindowTitle("FLOR DE PIÑA")
        self.resize(800, 600)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Reproducir el video.
        self.media_player.play()

        # Mostrar la ventana en pantalla completa.
        self.showFullScreen()

    def state_changed(self, newstate):
        if newstate == QMediaPlayer.StoppedState:
            try:
                # Iniciar multi_poema.py antes de cerrar esta ventana
                subprocess.Popen(["python", MULTI_POEMA_PATH])
                # Cerrar la ventana actual
                self.close()
            except Exception as e:
                print(f"Error al ejecutar multi_poema.py: {e}")
                self.close()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            # También ejecutar multi_poema.py cuando se presiona espacio
            try:
                subprocess.Popen(["python", MULTI_POEMA_PATH])
            except Exception as e:
                print(f"Error al ejecutar multi_poema.py: {e}")
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
