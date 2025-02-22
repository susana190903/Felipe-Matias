import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QSpinBox, QComboBox, QMessageBox, QSlider
from PyQt5.QtGui import  QFont
from PyQt5.QtCore import Qt
from moviepy.editor import VideoFileClip


class VideoConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Converter")
       # self.setWindowIcon(QIcon('icon.png'))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.file_label = QLabel("Selecciona un archivo de vídeo:")
        self.layout.addWidget(self.file_label)

        self.file_button = QPushButton("Seleccionar archivo")
        self.file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_button)

        self.options_layout = QVBoxLayout()

        self.quality_layout = QHBoxLayout()
        self.quality_label = QLabel("Calidad de salida:")
        self.quality_layout.addWidget(self.quality_label)
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(70)  # Valor predeterminado
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        self.quality_slider.setTickInterval(10)
        self.quality_layout.addWidget(self.quality_slider)
        self.options_layout.addLayout(self.quality_layout)

        self.fps_layout = QHBoxLayout()
        self.fps_label = QLabel("FPS:")
        self.fps_layout.addWidget(self.fps_label)
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(30)  # Valor predeterminado
        self.fps_slider.setTickPosition(QSlider.TicksBelow)
        self.fps_slider.setTickInterval(5)
        self.fps_layout.addWidget(self.fps_slider)
        self.options_layout.addLayout(self.fps_layout)

        self.format_layout = QHBoxLayout()
        self.format_label = QLabel("Formato de salida:")
        self.format_layout.addWidget(self.format_label)
        self.format_combobox = QComboBox()
        self.format_combobox.addItems(["mp4", "avi", "mov"])
        self.format_layout.addWidget(self.format_combobox)
        self.options_layout.addLayout(self.format_layout)

        self.layout.addLayout(self.options_layout)

        self.convert_button = QPushButton("Convertir")
        self.convert_button.clicked.connect(self.convert_video)
        self.layout.addWidget(self.convert_button)

        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QPushButton, QComboBox {
                font-size: 14px;
            }
            QSlider {
                font-size: 12px;
            }
        """)

    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de vídeo", "", "Archivos de vídeo (*.mp4 *.avi *.mov)")
        if filename:
            self.input_file = filename

    def convert_video(self):
        if hasattr(self, 'input_file'):
            output_filename, _ = QFileDialog.getSaveFileName(self, "Guardar archivo de salida", "", f"Archivos de vídeo (*.{self.format_combobox.currentText()})")
            if output_filename:
                try:
                    clip = VideoFileClip(self.input_file)
                    clip.set_duration(clip.duration)  # Fixes bug with MoviePy
                    clip.set_fps(self.fps_slider.value())
                    clip.write_videofile(output_filename, codec="libx264", fps=self.fps_slider.value(), preset='medium', bitrate="%dk" % (self.quality_slider.value() * 1000))
                    clip.close()
                    QMessageBox.information(self, "Conversión completada", "La conversión del video ha sido exitosa.")
                except Exception as e:
                    QMessageBox.critical(self, "Error al convertir", f"Ha ocurrido un error al convertir el video: {str(e)}")
        else:
            QMessageBox.warning(self, "Archivo no seleccionado", "Por favor, seleccione un archivo de vídeo.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    converter = VideoConverter()
    converter.resize(400, 250)
    converter.show()
    sys.exit(app.exec_())
