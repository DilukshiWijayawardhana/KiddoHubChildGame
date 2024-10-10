from flask import Flask, render_template, Response, request
import cv2
import numpy as np
import os
import time
from pymongo import MongoClient
from datetime import datetime
import face_recognition
import pandas as pd
import pickle
import certifi


# from keras.models import model_from_json
# from keras.preprocessing import image
# import time
# from bson.objectid import ObjectId

app = Flask(__name__)

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_detection_times = {}  # Dictionary to store detection times for each face
        self.camera_on_time = None
        self.camera_off_time = None
        self.is_recognizing = False
        self.location = None

        # Load known faces
        known_faces_dir = 'C:\\Users\\SKY\\Desktop\\Coding\\KiddoHubChildGame\\Game\\Flask Server\\Babies'

        for person_folder in os.listdir(known_faces_dir):
            person_path = os.path.join(known_faces_dir, person_folder)
            if os.path.isdir(person_path):
                for filename in os.listdir(person_path):
                    image_path = os.path.join(person_path, filename)
                    image = face_recognition.load_image_file(image_path)
                    encoding = face_recognition.face_encodings(image)
                    if encoding:
                        encoding = encoding[0]
                        self.known_face_encodings.append(encoding)
                        self.known_face_names.append(person_folder)
                    else:
                        print(f"No face found in {filename}. Skipping...")

    def recognize_faces(self, frame):
        if not self.is_recognizing:
            return []

        start_time = time.time()
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            if self.known_face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                # If a match was found in known_face_encodings, use the name of that person
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                face_names.append(name)
            else:
                print("No known faces found. Please add known faces to proceed.")

            # Calculate detection time for each face
            end_time = time.time()
            detection_time = end_time - start_time
            if name not in self.face_detection_times:
                self.face_detection_times[name] = []
            self.face_detection_times[name].append(detection_time)

        return zip(face_locations, face_names)

    def start_recognition(self):
        self.is_recognizing = True
        self.camera_on_time = datetime.now()

    def end_recognition(self):
        self.is_recognizing = False
        self.camera_off_time = datetime.now()
        # Insert detection times for each face into MongoDB
        for name, times in self.face_detection_times.items():
            total_time = sum(times)
            data = {
                'name': name,
                'total_time': total_time,
                'date': datetime.now().strftime("%Y-%m-%d"),
                'camera_on_time': self.camera_on_time.strftime("%Y-%m-%d %H:%M:%S"),
                'camera_off_time': self.camera_off_time.strftime("%Y-%m-%d %H:%M:%S"),
                'location': self.location
            }
            collection.insert_one(data)
        self.face_detection_times = {}  # Reset detection times

fr = FaceRecognition()

# Connect to MongoDB
#client = MongoClient('mongodb+srv://airstudiolk:k479q8fxdWt8fro7@cluster0.am0uxk6.mongodb.net/?retryWrites=true&w=majority')
ca = certifi.where()
client = MongoClient('mongodb+srv://kamaldesilva919:LROBZuFIdDsZLVJj@childdaycare.zxlal0y.mongodb.net/?retryWrites=true&w=majority&appName=ChildDaycare', tlsCAFile=ca)
db = client['test']
collection = db['face_detection_dbs']

def gen_frames():
    video_capture = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame = video_capture.read()  # read the camera frame
        if not success:
            break
        else:
            # Recognize faces
            face_locations_with_names = fr.recognize_faces(frame)

            # Draw rectangles and names on the faces
            for (top, right, bottom, left), name in face_locations_with_names:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html', face_locations_with_names=[])

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    fr.start_recognition()
    return "Face recognition started."

@app.route('/end_recognition', methods=['POST'])
def end_recognition():
    fr.end_recognition()
    return "Face recognition ended and data sent to database."

@app.route('/send_to_db', methods=['POST'])
def send_to_db():
    fr.location = request.form['location']
    return "Location set for data collection."

# ------------------------Quize predict diluksi=hi----------------------
@app.route('/gamepredict', methods=['GET', 'POST'])
def quzesselect():

    v1 = int(request.args.get('v1'))
    v2 = int(request.args.get('v2'))
    v3 = int(request.args.get('v3'))
    
    

    df = pd.read_csv("child_knowledge_dataset.csv")
    df.head()

    inputs = df.drop('Knowledge_Level',axis='columns')
    target = df['Knowledge_Level']

    # from sklearn.preprocessing import LabelEncoder


    inputs.head()

    # inputs_n = inputs.drop(['Type','Quiz','status','previous ','p status'],axis='columns')
    # inputs_n

    from sklearn import tree

    model = tree.DecisionTreeClassifier()

    model.fit(inputs,target)

    model.score(inputs, target)

    output = model.predict([[v1,v2,v3]])
    # output = "test"
    
    # return output
    # return 'Player Status: {}'.format(output)
    return (format(output))
    # print(output)


    # ------------------------Loctaion predict Nipun----------------------
@app.route('/loactionPredict', methods=['GET', 'POST'])
def loactionPredict():

    v1 = int(request.args.get('v1'))
    v2 = int(request.args.get('v2'))
    v3 = int(request.args.get('v3'))
    
    

    df = pd.read_csv("child_interest_dataset.csv")
    df.head()

    inputs = df.drop('Interesting_location',axis='columns')
    target = df['Interesting_location']

    # from sklearn.preprocessing import LabelEncoder


    inputs.head()

    # inputs_n = inputs.drop(['Type','Quiz','status','previous ','p status'],axis='columns')
    # inputs_n

    from sklearn import tree

    model = tree.DecisionTreeClassifier()

    model.fit(inputs,target)

    model.score(inputs, target)

    output = model.predict([[v1,v2,v3]])
    # output = "test"
    
    # return output
    # return 'Player Status: {}'.format(output)
    return (format(output))
    # print(output)



    # ----------------Suran Emotion predict---------------------

#     collectionemo = db['setemotions']

# # Load emotion detection model
# model = model_from_json(open("fer.json", "r").read())
# model.load_weights('fer.h5')

# # Load face detection classifier
# face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# # Variable to keep track of process status
# process_running = False
# start_time = 0

# # Route to render the HTML template
# @app.route('/Emotion')
# def index():
#     return render_template('emotion.html')

# # Function to perform facial emotion analysis
# def detect_emotion_Emotion(frame):
#     global process_running, start_time

#     gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces
#     faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

#     for (x, y, w, h) in faces_detected:
#         if not process_running:
#             break

#         # Perform age and gender detection
#         face = frame[y:y+h, x:x+w]

#         # Preprocess face for emotion detection
#         roi_gray = gray_img[y:y+w, x:x+h]
#         roi_gray = cv2.resize(roi_gray, (48, 48))
#         img_pixels = image.img_to_array(roi_gray)
#         img_pixels = np.expand_dims(img_pixels, axis=0)
#         img_pixels /= 255

#         # Predict emotion
#         predictions = model.predict(img_pixels)
#         max_index = np.argmax(predictions[0])
#         emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
#         predicted_emotion = emotions[max_index]

#         # Perform age and gender detection
#         try:
#             result = DeepFace.analyze(face, actions=("age", "gender"))
#             age = result[0]["age"]
#             gender = result[0]["dominant_gender"]
#         except ValueError:
#             print("No face detected. Using last detected values for age and gender.")
#             age = "Unknown"
#             gender = "Unknown"

#         # Display information on the frame
#         cv2.putText(frame, f"Emotion: {predicted_emotion}, Age: {age}, Gender: {gender}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), thickness=7)

#     # Check if 30 seconds have passed and stop the process
#     if process_running and time.time() - start_time >= 30:
#         process_running = False

#         # Update the last detected values when the process ends
#         data = {
#             "emotion": predicted_emotion,
#             "age": age,
#             "gender": gender
#         }
#         update_query = {"_id": ObjectId("65eed93441c85413b54afc95")}
#         update_values = {"$set": data}
#         try:
#             collectionemo.update_one(update_query, update_values)
#             print("Data updated successfully")
#         except Exception as e:
#             print(f"Error updating data to MongoDB: {str(e)}")

#     return frame

# # Video streaming route
# def video_stream_Emotion():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = detect_emotion_Emotion(frame)

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()

# # Route to stream the video with information displayed
# @app.route('/video_feed_Emotion')
# def video_feed_Emotion():
#     return Response(video_stream_Emotion(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# # Route to start the process
# @app.route('/start_process_Emotion')
# def start_process_Emotion():
#     global process_running, start_time
#     process_running = True
#     start_time = time.time()  # Set the start time when the process starts
#     return 'Process started'

# # Route to end the process
# @app.route('/end_process_Emotion')
# def end_process_Emotion():
#     global process_running
#     process_running = False
#     return 'Process ended'

if __name__ == "__main__":
    app.run(debug=True)
