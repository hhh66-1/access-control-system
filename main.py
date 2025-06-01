from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from auth import AuthWindow
from admin_panel import AdminPanel
from guest_request import GuestRequestForm
from emulator import EmulatorWindow
import sys

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.auth = AuthWindow(self)
        self.admin = AdminPanel()
        self.request = GuestRequestForm()
        self.emulator = EmulatorWindow()

        self.addWidget(self.auth)
        self.addWidget(self.admin)
        self.addWidget(self.request)
        self.addWidget(self.emulator)

        self.setFixedSize(400, 500)

    def switch_to(self, index):
        self.setCurrentIndex(index)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())