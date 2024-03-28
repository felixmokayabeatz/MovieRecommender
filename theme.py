from PyQt5.QtWidgets import QRadioButton, QGroupBox, QFormLayout, QLabel
from PyQt5.QtGui import QPalette, QColor

def change_theme(parent, theme_label):
    palette = parent.palette()

    if parent.light_theme_button.isChecked():
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(255, 255, 255))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        
    else:
        # Dark theme
        palette.setColor(QPalette.Window, QColor(60, 70, 70))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 59, 59))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
      

    # Set palette for the entire application
    parent.setPalette(palette)

    # Update specific widgets
    parent.rating_input.setStyleSheet("color: {}; background-color: {}".format(palette.color(QPalette.WindowText).name(), palette.color(QPalette.Window).name()))
    parent.votes_input.setStyleSheet("color: {}; background-color: {}".format(palette.color(QPalette.WindowText).name(), palette.color(QPalette.Window).name()))
    parent.year_input.setStyleSheet("color: {}; background-color: {}".format(palette.color(QPalette.WindowText).name(), palette.color(QPalette.Window).name()))
    parent.button.setStyleSheet("color: {}; background-color: {}".format(palette.color(QPalette.ButtonText).name(), palette.color(QPalette.Button).name()))

    # Update the layout's style sheet to reflect the palette change
    parent.centralWidget().setStyleSheet("background-color: {}".format(palette.color(QPalette.Window).name()))

    # Update theme button text color
    parent.light_theme_button.setStyleSheet("color: {}".format(palette.color(QPalette.ButtonText).name()))
    parent.dark_theme_button.setStyleSheet("color: {}".format(palette.color(QPalette.ButtonText).name()))

def create_theme_selector(parent):
    theme_group = QGroupBox(parent)
    theme_layout = QFormLayout(theme_group)

    parent.light_theme_button = QRadioButton("Light Theme", parent)
    parent.light_theme_button.setChecked(True)
    theme_layout.addRow(parent.light_theme_button)

    parent.dark_theme_button = QRadioButton("Dark Theme", parent)
    theme_layout.addRow(parent.dark_theme_button)

    # Add a placeholder label to use later for checking the selected theme
    theme_label = QLabel(parent)
    theme_layout.addRow(theme_label)

    # Connect theme buttons to the change_theme function
    parent.light_theme_button.toggled.connect(lambda: change_theme(parent, theme_label))
    parent.dark_theme_button.toggled.connect(lambda: change_theme(parent, theme_label))

    return theme_group
