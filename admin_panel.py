from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
import json
import os

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавление сотрудника")
        self.fio_input = QLineEdit()
        self.gender_input = QLineEdit()
        self.job_input = QLineEdit()
        self.photo_button = QPushButton("Загрузить фото")
        self.save_button = QPushButton("Сохранить")

        self.photo_path = ""

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.fio_input)
        layout.addWidget(QLabel("Пол:"))
        layout.addWidget(self.gender_input)
        layout.addWidget(QLabel("Должность:"))
        layout.addWidget(self.job_input)
        layout.addWidget(self.photo_button)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        self.photo_button.clicked.connect(self.load_photo)
        self.save_button.clicked.connect(self.save_data)

    def load_photo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.png *.jpg)")
        if file:
            self.photo_path = file

    def save_data(self):
        data = {
            "fio": self.fio_input.text(),
            "gender": self.gender_input.text(),
            "job": self.job_input.text(),
            "photo": self.photo_path
        }
        with open("data/users.json", "r+", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except:
                all_data = []
            all_data.append(data)
            f.seek(0)
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        QMessageBox.information(self, "Успех", "Сотрудник добавлен.")
        self.fio_input.clear()
        self.gender_input.clear()
        self.job_input.clear()