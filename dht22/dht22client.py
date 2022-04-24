import sys

import adafruit_dht
import board
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget

device = adafruit_dht.DHT22(board.D18)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self.get_label(), alignment=Qt.AlignCenter)
        self.button = QPushButton("Get DHT22 Data")
        self.button.clicked.connect(self.click)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.resize(QApplication.primaryScreen().availableSize() / 5)


    def get_label(self):
        temperature = device.temperature
        humidity = device.humidity
        return f"Temp: {temperature:.1f}°C, Humidity: {humidity}%"

    @Slot()
    def click(self):
        try:
            self.label.setText(self.get_label())
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            device.exit()
            raise error


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
