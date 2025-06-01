from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget, QLabel
from PyQt5.QtCore import Qt
from auth import AuthWindow
from admin_panel import AdminPanel
from guest_request import GuestRequestForm
from emulator import EmulatorWindow
import sys

class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.auth = AuthWindow(self)
        self.admin = AdminPanel(self)
        self.request = GuestRequestForm(self)
        self.emulator = EmulatorWindow(self)

        self.addWidget(self.auth)
        self.addWidget(self.admin)
        self.addWidget(self.request)
        self.addWidget(self.emulator)

        self.setFixedSize(800, 600)
        self.setWindowTitle("Система управления доступом 'Стражник'")

        self.auth.auth_successful.connect(self.handle_auth)

    def handle_auth(self, role, full_name):
        if role == "admin":
            self.setCurrentWidget(self.admin)
        else:
            self.setCurrentWidget(self.request)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()