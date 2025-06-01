from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit
import json, random, datetime

class EmulatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Эмулятор трафика")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.run_button = QPushButton("Запустить эмулятор")

        layout = QVBoxLayout()
        layout.addWidget(self.log_output)
        layout.addWidget(self.run_button)
        self.setLayout(layout)

        self.run_button.clicked.connect(self.run_emulation)

    def run_emulation(self):
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
            logs = []
            for user in random.sample(users, min(3, len(users))):
                action = random.choice(["пришел", "ушел"])
                log = f"{datetime.datetime.now().strftime('%H:%M:%S')} - {user['fio']} {action}"
                self.log_output.append(log)
                logs.append(log)
            with open("data/log.json", "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except:
            self.log_output.append("Ошибка при эмуляции.")