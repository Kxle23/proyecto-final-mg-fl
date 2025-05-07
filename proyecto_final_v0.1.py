from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QFileDialog, QTextEdit, QHBoxLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import shutil
import os
import sys
from datetime import datetime

class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Organizador de Archivos")
        self.setGeometry(100, 100, 700, 500)

        # Etiqueta de encabezado (reemplazo de la imagen)
        self.header_label = QLabel("Organizador de Archivos")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setFont(QFont("Arial", 18, QFont.Bold))

        # Etiqueta principal
        self.label = QLabel("Ingresa la ruta de la carpeta a organizar:")
        self.label.setFont(QFont("Arial", 12))

        # Campo de texto para ruta
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ejemplo: C:/Usuarios/TuUsuario/Descargas")

        # Botón de búsqueda
        self.browse_button = QPushButton("Buscar")
        self.browse_button.clicked.connect(self.browse_folder)

        # Botón para organizar archivos
        self.organize_button = QPushButton("Organizar Archivos")
        self.organize_button.clicked.connect(self.organize_files)

        # Botón para buscar archivos pesados
        self.heavy_files_button = QPushButton("Buscar Archivos Pesados")
        self.heavy_files_button.clicked.connect(self.find_heavy_files)

        # Cuadro de texto para mostrar resultados
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        # Layout horizontal para la ruta y el botón de búsqueda
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)

        # Layout horizontal para los botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.organize_button)
        buttons_layout.addWidget(self.heavy_files_button)
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.header_label)
        layout.addWidget(self.label)
        layout.addLayout(path_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.result_display)

        # Contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.path_input.setText(folder)

    def organize_files(self):
        folder_path = self.path_input.text().strip()
        if not folder_path or not os.path.exists(folder_path):
            self.label.setText("Por favor, ingresa una ruta válida.")
            return

        date_str = datetime.now().strftime("%Y-%m-%d")
        organization_folder = os.path.join(folder_path, f"Organización_{date_str}")
        os.makedirs(organization_folder, exist_ok=True)

        file_types = {
            "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
            "Imágenes": [".jpg", ".png", ".gif", ".bmp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar"],
            "Programas": [".exe", ".msi", ".dmg", ".apk"],
            "Otros": []
        }

        for category in file_types.keys():
            category_folder = os.path.join(organization_folder, category)
            os.makedirs(category_folder, exist_ok=True)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                moved = False
                for category, extensions in file_types.items():
                    if any(file.endswith(ext) for ext in extensions):
                        shutil.move(file_path, os.path.join(organization_folder, category, file))
                        moved = True
                        break
                if not moved:
                    shutil.move(file_path, os.path.join(organization_folder, "Otros", file))

        self.label.setText("Archivos organizados correctamente.")

    def find_heavy_files(self):
        folder_path = self.path_input.text().strip()
        if not folder_path or not os.path.exists(folder_path):
            self.label.setText("Por favor, ingresa una ruta válida.")
            return

        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    size = os.path.getsize(file_path)
                    files.append((file_path, size))
                except Exception:
                    continue

        files.sort(key=lambda x: x[1], reverse=True)

        result_text = "Archivos más pesados en la carpeta:\n\n"
        for file_path, size in files[:10]:
            result_text += f"{os.path.basename(file_path)} - {size / (1024*1024):.2f} MB\n"
            result_text += f"Ubicación: {os.path.dirname(file_path)}\n\n"

        self.result_display.setPlainText(result_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())
