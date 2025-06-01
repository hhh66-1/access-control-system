from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import json

class GuestRequestForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заявка на пропуск")
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.reason_input = QLineEdit()
        self.submit_button = QPushButton("Отправить заявку")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Причина:"))
        layout.addWidget(self.reason_input)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)

        self.submit_button.clicked.connect(self.submit)

    def submit(self):
        data = {
            "name": self.name_input.text(),
            "email": self.email_input.text(),
            "reason": self.reason_input.text()
        }
        with open("data/requests.json", "r+", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except:
                all_data = []
            all_data.append(data)
            f.seek(0)
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        QMessageBox.information(self, "Готово", "Заявка отправлена.")
        self.name_input.clear()
        self.email_input.clear()
        self.reason_input.clear()