#Importación de elementos gráficos básicos de PySide6
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel,
    QLineEdit, QFileDialog, QTextEdit, QHBoxLayout, QMessageBox
)

#QFont se usa para cambiar el tipo y tamaño de letra, aparece muy poco en las guías, pero se puede mantener si se simplifica
from PySide6.QtGui import QFont, QIcon, QPixmap

#Qt tiene constantes útiles como la alineación centrada
from PySide6.QtCore import Qt

#Módulos del sistema para trabajar con carpetas y archivos
import shutil
import os
import sys
from datetime import datetime

#Creamos una clase para la ventana principal
class FileOrganizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OrgaFile")
        self.setGeometry(100, 100, 700, 500)
        self.window_icon = QPixmap("assets/window_icon.png")
        self.setWindowIcon(self.window_icon)

        #Estilos avanzados con colores y bordes redondeados
        self.setStyleSheet("background-color: #2E3440; color: #D8DEE9; font-size: 14px;")

        #Imagen (icono centrado) con QPixmap
        self.header_label = QLabel()
        pixmap = QPixmap("assets/orgafile.png")  #Se carga una imagen para mostrar arriba
        if not pixmap.isNull():
            pixmap = pixmap.scaled(pixmap.width()/10, pixmap.height()/10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.header_label.setPixmap(pixmap)
        self.header_label.setAlignment(Qt.AlignCenter)

        #Etiqueta que indica al usuario qué debe hacer
        self.label = QLabel("Ingresa la ruta de la carpeta a organizar:")
        self.label.setFont(QFont("Arial", 12))  #Se usa QFont

        #Campo de entrada de texto
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ejemplo: C:/Usuarios/TuUsuario/Descargas")
        self.path_input.setStyleSheet("background-color: #4C566A; color: white; border-radius: 5px; padding: 5px;")

        #Botón con icono
        self.browse_button = QPushButton()
        self.browse_button.setIcon(QIcon("assets/search_icon.png"))  #QIcon con imagen
        self.browse_button.setStyleSheet("background-color: #88C0D0; border-radius: 5px; padding: 5px;")
        self.browse_button.clicked.connect(self.browse_folder)

        #Botón para organizar archivos
        self.organize_button = QPushButton("Organizar Archivos")
        self.organize_button.setStyleSheet("background-color: #A3BE8C; color: black; border-radius: 5px; padding: 5px;")
        self.organize_button.clicked.connect(self.organize_files)

        #Botón para buscar archivos pesados
        self.heavy_files_button = QPushButton("Buscar Archivos Pesados")
        self.heavy_files_button.setStyleSheet("background-color: #EBCB8B; color: black; border-radius: 5px; padding: 5px;")
        self.heavy_files_button.clicked.connect(self.find_heavy_files)

        #Cuadro de texto donde se mostrarán los resultados
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("background-color: #3B4252; color: white; border-radius: 5px; padding: 5px;")

        #Layout horizontal para agrupar campo de ruta y botón de búsqueda
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_button)

        #Layout horizontal para los botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.organize_button)
        buttons_layout.addWidget(self.heavy_files_button)
        buttons_layout.setSpacing(20)
        buttons_layout.setAlignment(Qt.AlignCenter)

        #Layout principal vertical
        layout = QVBoxLayout()
        layout.addWidget(self.header_label)
        layout.addWidget(self.label)
        layout.addLayout(path_layout)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.result_display)

        #Contenedor y configuración final de la ventana
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    #Esta función abre el explorador para seleccionar carpeta
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.path_input.setText(folder)

    #Esta función organiza los archivos en carpetas según su tipo
    def organize_files(self):
        #Obtiene la ruta a organizar
        folder_path = self.path_input.text().strip()
        if not folder_path or not os.path.exists(folder_path):
            self.label.setText("Por favor, ingresa una ruta válida.")
            return

        #Crea la carpeta donde se hará la organización
        date_str = datetime.now().strftime("%Y-%m-%d")
        organization_folder = os.path.join(folder_path, f"Organización_{date_str}")
        os.makedirs(organization_folder, exist_ok=True)

        #Extensiones de los archivos ordenados por categorías
        file_types = {
            "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
            "Imágenes": [".jpg", ".png", ".gif", ".bmp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov"],
            "Comprimidos": [".zip", ".rar", ".7z", ".tar"],
            "Programas": [".exe", ".msi", ".dmg", ".apk"],
            "Otros": []
        }

        #Crea una carpeta por cada categoría
        for category in file_types.keys():
            category_folder = os.path.join(organization_folder, category)
            os.makedirs(category_folder, exist_ok=True)

        #Mueve cada archivo en su carpeta correspondiente
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

        #Notifica al usuario que los archivos fueron organizados
        QMessageBox.information(self,"OrgaFIle","Archivos organizados correctamente.")

    #Esta función busca los 10 archivos más pesados en la carpeta
    def find_heavy_files(self):
        #Obtiene la ruta con la cual trabajar
        folder_path = self.path_input.text().strip()
        if not folder_path or not os.path.exists(folder_path):
            self.label.setText("Por favor, ingresa una ruta válida.")
            return

        #Explora la ruta de la carpeta para obtener la ruta de cada archivo y su tamaño
        files = []
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                try:
                    size = os.path.getsize(file_path)
                    files.append((file_path, size))
                except Exception:
                    continue
        
        #Ordena los archivos de mayor a menor
        files.sort(key=lambda x: x[1], reverse=True)

        #Aquí se usa HTML para mostrar colores y formato
        result_text = "<b>Archivos más pesados en la carpeta:</b><br>"
        for file_path, size in files[:10]:
            result_text += f"<p><b>{os.path.basename(file_path)}</b> "
            result_text += f"<span style='color: #EBCB8B;'>- {size / (1024*1024):.2f} MB</span><br>"
            result_text += f"<span style='color: #88C0D0;'>Ubicación: {os.path.dirname(file_path)}</span></p>"

        #Muestra la información en la pantalla
        self.result_display.setHtml(result_text)

#Punto de entrada del programa: inicia la app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizer()
    window.show()
    sys.exit(app.exec())
