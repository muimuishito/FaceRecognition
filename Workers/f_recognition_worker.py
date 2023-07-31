from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage
import cv2
import numpy as np
import face_recognition
import os
from pathlib import Path
from f_recognition.Configurations.CreateConfigurationFiles.config_camera_reader_helper import read_camara_config



class FaceRecognitionWorker(QThread):
    
    camara_config = read_camara_config()
    image_emitted_signal = Signal(QImage)
    err = Signal(object) 
    _ThreadActive = True
    
    cap = cv2.VideoCapture(int(camara_config['CamaraConfig']['camara']), cv2.CAP_DSHOW)
   
    img_folder = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\UserImg')
    
    # Verifica si no existe la carpeta de imágenes
    if not img_folder.exists():
    # Crea la carpeta para almacenar las imágenes
        img_folder.mkdir(exist_ok=False, parents=True)
    
    imgs = []
    class_name = []
    img_list = os.listdir(img_folder)
        
    for im in img_list:        
        curr_img = cv2.imread(f'{img_folder}/{im}')
        imgs.append(curr_img)
        class_name.append(os.path.splitext(im)[0]) 

    
    def find_encodings(images):    
        encode_list = []        
        for image in images:
            try:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)            
                encode = face_recognition.face_encodings(img)
                if len(encode) > 0:
                    encode = encode[0]
                else:
                    raise ValueError("No se encontraron rostros")    
                encode_list.append(encode)
            except:
                pass    
        return encode_list   
    
    encode_list_known = find_encodings(imgs)
       
    def run(self):    
        try:                      
            while self._ThreadActive:
                success, img = self.cap.read()                
                if success == False:
                    break
                img_small = cv2.resize(img, (0,0), None, 0.25, 0.25)
                img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
                
                face_current_frame = face_recognition.face_locations(img_small, number_of_times_to_upsample=2)
                encodes_current_frame = face_recognition.face_encodings(img_small, face_current_frame)
                
                for encode_face, face_location in zip(encodes_current_frame, face_current_frame):
                    matches = face_recognition.compare_faces(self.encode_list_known, encode_face, tolerance=0.4)
                    face_dist = face_recognition.face_distance(self.encode_list_known, encode_face)
                            
                    match_index = np.argmin(face_dist)
                    
                    if matches[match_index]:
                        
                        name = self.class_name[match_index].split(' ')[0]
                        
                        y1,x2,y2,x1 = face_location
                        y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, .5, (255, 255, 255), 2)
                        
                rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                         
                convert_to_qt_format = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                #scaled_frame = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_emitted_signal.emit(convert_to_qt_format)

                # cv2.imshow('WebCam', img)
                # if cv2.waitKey(1) == 27:
                #     break  
                
        except Exception:           
            self.err.emit(ValueError("Error en las imagenes de rostros"))
            
        
       
    def open_camera(self):
        if not self.cap.isOpened():
            self.cap.open(0)            
    
    
    def release_camera(self):        
        if self.cap.isOpened():
            self.cap.release()
              
        
    def stop(self):                
        self.ThreadActive = False        
        if self.isRunning():
            self.quit()        
            self.wait()


    


         


    
# if __name__ == '__main__':
#     wtp = FaceRecognitionWorker()    
#     wtp.run()
      
        
   
