from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QMessageBox)
from PyQt5.QtCore import pyqtSignal
import json
import re
import hashlib

class AuthWindow(QWidget):
    auth_successful = pyqtSignal(str, str)  # сигнал с ролью и ФИО пользователя

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор роли
        role_layout = QHBoxLayout()
        role_label = QLabel("Тип пользователя:")
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Администратор доступа", "Сотрудник службы безопасности"])
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)
        layout.addLayout(role_layout)

        # Логин
        login_layout = QHBoxLayout()
        login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        layout.addLayout(login_layout)

        # Пароль
        password_layout = QHBoxLayout()
        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # Секретное слово
        secret_layout = QHBoxLayout()
        secret_label = QLabel("Секретное слово:")
        self.secret_input = QLineEdit()
        self.secret_input.setEchoMode(QLineEdit.Password)
        secret_layout.addWidget(secret_label)
        secret_layout.addWidget(self.secret_input)
        layout.addLayout(secret_layout)

        # Кнопка входа
        self.login_button = QPushButton("Войти в систему")
        self.login_button.clicked.connect(self.try_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def load_users(self):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                self.users = json.load(f)['users']
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные пользователей: {str(e)}")
            self.users = []

    def validate_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True

    def try_login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        secret_word = self.secret_input.text()
        role = "admin" if self.role_combo.currentText() == "Администратор доступа" else "security"

        if not login or not password or not secret_word:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
            return

        if not self.validate_password(password):
            QMessageBox.warning(self, "Ошибка", 
                "Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и специальные символы")
            return

        for user in self.users:
            if (user['login'] == login and 
                user['password'] == password and 
                user['secret_word'] == secret_word and 
                user['role'] == role):
                self.auth_successful.emit(role, user['full_name'])
                return

        QMessageBox.warning(self, "Ошибка", "Неверные учетные данные")