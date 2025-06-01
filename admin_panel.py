from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QMessageBox,
                             QFileDialog, QGroupBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import json
import os
from PIL import Image
import io

class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_users()

    def init_ui(self):
        layout = QVBoxLayout()

        user_group = QGroupBox("Данные пользователя")
        user_layout = QVBoxLayout()

        fio_layout = QHBoxLayout()
        fio_label = QLabel("ФИО:")
        self.fio_input = QLineEdit()
        fio_layout.addWidget(fio_label)
        fio_layout.addWidget(self.fio_input)
        user_layout.addLayout(fio_layout)

        gender_layout = QHBoxLayout()
        gender_label = QLabel("Пол:")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Мужской", "Женский"])
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)
        user_layout.addLayout(gender_layout)

        job_layout = QHBoxLayout()
        job_label = QLabel("Должность:")
        self.job_input = QLineEdit()
        job_layout.addWidget(job_label)
        job_layout.addWidget(self.job_input)
        user_layout.addLayout(job_layout)

        photo_layout = QHBoxLayout()
        self.photo_label = QLabel()
        self.photo_label.setFixedSize(150, 200)
        self.photo_label.setStyleSheet("border: 1px solid #ccc;")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setText("Фото не выбрано")
        photo_layout.addWidget(self.photo_label)

        photo_button_layout = QVBoxLayout()
        self.photo_button = QPushButton("Выбрать фото")
        self.photo_button.clicked.connect(self.select_photo)
        photo_button_layout.addWidget(self.photo_button)
        photo_layout.addLayout(photo_button_layout)
        user_layout.addLayout(photo_layout)

        user_group.setLayout(user_layout)
        layout.addWidget(user_group)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_user)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.photo_path = None

    def load_users(self):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                self.users = json.load(f)['users']
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные пользователей: {str(e)}")
            self.users = []

    def select_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фотографию",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        
        if file_name:
            try:
                if os.path.getsize(file_name) > 2 * 1024 * 1024:
                    QMessageBox.warning(self, "Ошибка", "Размер файла не должен превышать 2 МБ")
                    return

                with Image.open(file_name) as img:
                    width, height = img.size
                    if abs(width/height - 3/4) > 0.1:
                        QMessageBox.warning(self, "Ошибка", "Соотношение сторон должно быть 3:4")
                        return

                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.photo_label.setPixmap(pixmap)
                self.photo_path = file_name

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def validate_form(self):
        if not self.fio_input.text():
            QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return False
        if not self.job_input.text():
            QMessageBox.warning(self, "Ошибка", "Введите должность")
            return False
        if not self.photo_path:
            QMessageBox.warning(self, "Ошибка", "Выберите фотографию")
            return False
        return True

    def save_user(self):
        if not self.validate_form():
            return

        new_user = {
            "fio": self.fio_input.text(),
            "gender": self.gender_combo.currentText(),
            "job": self.job_input.text(),
            "photo": self.photo_path
        }

        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            data['users'].append(new_user)

            with open('data/users.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Успех", "Данные успешно сохранены")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")

    def clear_form(self):
        self.fio_input.clear()
        self.gender_combo.setCurrentIndex(0)
        self.job_input.clear()
        self.photo_label.clear()
        self.photo_label.setText("Фото не выбрано")
        self.photo_path = None