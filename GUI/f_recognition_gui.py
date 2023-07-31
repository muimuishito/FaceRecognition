from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
from PySide6 import QtGui
from f_recognition.Workers.f_recognition_worker import FaceRecognitionWorker
from functools import partial
import sys



class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(660, 500)
        self.setWindowTitle("Identificación Facial")
        #self.setWindowIcon(QtGui.QIcon(r'..\Resources\ran.ico'))
        self.setWindowIcon(QtGui.QIcon(r'Resources\ran.ico')) #Compiler            
        self.create_window_form()
             
        
        
    @property
    def current_path(self):
        return self._current_path
    
    
    @current_path.setter
    def current_path(self, path):
        self._current_path = path     
        
       
    def create_window_form(self):
        self.user_container = QLabel()
        
        up_lo = QHBoxLayout()       
        up_lo.addWidget(self.user_container)       
        
        self.open_btn = QPushButton("Identificación Facial")
        self.open_btn.setFixedSize(400,30)
        self.open_btn.clicked.connect(self.take_f_recognition_worker)        
        
        down_lo = QHBoxLayout()
        down_lo.addWidget(self.open_btn)
                
        container_v_lo = QVBoxLayout()
        container_v_lo.addLayout(up_lo)
        container_v_lo.addLayout(down_lo)
        self.setLayout(container_v_lo)
        
        
    def stop_f_recognition_worker(self, obj):
        obj.stop()
        obj.deleteLater()   
      
        
    def multiple_data_message(self, title, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)        
        dlg.setMaximumHeight(600)           
        dlg.setText(str(message))        
        dlg.setIcon(QMessageBox.Critical)   
        dlg.show()
    
    
    def multiple_data_worker_message(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error en el sistema")        
        dlg.setMaximumHeight(600)            
        # Texto que se muestra dentro del cuadro de mensage
        dlg.setText(str(message))
        # Tipo de icono que se muestra en la cuadro de mensage
        dlg.setIcon(QMessageBox.Critical)      
        # Muestra el cuadro de mensage
        dlg.show()
    
   
    def image_update_slot(self, image):
        if isinstance(image, QtGui.QImage):
            self.user_container.setPixmap(QtGui.QPixmap.fromImage(image))
            self.user_container.setStyleSheet('''QLabel{ 
                                                border: 6px solid #ADD8E6;
                                                border-radius: 10%;
                                               }''')
    
    
    def take_f_recognition_worker(self):
        self.open_btn.setEnabled(False)
        #self.frw.open_camera()
        self.frw = FaceRecognitionWorker()    
        #self.frw.run() # DEBUG MODE
        self.frw.start()
        self.frw.image_emitted_signal.connect(self.image_update_slot)
        self.frw.finished.connect(partial(self.stop_f_recognition_worker, self.frw))
        self.frw.err.connect(self.multiple_data_worker_message)
    
    
    def closeEvent(self, event):
        close = QMessageBox.question(self, "Cerrar", "¿Está seguro de terminar el proceso?", QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
            try:                
                self.frw.release_camera()
                self.frw.stop()                
            except:
                pass                
        else:
            event.ignore()                    
             


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())