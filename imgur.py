import sys
import webbrowser
import requests
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect
import pyscreenshot as ImageGrab
import os
import uuid
# By benox. Culiacán, sinaloa. Si compartes este script o lo copias, solo agradece al autor original.
CLIENT_ID = ''  # Reemplaza esto con tu Client ID de Imgur

class ScreenCapture(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drawing = False
        self.rect = QRect()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 0, 0, 255), 3))
        painter.setBrush(QColor(0, 0, 0, 120))
        painter.drawRect(self.rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.rect.setTopLeft(event.pos())
            self.rect.setBottomRight(event.pos())

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.rect.setBottomRight(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            if self.rect.width() > 1 and self.rect.height() > 1:
                self.close()
                self.capture()

    def capture(self):
        screenshot = ImageGrab.grab(bbox=(self.rect.x(), self.rect.y(), self.rect.x() + self.rect.width(), self.rect.y() + self.rect.height()))
        filename = str(uuid.uuid4()) + ".png"
        screenshot.save(filename)

        self.upload_to_imgur(filename)

        os.remove(filename)  # Elimina el archivo después de subirlo

    def upload_to_imgur(self, filename):
        headers = {'Authorization': 'Client-ID ' + CLIENT_ID}
        with open(filename, 'rb') as fp:
            img_data = base64.b64encode(fp.read()).decode()
        response = requests.post(
            'https://api.imgur.com/3/image',
            headers=headers,
            data={
                'image': img_data,
                'type': 'base64',
            }
        )
        response.raise_for_status()
        data = response.json()
        print(f"Imagen subida a {data['data']['link']}")
        webbrowser.open(data['data']['link'])

app = QApplication(sys.argv)
window = ScreenCapture()
window.setWindowOpacity(0.2)
window.showFullScreen()
app.exec_()
