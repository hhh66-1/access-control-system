from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
import json
import random
from datetime import datetime
import os

class EmulatorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_data()
        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_event)
        self.is_running = False

    def init_ui(self):
        layout = QVBoxLayout()

        title_label = QLabel("Эмулятор посещения")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Запустить")
        self.start_button.clicked.connect(self.toggle_emulator)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_log)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.clear_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def load_data(self):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as f:
                self.users = json.load(f)['users']

            with open('data/requests.json', 'r', encoding='utf-8') as f:
                self.requests = json.load(f)['requests']

            with open('data/log.json', 'r', encoding='utf-8') as f:
                self.logs = json.load(f)['logs']

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
            self.users = []
            self.requests = []
            self.logs = []

    def toggle_emulator(self):
        if not self.is_running:
            self.timer.start(5000)
            self.start_button.setText("Остановить")
            self.is_running = True
        else:
            self.timer.stop()
            self.start_button.setText("Запустить")
            self.is_running = False

    def generate_event(self):
        event_type = random.choice(['entry', 'exit'])
        
        if random.random() < 0.7:
            user = random.choice(self.users)
            name = user['full_name']
            is_employee = True
        else:
            if self.requests:
                request = random.choice(self.requests)
                name = request['visitor']['fio']
                is_employee = False
            else:
                return

        current_time = datetime.now().strftime("%H:%M:%S")
        
        if event_type == 'entry':
            message = f"[{current_time}] {'Сотрудник' if is_employee else 'Гость'} {name} вошел в здание"
        else:
            message = f"[{current_time}] {'Сотрудник' if is_employee else 'Гость'} {name} вышел из здания"

        self.log_text.append(message)

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": event_type,
            "name": name,
            "is_employee": is_employee
        }

        try:
            self.logs.append(log_entry)
            with open('data/log.json', 'w', encoding='utf-8') as f:
                json.dump({"logs": self.logs}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить лог: {str(e)}")

    def clear_log(self):
        self.log_text.clear()
        self.logs = []
        try:
            with open('data/log.json', 'w', encoding='utf-8') as f:
                json.dump({"logs": []}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось очистить лог: {str(e)}")