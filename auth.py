from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

class AuthWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Авторизация")
        self.role_box = QComboBox()
        self.role_box.addItems(["Администратор доступа", "Сотрудник службы безопасности"])
        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.secret_input = QLineEdit()
        self.login_button = QPushButton("Войти")

        self.password_input.setEchoMode(QLineEdit.Password)
        self.secret_input.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Роль:"))
        layout.addWidget(self.role_box)
        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Секретное слово:"))
        layout.addWidget(self.secret_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        role = self.role_box.currentText()
        login = self.login_input.text()
        password = self.password_input.text()
        secret = self.secret_input.text()

        if role == "Администратор доступа" and login == "guardianskk" and password == "Admin@123" and secret == "key1":
            self.main_window.switch_to(1)
        elif role == "Сотрудник службы безопасности" and login == "defendservice" and password == "Secure@456" and secret == "key2":
            self.main_window.switch_to(2)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверные данные.")