from flask import Flask, render_template, Response
import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        return image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
	facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	font = cv2.FONT_HERSHEY_SIMPLEX

	while True:
		fr = camera.get_frame()

		flip_fr = cv2.flip(fr,1)
		gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
		faces = facec.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			fc = fr[y:y+h, x:x+w, :]
			gfc = cv2.cvtColor(fc, cv2.COLOR_BGR2GRAY)
			cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
			flip_fr = cv2.flip(fr,1)

		ret, jpeg = cv2.imencode('.jpg', fr)

		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.secret_key = 'mai_nahi_batata'
	app.debug = True
	app.run(host='localhost', port=5000)