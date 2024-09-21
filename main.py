import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import pyautogui

class ScreenshotThread(QThread):
    update_signal = pyqtSignal(QPixmap)

    def run(self):
        while True:
            screenshot = pyautogui.screenshot()
            qImg = QImage(screenshot.tobytes('raw', 'RGB'), screenshot.width, screenshot.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.update_signal.emit(pixmap)
            self.msleep(1)  # per 10 second update

class ScreenViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Screen Viewer')
        self.resize(1680, 709)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.label = QLabel(self)
        self.label.setScaledContents(False)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.label)
        self.setLayout(layout)

        self.screenshot_thread = ScreenshotThread()
        self.screenshot_thread.update_signal.connect(self.update_label)
        self.screenshot_thread.start()

    def update_label(self, pixmap):
        self.label.setPixmap(pixmap.scaled(self.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_viewer = ScreenViewer()
    screen_viewer.show()
    sys.exit(app.exec_())
