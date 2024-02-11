import sys
import os
import json
import re
try :
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel, QMenu, QGridLayout, QFileDialog
    from PyQt6.QtGui import QColor, QAction
    from PyQt6.QtCore import Qt, QStandardPaths
except :
    print("Error with PyOt6")
    print("Initiating PyQt5")
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QColorDialog, QLabel, QMenu, QGridLayout, QAction, QFileDialog
    from PyQt5.QtGui import QColor
    from PyQt5.QtCore import Qt, QStandardPaths

class ColorPaletteApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.color_palette = []  # List to store color values
        self.color_widgets = []  # List to store color widgets

        self.initUI()
        
    def import_colors_from_files(self):
        file_dialog = QFileDialog(self)
        files, _ = file_dialog.getOpenFileNames(self, "Select Files to Import Colors", "", "Text Files (*.css *.json *js *html *jsx *ts *tsx);;All Files (*)")

        for file_path in files:
            self.scan_and_import_colors(file_path)

    def scan_and_import_colors(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()

                # Extract color codes using regular expression
                color_codes = re.findall(r'#(?:[0-9a-fA-F]{3}){1,2}\b', content)

                for code in color_codes:
                    color = QColor(code)
                    self.color_palette.append(color)
                    self.add_color_to_ui(color)

        except (FileNotFoundError, PermissionError, UnicodeDecodeError):
            print(f"Error scanning and importing colors from {file_path}")


    def initUI(self):
        # Set up the main window
        self.setWindowTitle("Color Palette")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.color_layout = QGridLayout()
        self.options_layout = QGridLayout()

        self.layout.addLayout(self.options_layout)
        self.layout.addLayout(self.color_layout)
        
        # + button
        self.add_color_button = QPushButton("+")
        self.add_color_button.setMaximumWidth(50)
        self.add_color_button.setMaximumHeight(50)
        self.add_color_button.setStyleSheet("font-size: 20px;")
        self.add_color_button.clicked.connect(self.show_color_dialog)
        self.options_layout.addWidget(self.add_color_button, 0, 0)
 
        # New button
        self.add_new_button = QPushButton("New")
        self.add_new_button.setMaximumWidth(100)
        self.add_new_button.setMaximumHeight(50)
        self.add_new_button.setStyleSheet("font-size: 20px;")
        self.add_new_button.clicked.connect(self.clean_layout)
        self.options_layout.addWidget(self.add_new_button, 0, 1)

        # Save button
        self.add_save_button = QPushButton("Save")
        self.add_save_button.setMaximumWidth(100)
        self.add_save_button.setMaximumHeight(50)
        self.add_save_button.setStyleSheet("font-size: 20px;")
        self.add_save_button.clicked.connect(self.save_color_palette)
        self.options_layout.addWidget(self.add_save_button, 0, 2)

        # Load button
        self.add_load_button = QPushButton("Load")
        self.add_load_button.setMaximumWidth(100)
        self.add_load_button.setMaximumHeight(50)
        self.add_load_button.setStyleSheet("font-size: 20px;")
        self.add_load_button.clicked.connect(self.load_color_palette)
        self.options_layout.addWidget(self.add_load_button, 0, 3)

        # Import button
        self.import_colors_button = QPushButton("Import")
        self.import_colors_button.setMaximumWidth(100)
        self.import_colors_button.setMaximumHeight(50)
        self.import_colors_button.setStyleSheet("font-size: 20px;")
        self.import_colors_button.clicked.connect(self.import_colors_from_files)
        self.options_layout.addWidget(self.import_colors_button, 0, 4)

    def show_color_dialog(self):
        # Show a color dialog to select a color
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()

        if color.isValid():
            self.color_palette.append(color)
            self.add_color_to_ui(color)

    def add_color_to_ui(self, color):
        # Add a color to the user interface
        color_widget = QWidget()

        color_block = QLabel()
        color_block.setMaximumSize(200, 200)
        color_block.setMinimumSize(100, 100)
        color_block.setStyleSheet(f"background-color: {color.name()}; border-radius: 10px;")

        hex_label = QLabel(color.name())
        hex_label.setStyleSheet("font-size: 20px;")

        color_layout = QVBoxLayout()
        color_layout.addWidget(hex_label)
        color_layout.addWidget(color_block)
        color_widget.setLayout(color_layout)

        row = (len(self.color_palette) - 1) // 2
        col = (len(self.color_palette) - 1) % 2

        self.color_layout.addWidget(color_widget, row, col)
        self.color_widgets.append(color_widget)

        def context_menu_handler(event):
            # Handle right-click context menu for color items
            if event.button() == Qt.MouseButton.RightButton:
                context_menu = QMenu(self)
                hex_action = context_menu.addAction("Copy HEX")
                rgb_action = context_menu.addAction("Copy RGBA")
                remove_action = context_menu.addAction("Remove Color")

                hex_action.triggered.connect(lambda: self.copy_to_clipboard(color.name()))
                rgb_action.triggered.connect(lambda: self.copy_to_clipboard(str(color.getRgb())))
                remove_action.triggered.connect(lambda: self.remove_color(color, color_widget))

                context_menu.exec(event.globalPosition().toPoint())
            elif event.button() == Qt.MouseButton.LeftButton:
                self.copy_to_clipboard(color.name())

        color_widget.mousePressEvent = context_menu_handler

    def copy_to_clipboard(self, value):
        # Copy a value to the clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(value)

    def clean_layout(self):
        # removes all the colors from the layout
        # a new empty layout
        for i in reversed(range(self.color_layout.count())): 
                widget = self.color_layout.itemAt(i).widget()
                if widget: widget.deleteLater()
            
        self.color_widgets = []
        self.color_palette = []

    def remove_color(self, color, color_widget):
        # Remove a color from the palette and UI
        self.color_palette.remove(color)
        self.color_widgets.remove(color_widget)
        color_widget.deleteLater()
        self.update_color_layout()

    def update_color_layout(self):
        # Update the color layout after removing a color
        temp_palette = []
        temp_widgets = []
        for i in reversed(range(self.color_layout.count())):
            widget = self.color_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        temp_palette.extend(self.color_palette)
        temp_widgets.extend(self.color_widgets)

        self.color_palette.clear()
        self.color_widgets.clear()

        for color, widget in zip(temp_palette, temp_widgets):
            self.color_palette.append(color)
            self.add_color_to_ui(color)

    def save_session_data(self, path = None):
        # Save the session data (color palette) to a JSON file
        if path :
            session_data_path = path
        else : 
            session_data_path = self.get_session_data_path()

        data = [color.name() for color in self.color_palette]
        with open(session_data_path, 'w') as f:
            json.dump(data, f)

    def get_session_data_path(self):
        # Get the path for storing session data (JSON file)
        documents_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        app_data_dir = os.path.join(documents_dir, "ColorPalette_data")
        os.makedirs(app_data_dir, exist_ok=True)
        return os.path.join(app_data_dir, "session_data.json")

    def load_session_data(self, path = None):
        # Load session data (color palette) from a JSON file
        if path :
            session_data_path = path
        else:
            session_data_path = self.get_session_data_path()

        if path : # if a specified path is given to load 
                  # clean the layout
            self.clean_layout()

        try:
            with open(session_data_path, 'r') as f:
                data = json.load(f)
                for color in data:
                    self.color_palette.append(QColor(color))
                    self.add_color_to_ui(QColor(color))
        except (FileNotFoundError, json.JSONDecodeError):
            print("An Error While Loading the Color Palette")

    def save_color_palette(self):
        # save the instance of color palette into a json file at specified path
        save_path = QFileDialog.getSaveFileName(self, "Save Color palette", self.get_session_data_path(), 'All Files (*.*)')

        if save_path != ("", "") :
            self.save_session_data(path = save_path[0])

    def load_color_palette(self):
        # load the color palette data fom a specified json file
        load_path = QFileDialog.getOpenFileName(self, "Save Color palette", self.get_session_data_path(), 'JSON (*.json)')

        if load_path != ("", "") :
            self.load_session_data(path = load_path[0])

    def closeEvent(self, event):
        # Save session data and close the application
        self.save_session_data()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = ColorPaletteApp()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
