import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, 
    QTableWidget, QTableWidgetItem, QFileDialog, QWidget
)
from PyQt6.QtCore import Qt
from database import Database
from parser import parse_nota_dinas
from pdf_export import export_to_pdf
from excel_export import export_to_excel

class NotaDinasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Nota Dinas")
        self.setGeometry(100, 100, 800, 600)
        
        # Komponen UI
        self.upload_btn = QPushButton("Upload Nota Dinas")
        self.upload_btn.clicked.connect(self.upload_file)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Tanggal", "Pengirim", "Tempat", "Petugas"])
        self.table.setColumnHidden(0, True)  # Sembunyikan kolom ID
        
        self.download_excel_btn = QPushButton("Download Excel")
        self.download_excel_btn.clicked.connect(self.download_excel)
        
        self.download_pdf_btn = QPushButton("Download PDF")
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.table)
        layout.addWidget(self.download_excel_btn)
        layout.addWidget(self.download_pdf_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Database
        self.db = Database()
        self.load_data()
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Nota Dinas", "", 
            "PDF Files (*.pdf);;Word Files (*.docx)"
        )
        if file_path:
            try:
                data = parse_nota_dinas(file_path)
                self.db.insert_data(data)
                self.load_data()
            except Exception as e:
                print(f"Error: {e}")
    
    def load_data(self):
        data = self.db.get_all_data()
        self.table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            for col_idx, item in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
    
    def download_excel(self):
        data = self.db.get_all_data()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Simpan Excel", "", "Excel Files (*.xlsx)"
        )
        if filename:
            export_to_excel(data, filename)
    
    def download_pdf(self):
        data = self.db.get_all_data()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Simpan PDF", "", "PDF Files (*.pdf)"
        )
        if filename:
            export_to_pdf(data, filename)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotaDinasApp()
    window.show()
    sys.exit(app.exec())