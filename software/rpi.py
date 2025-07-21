# import time
# import cv2
# import os
# import pyrebase
# from datetime import datetime
# import numpy as np
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.base import MIMEBase
# from email import encoders
# import speech_recognition as sr
# from gtts import gTTS
# import threading

# temp, humi, gas = 0,0,0
# recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('trainer/trainer.xml')
# cascadePath = "haarcascade_frontalface_default.xml"
# faceCascade = cv2.CascadeClassifier(cascadePath);
# font = cv2.FONT_HERSHEY_SIMPLEX

# config = {
#   "apiKey": "AIzaSyCo-xvqOvHEhDJ_s0prAaZwwSa-ZibziKU",
#   "authDomain": "final-project-439bc.firebaseapp.com",
#   "databaseURL": "https://final-project-439bc-default-rtdb.asia-southeast1.firebasedatabase.app",
#   "storageBucket": "final-project-439bc.firebasestorage.app"
# }
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
# def listener1(mess):
#     global temp
#     temp = mess["data"]
# def listener2(mess):
#     global humi
#     humi = mess["data"]
# def listener3(mess):
#     global gas
#     gas = mess["data"]
# db.child("Temperature").stream(listener1)
# db.child("Humidity").stream(listener2)
# db.child("Gas").stream(listener3)

# # Gửi email kèm theo ảnh
# def send_email_with_image(sender_email, password, receiver_email, subject, body, attachment_path):
#     # Tạo email
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject

#     # Thêm nội dung email
#     msg.attach(MIMEText(body, 'plain'))
    
#     if attachment_path != None:
#         # Thêm ảnh đính kèm
#         with open(attachment_path, "rb") as attachment:
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(attachment.read())

#         encoders.encode_base64(part)
#         part.add_header(
#             "Content-Disposition",
#             f"attachment; filename={os.path.basename(attachment_path)}",
#         )
#         msg.attach(part)

#     # Gửi email
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, password)
#         server.send_message(msg)
#         print("Email đã được gửi thành công!")
#     except Exception as e:
#         print(f"Gửi email thất bại: {e}")
#     finally:
#         server.quit()

# sender_email = "bktech0524@gmail.com"
# password = "rmdm tlal paqp ohmj"
# receiver_email = "daotran0940@gmail.com"
# subject = "Cảnh báo có người lạ"
# body = "Đây là ảnh chụp từ Camera"
# image_path = "warning.jpg"
# #************************************************

# def speak(text):
#     tts = gTTS(text=text, lang='vi')
#     tts.save("output.mp3")
#     os.system("mpg321 output.mp3")
    
# def listen_for_command():
#     global temp, humi, gas
#     #viet lai
#     recognizer = sr.Recognizer()
#     while True:
#         with sr.Microphone() as source:
#             print("Assistant: Đang lắng nghe...")
#             try:
#                 audio = recognizer.listen(source, timeout=1)  # Lắng nghe trong 3 giây
#                 command = recognizer.recognize_google(audio, language="vi-VN")  # Nhận diện tiếng Việt
#                 print(f"Bạn nói: {command}")
#                 if "nhiệt độ hiện tại là bao nhiêu" in command.lower():
#                     speak(f"Nhiệt độ hiện tại là {temp} độ C")
#                 if "độ ẩm hiện tại là bao nhiêu" in command.lower():
#                     speak(f"Độ ẩm hiện tại là {humi} %")
#                 if "nồng độ khí ga là bao nhiêu" in command.lower():
#                     speak(f"Nồng độ khí ga hiện tại là {gas} %")
#                 if "bật đèn" in command.lower():
#                     db.child("Light").set("1")
#                     speak("Đèn đang bật")
#                 if "tắt đèn" in command.lower():
#                     db.child("Light").set("0")
#                     speak("Đèn đang tắt")
#                 if "chế độ tự động" in command.lower():
#                     db.child("Light").set("-1")
#                     speak("Chế độ tự động theo cảm biến chuyển động và hẹn giờ")
#                 if "mở cửa" in command.lower():
#                     db.child("Control").set("1")
#                     speak("Cửa đang mở")
#                 if "đóng cửa" in command.lower():
#                     db.child("Control").set("0")
#                     speak("Cửa đang đóng")
#             except sr.UnknownValueError:
#                 print("Assistant: Không hiểu bạn nói gì.")
#             except sr.WaitTimeoutError:
#                 print("Assistant: Không nhận được âm thanh.")
#                 #ket thuc viet lai

# def display_camera():
#     global temp, humi, gas
#     ckTemp, ckGas = 0,0
#     cap = cv2.VideoCapture(0)
#     cnt1,cnt2 = 0,0

#     while True:
#         ########################################################################
#         # dieu kien de nguong canh bao
#         if temp > 40 and ckTemp==0:
#             ckTemp = 1
#             speak("Cảnh báo nhiệt độ cao")
#             send_email_with_image(sender_email, password, receiver_email, "Cảnh báo nhiệt độ cao", f"Nhiệt độ cao: {temp}", None)
#         if temp < 35 and ckTemp==1:
#             ckTemp = 0
#         if gas > 5 and ckGas==0:
#             ckGas = 1
#             speak("Cảnh báo nồng độ khí ga cao")
#             send_email_with_image(sender_email, password, receiver_email, "Cảnh báo Nồng độ khí gas cao", f"Nồng độ khí gas cao: {gas}", None)
#         if gas < 3 and ckGas==1:
#             ckGas = 0
#         ########################################################################
        
#         _, image =cap.read()
#         gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#         faces = faceCascade.detectMultiScale(gray, 1.3,5)
#         if len(faces)>0:
#             for (x,y,w,h) in faces:
#                 roi_gray = gray[y:y + h, x:x + w]
#                 cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
#                 id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
#                 print(confidence)
#                 if confidence<50:
#                     cnt1 += 1
#                     nameid = str(id)
#                     confidence = "  {0}%".format(round(100 - confidence))
#                 else:
#                     cnt2 += 1
#                     nameid = "unknown"
#                     confidence = "  {0}%".format(round(100 - confidence))
                
#                 cv2.putText(image, f"{nameid} {confidence}", (x, y-10), font, 1, (0,255,0), 2)  
#         else:
#             cnt1,cnt2 = 0,0
            
#         if cnt1 > 15:
#             db.child("Control").set("1")
#             cnt1,cnt2 = 0,0
#         if cnt2 > 15:
#             cv2.imwrite("warning.jpg", image)
#             db.child("Control").set("-1")
#             send_email_with_image(sender_email, password, receiver_email, subject, body, image_path)
#             cnt1,cnt2 = 0,0
#         cv2.imshow('im',image) 
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# thread1 = threading.Thread(target=listen_for_command)
# thread2 = threading.Thread(target=display_camera)
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()

from graphviz import Digraph

def generate_flowchart():
    dot = Digraph(comment="Updated Flowchart")

    # Start Point
    dot.node("Start", "Bắt đầu hành động", shape="ellipse")

    # Home Navigation
    dot.node("Home", "Trang Home", shape="box")
    dot.node("ReadDB", "Đọc Realtime Database / Firestore Database", shape="parallelogram")
    dot.node("ValidateData", "Dữ liệu từ Database hợp lệ?", shape="diamond")
    dot.node("UpdateUI", "Cập nhật giao diện", shape="box")
    dot.node("ControlDevices", "Điều khiển đèn (cửa)", shape="box")
    dot.node("TimeCheck", "Đúng thời gian?", shape="diamond")
    dot.node("UpdateDB", "Cập nhật \"0\" hoặc \"1\" về Database", shape="parallelogram")

    # Settings Navigation
    dot.node("Settings", "Trang Setting", shape="box")
    dot.node("ReadFirestore", "Đọc Firestore Database", shape="parallelogram")
    dot.node("AddUser", "Thêm tài khoản người dùng", shape="box")
    dot.node("ValidateUser", "Thông tin tài khoản hợp lệ không?", shape="diamond")
    dot.node("RegisterScreen", "Gọi màn hình đăng ký", shape="box")
    dot.node("Error", "Báo lỗi", shape="box")

    # Logout
    dot.node("Logout", "Đăng xuất", shape="diamond")
    dot.node("ClearSession", "Xóa dữ liệu phiên", shape="box")
    dot.node("LoginScreen", "Gọi màn hình đăng nhập", shape="box")

    # End Point
    dot.node("End", "Kết thúc hành động", shape="ellipse")

    # Transitions
    dot.edges([("Start", "Home"),
               ("Home", "ReadDB"),
               ("ReadDB", "ValidateData"),
               ("ValidateData", "UpdateUI", "S"),
               ("ValidateData", "Error", "Đ"),
               ("UpdateUI", "ControlDevices"),
               ("ControlDevices", "TimeCheck"),
               ("TimeCheck", "UpdateDB", "S"),
               ("TimeCheck", "Error", "Đ"),
               ("Home", "Settings"),

               ("Settings", "ReadFirestore"),
               ("Settings", "AddUser"),
               ("AddUser", "ValidateUser"),
               ("ValidateUser", "RegisterScreen", "S"),
               ("ValidateUser", "Error", "Đ"),
               ("Settings", "Logout"),

               ("Logout", "ClearSession", "S"),
               ("Logout", "LoginScreen", "Đ"),
               ("ClearSession", "LoginScreen"),

               ("UpdateDB", "End"),
               ("Error", "End"),
               ("LoginScreen", "End")])

    return dot

# Generate and save the flowchart
dot = generate_flowchart()
dot.render("updated_flowchart", format="png", cleanup=True)
