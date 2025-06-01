from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QMessageBox,
                             QFileDialog, QGroupBox, QDateEdit, QTextEdit)
from PyQt5.QtCore import Qt, QDate
import json
import re
from datetime import datetime, timedelta
import os

class GuestRequestForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_departments()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выбор типа заявки
        request_type_group = QGroupBox("Тип заявки")
        request_type_layout = QHBoxLayout()
        self.individual_radio = QPushButton("Индивидуальное посещение")
        self.group_radio = QPushButton("Групповое посещение")
        self.individual_radio.setCheckable(True)
        self.group_radio.setCheckable(True)
        self.individual_radio.setChecked(True)
        self.individual_radio.clicked.connect(lambda: self.switch_request_type("individual"))
        self.group_radio.clicked.connect(lambda: self.switch_request_type("group"))
        request_type_layout.addWidget(self.individual_radio)
        request_type_layout.addWidget(self.group_radio)
        request_type_group.setLayout(request_type_layout)
        layout.addWidget(request_type_group)

        # Информация для пропуска
        pass_info_group = QGroupBox("Информация для пропуска")
        pass_info_layout = QVBoxLayout()

        # Срок действия
        date_layout = QHBoxLayout()
        date_label = QLabel("Срок действия:")
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate().addDays(1))
        self.date_input.setMinimumDate(QDate.currentDate().addDays(1))
        self.date_input.setMaximumDate(QDate.currentDate().addDays(15))
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_input)
        pass_info_layout.addLayout(date_layout)

        # Подразделение
        dept_layout = QHBoxLayout()
        dept_label = QLabel("Подразделение:")
        self.dept_combo = QComboBox()
        dept_layout.addWidget(dept_label)
        dept_layout.addWidget(self.dept_combo)
        pass_info_layout.addLayout(dept_layout)

        # Принимающий сотрудник
        employee_layout = QHBoxLayout()
        employee_label = QLabel("Принимающий сотрудник:")
        self.employee_combo = QComboBox()
        employee_layout.addWidget(employee_label)
        employee_layout.addWidget(self.employee_combo)
        pass_info_layout.addLayout(employee_layout)

        pass_info_group.setLayout(pass_info_layout)
        layout.addWidget(pass_info_group)

        # Информация о посетителе
        visitor_group = QGroupBox("Информация о посетителе")
        visitor_layout = QVBoxLayout()

        # ФИО
        fio_layout = QHBoxLayout()
        fio_label = QLabel("ФИО:")
        self.fio_input = QLineEdit()
        fio_layout.addWidget(fio_label)
        fio_layout.addWidget(self.fio_input)
        visitor_layout.addLayout(fio_layout)

        # Телефон
        phone_layout = QHBoxLayout()
        phone_label = QLabel("Телефон:")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7 (___) ___-__-__")
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        visitor_layout.addLayout(phone_layout)

        # Email
        email_layout = QHBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        visitor_layout.addLayout(email_layout)

        # Организация
        org_layout = QHBoxLayout()
        org_label = QLabel("Организация:")
        self.org_input = QLineEdit()
        org_layout.addWidget(org_label)
        org_layout.addWidget(self.org_input)
        visitor_layout.addLayout(org_layout)

        # Примечание
        note_layout = QHBoxLayout()
        note_label = QLabel("Примечание:")
        self.note_input = QTextEdit()
        self.note_input.setMaximumHeight(100)
        note_layout.addWidget(note_label)
        note_layout.addWidget(self.note_input)
        visitor_layout.addLayout(note_layout)

        # Дата рождения
        birth_layout = QHBoxLayout()
        birth_label = QLabel("Дата рождения:")
        self.birth_input = QDateEdit()
        self.birth_input.setMaximumDate(QDate.currentDate())
        birth_layout.addWidget(birth_label)
        birth_layout.addWidget(self.birth_input)
        visitor_layout.addLayout(birth_layout)

        # Паспортные данные
        passport_layout = QHBoxLayout()
        passport_label = QLabel("Серия и номер паспорта:")
        self.passport_series = QLineEdit()
        self.passport_series.setMaxLength(4)
        self.passport_number = QLineEdit()
        self.passport_number.setMaxLength(6)
        passport_layout.addWidget(passport_label)
        passport_layout.addWidget(self.passport_series)
        passport_layout.addWidget(self.passport_number)
        visitor_layout.addLayout(passport_layout)

        # Фотография
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
        visitor_layout.addLayout(photo_layout)

        # Скан паспорта
        passport_scan_layout = QHBoxLayout()
        self.passport_scan_label = QLabel()
        self.passport_scan_label.setFixedSize(150, 200)
        self.passport_scan_label.setStyleSheet("border: 1px solid #ccc;")
        self.passport_scan_label.setAlignment(Qt.AlignCenter)
        self.passport_scan_label.setText("Скан не выбран")
        passport_scan_layout.addWidget(self.passport_scan_label)

        passport_scan_button_layout = QVBoxLayout()
        self.passport_scan_button = QPushButton("Выбрать скан")
        self.passport_scan_button.clicked.connect(self.select_passport_scan)
        passport_scan_button_layout.addWidget(self.passport_scan_button)
        passport_scan_layout.addLayout(passport_scan_button_layout)
        visitor_layout.addLayout(passport_scan_layout)

        visitor_group.setLayout(visitor_layout)
        layout.addWidget(visitor_group)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_request)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_form)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.clear_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.photo_path = None
        self.passport_scan_path = None
        self.request_type = "individual"

    def load_departments(self):
        # Здесь должна быть загрузка отделов из базы данных
        self.departments = ["IT", "HR", "Безопасность", "Бухгалтерия"]
        self.dept_combo.addItems(self.departments)
        self.dept_combo.currentIndexChanged.connect(self.update_employees)

    def update_employees(self):
        # Здесь должна быть загрузка сотрудников выбранного отдела
        self.employee_combo.clear()
        dept = self.dept_combo.currentText()
        if dept == "IT":
            self.employee_combo.addItems(["Иванов И.И.", "Петров П.П."])
        elif dept == "HR":
            self.employee_combo.addItems(["Сидоров С.С.", "Козлов К.К."])
        # и т.д.

    def switch_request_type(self, type_):
        self.request_type = type_
        if type_ == "individual":
            self.individual_radio.setChecked(True)
            self.group_radio.setChecked(False)
            self.birth_input.setMaximumDate(QDate.currentDate().addYears(-14))
        else:
            self.individual_radio.setChecked(False)
            self.group_radio.setChecked(True)
            self.birth_input.setMaximumDate(QDate.currentDate().addYears(-16))

    def select_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фотографию",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )
        
        if file_name:
            try:
                if os.path.getsize(file_name) > 4 * 1024 * 1024:  # 4 MB
                    QMessageBox.warning(self, "Ошибка", "Размер файла не должен превышать 4 МБ")
                    return

                # Отображение превью
                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.photo_label.setPixmap(pixmap)
                self.photo_path = file_name

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def select_passport_scan(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите скан паспорта",
            "",
            "Images (*.jpg)"
        )
        
        if file_name:
            try:
                # Отображение превью
                pixmap = QPixmap(file_name)
                pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.passport_scan_label.setPixmap(pixmap)
                self.passport_scan_path = file_name

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить скан: {str(e)}")

    def validate_form(self):
        if not self.fio_input.text():
            QMessageBox.warning(self, "Ошибка", "Введите ФИО")
            return False

        # Валидация телефона
        phone = self.phone_input.text()
        if phone and not re.match(r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}', phone):
            QMessageBox.warning(self, "Ошибка", "Неверный формат телефона")
            return False

        # Валидация email
        email = self.email_input.text()
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            QMessageBox.warning(self, "Ошибка", "Введите корректный email")
            return False

        if not self.note_input.toPlainText():
            QMessageBox.warning(self, "Ошибка", "Введите примечание")
            return False

        # Валидация паспортных данных
        if not self.passport_series.text() or not self.passport_number.text():
            QMessageBox.warning(self, "Ошибка", "Введите серию и номер паспорта")
            return False

        if not self.passport_scan_path:
            QMessageBox.warning(self, "Ошибка", "Выберите скан паспорта")
            return False

        return True

    def save_request(self):
        if not self.validate_form():
            return

        new_request = {
            "type": self.request_type,
            "date": self.date_input.date().toString("dd.MM.yyyy"),
            "department": self.dept_combo.currentText(),
            "employee": self.employee_combo.currentText(),
            "visitor": {
                "fio": self.fio_input.text(),
                "phone": self.phone_input.text(),
                "email": self.email_input.text(),
                "organization": self.org_input.text(),
                "note": self.note_input.toPlainText(),
                "birth_date": self.birth_input.date().toString("dd.MM.yyyy"),
                "passport": {
                    "series": self.passport_series.text(),
                    "number": self.passport_number.text()
                },
                "photo": self.photo_path,
                "passport_scan": self.passport_scan_path
            }
        }

        try:
            # Загрузка существующих данных
            with open('data/requests.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Добавление нового запроса
            data['requests'].append(new_request)

            # Сохранение обновленных данных
            with open('data/requests.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Успех", "Заявка успешно сохранена")
            self.clear_form()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить заявку: {str(e)}")

    def clear_form(self):
        self.fio_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.org_input.clear()
        self.note_input.clear()
        self.passport_series.clear()
        self.passport_number.clear()
        self.photo_label.clear()
        self.photo_label.setText("Фото не выбрано")
        self.passport_scan_label.clear()
        self.passport_scan_label.setText("Скан не выбран")
        self.photo_path = None
        self.passport_scan_path = None