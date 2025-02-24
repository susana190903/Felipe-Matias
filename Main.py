import sys
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QSlider, QVBoxLayout, QLabel)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QCursor, QFont
from functools import partial  


# Ruta del archivo.
VIDEO_PATH = "VIDEOS/D2/main2.avi"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana sin barra de título
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        # Contenedor para organizar el texto y el video.
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: black;")
        
        # Controles principales para organizar la ventana.
        self.layout = QVBoxLayout(self.container)

        # Texto encima del video
        self.label = QLabel("Felipe Matías Velasco", self.container)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Ananda", 35))
        self.label.setStyleSheet("color: yellow;")

        # Control de reproducción de video de Qt.
        self.video_widget = QVideoWidget(self.container)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(VIDEO_PATH)))
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.stateChanged.connect(self.state_changed)
        self.media_player.mediaStatusChanged.connect(self.media_status_changed)

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
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.video_widget)

        # Personalizar la ventana.
        self.setWindowTitle("BIENVENIDO")

        # Definir el tamaño y posición de la ventana
        self.setGeometry(0, 0, 900, 700)  # Ajusta el tamaño según tus necesidades de felipe matias
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry(desktop.screenNumber(QCursor().pos()))
        self.move(screen_rect.width() - self.width(), 0) # Mover la ventana a la mitad izquierda

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Reproducir el video.
        self.media_player.play()

        # Aplicar el estilo CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
                color: white;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #3A3A3A;
                height: 10px;
                background: #2E2E2E;
                margin: 0px;
            }
            
            QSlider::handle:horizontal {
                background: #606060;
                border: 1px solid #3A3A3A;
                width: 14px;
                margin: -2px 0;
                border-radius: 5px;
            }
        """)

    def state_changed(self, newstate):
        if newstate == QMediaPlayer.StoppedState:
            # No cerrar la ventana al finalizar
            self.media_player.play()

    def media_status_changed(self, status):
        if status == QMediaPlayer.EndOfMedia:
            # Reiniciar la reproducción al finalizar el video
            self.media_player.setPosition(0)
            self.media_player.play()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonDblClick:
            obj.setFullScreen(not obj.isFullScreen())
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())