import cv2
from flask import Flask, Response
from flask_sock import Sock

import RPi.GPIO as GPIO
import time
# ! /usr/bin/python
# -*- coding: utf-8 -*-

# 17
# 27
# 22
# 10
RIGHT_STRAIGHT = 27
RIGHT_REVERSE = 17
LEFT_REVERSE = 22
LEFT_STRAIGHT = 10


GPIO.setmode(GPIO.BCM)
GPIO.setup(RIGHT_STRAIGHT, GPIO.OUT)
GPIO.setup(RIGHT_REVERSE, GPIO.OUT)
GPIO.setup(LEFT_STRAIGHT, GPIO.OUT)
GPIO.setup(LEFT_REVERSE, GPIO.OUT)

connected = set()
app = Flask('__name__')
sock = Sock(app)
video = cv2.VideoCapture(0)


def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@sock.route("/sock")
def server(ws):
    while True:
        try:
            message = ws.receive()
            ws.send(f' recebido: {message}')
            if (message == "up"):
                GPIO.output(RIGHT_STRAIGHT, GPIO.HIGH)
                GPIO.output(LEFT_STRAIGHT, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(RIGHT_STRAIGHT, GPIO.LOW)
                GPIO.output(LEFT_STRAIGHT, GPIO.LOW)
                ws.send(f' recebido: {message}')
            elif (message == "down"):
                GPIO.output(RIGHT_REVERSE, GPIO.HIGH)
                GPIO.output(LEFT_REVERSE, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(RIGHT_REVERSE, GPIO.LOW)
                GPIO.output(LEFT_REVERSE, GPIO.LOW)
                ws.send(f' recebido: {message}')
            elif (message == "left"):
                GPIO.output(LEFT_STRAIGHT, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LEFT_STRAIGHT, GPIO.LOW)
                ws.send(f' recebido: {message}')
            elif (message == "right"):
                GPIO.output(RIGHT_STRAIGHT, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(RIGHT_STRAIGHT, GPIO.LOW)
                ws.send(f' recebido: {message}')
        except:
            print('erro na execu????o')
            connected.remove(ws)
            GPIO.cleanup()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
    video.release()
