"""Compact, readable application theme."""

STYLE = """
QMainWindow { background: #f4f7fb; }
QWidget { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #263449; }
QGroupBox { border: 1px solid #dce4ee; background: white; border-radius: 9px;
            margin-top: 15px; padding: 12px 9px 9px 9px; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; }
QLineEdit, QComboBox { border: 1px solid #cdd8e5; border-radius: 6px; padding: 6px;
                        background: white; min-height: 22px; }
QPushButton { border: 1px solid #cad5e4; border-radius: 6px; background: #ffffff;
              padding: 7px 13px; font-weight: 500; }
QPushButton:hover { background: #eaf2ff; }
QPushButton:disabled { color: #8895a4; background: #eff2f5; }
QPushButton#primary { background: #205cb4; color: white; border-color: #205cb4; }
QPushButton#primary:hover { background: #164e9c; }
QTableWidget { border: 1px solid #dce4ee; border-radius: 8px; background: white;
               alternate-background-color: #f5f8fd; gridline-color: #edf0f5; }
QHeaderView::section { background: #eef3f9; padding: 8px; border: 0;
                        border-bottom: 1px solid #dce4ee; font-weight: 600; }
QProgressBar { border: 1px solid #cdd8e5; border-radius: 5px; background: white; height: 16px; text-align: center; }
QProgressBar::chunk { background: #3278d0; border-radius: 4px; }
QStatusBar { background: #eaf0f7; }
QTextEdit { border: 1px solid #dce4ee; background: #fbfcfe; border-radius: 6px; }
"""
