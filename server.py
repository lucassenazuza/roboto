import asyncio
import websockets
# ! /usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO
import time

# 17
# 18
# 27
# 22
UP = 17
DOWN = 18
LEFT = 27
RIGHT = 22
GPIO.setmode(GPIO.GPIO)
GPIO.setup(UP, GPIO.OUT)
GPIO.setup(DOWN, GPIO.OUT)
GPIO.setup(RIGHT, GPIO.OUT)
GPIO.setup(LEFT, GPIO.OUT)

connected = set()


async def server(websocket, path):
    # Register.
    connected.add(websocket)
    try:
        async for message in websocket:
            if (message == "up"):
                GPIO.output(UP, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(UP, GPIO.LOW)
                await websocket.send(f' recebido: {message}')
            elif (message == "down"):
                GPIO.output(DOWN, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(DOWN, GPIO.LOW)
                await websocket.send(f' recebido: {message}')
            elif (message == "left"):
                GPIO.output(LEFT, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(LEFT, GPIO.LOW)
                await websocket.send(f' recebido: {message}')
            elif (message == "right"):
                GPIO.output(RIGHT, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(RIGHT, GPIO.LOW)
                await websocket.send(f' recebido: {message}')
    finally:
        # Unregister.
        connected.remove(websocket)


start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
