from signal import signal, SIGINT
import logging
import json
import redis
import cv2
import numpy as np


class Selfie:
    '''4.) Subscribe to the key "Bang", if a new number is published, take a picture
    from a webcam and "set" the image to the key "selfie" on redis.

    note: for testing this class, .redis_retrieve_selfie_and_save() can be used
    to retrieve and save the image from redis to the file system.
    '''

    def __init__(self, host: str = '127.0.0.1',
                 port: int = 6379,
                 password: str = None) -> None:

        self.host = host
        self.port = port
        self.password = password

        self._r_conn = None
        self._r_pubsub = None
        self._redis_connect_and_subcribe()
        self.is_listening = False

    def _redis_connect_and_subcribe(self):
        self._r_conn = redis.Redis(host=self.host,
                                   port=self.port,
                                   password=self.password)
        self._r_pubsub = self._r_conn.pubsub()

    def _redis_subscribe(self):
        logging.debug("subscribing to 'Bang' on redis")
        self._r_pubsub.subscribe('Bang')

    def _redis_unsubscribe(self):
        logging.debug("unsubscribing to 'Bang' on redis")
        self._r_pubsub.unsubscribe('Bang')

    def stop_listen_handle(self, signum, frame):
        '''handler for shutting down with ctrl-c'''
        self.stop_listening()

    def stop_listening(self):
        '''unsubscribe from 'Bang' and stop self.listen()'''
        self.is_listening = False
        self._r_pubsub.unsubscribe()

    def listen(self):
        '''4.) Subscribe to the key "Bang", if a new number is published, take a picture
        from a webcam and "set" the image to the key "selfie" on redis.
        '''
        self.is_listening = True
        signal(SIGINT, self.stop_listen_handle)

        self._redis_subscribe()
        for message in self._r_pubsub.listen():
            if message['type'] == 'message':
                if not self.is_listening:
                    break

                data = json.loads(message['data'])
                logging.debug(data)

                self._take_selfie()

    def _take_selfie(self):
        '''takes a selfie and the calls ._redis_set_selfie(img)'''
        logging.debug('getting selfie image from usb camera')

        cam = cv2.VideoCapture(0)   # 0 -> index of camera
        s, img = cam.read()
        if s:
            self._redis_set_selfie(img)

    def _redis_set_selfie(self, img):
        '''stores the image on redis
        https://gist.github.com/gachiemchiep/52f3255a81c907461c2c7ced6ede367a'''

        logging.debug("setting 'selfie' to new image")

        retval, buffer = cv2.imencode('.png', img)
        img_bytes = np.array(buffer).tostring()

        self._r_conn.set('selfie', img_bytes)

    def redis_retrieve_selfie_and_save(self, filepath='selfie_from_redis.png'):
        '''used to retrieve and save the
        image to the file system.
        '''
        logging.debug("retrieve 'selfie' from redis")

        encoded = self._r_conn.get('selfie')
        decoded = cv2.imdecode(np.frombuffer(encoded, np.uint8), 1)
        cv2.imwrite(filepath, decoded)
