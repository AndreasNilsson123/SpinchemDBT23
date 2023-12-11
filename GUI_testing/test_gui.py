import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit

class NumpadApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a QLineEdit for displaying input/output
        self.input_display = QLineEdit(self)
        self.input_display.setReadOnly(True)

        # Create buttons for the numpad
        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3',
            '0', '.', '='
        ]

        # Create a layout
        layout = QVBoxLayout()

        # Add the input display to the layout
        layout.addWidget(self.input_display)

        # Create and add buttons to the layout
        for btn_text in buttons:
            btn = QPushButton(btn_text, self)
            btn.clicked.connect(lambda ch=btn_text: self.handle_button_click(ch))
            layout.addWidget(btn)

        # Set the layout for the main window
        self.setLayout(layout)

        self.setWindowTitle('Numpad Example')
        self.setGeometry(300, 300, 300, 400)

    def handle_button_click(self, button_text):
        current_text = self.input_display.text()

        # Handle button clicks
        if button_text == '=':
            try:
                result = eval(current_text)
                self.input_display.setText(str(result))
            except Exception as e:
                self.input_display.setText('Error')
        else:
            self.input_display.setText(current_text + button_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    numpad = NumpadApp()
    numpad.show()
    sys.exit(app.exec_())
