import sys
import datetime
import json
import logging
import redis


class FizzBang:

    def __init__(self, host: str = '127.0.0.1',
                 port: int = 6379,
                 password: str = None) -> None:

        self.host = host
        self.port = port
        self.password = password
        self._r_conn = None
        self._redis_connect()

    def _redis_connect(self):
        logging.debug('FizzBang connecting to redis')
        self._r_conn = redis.Redis(host=self.host,
                                   port=self.port,
                                   password=self.password)

    def input(self, number: int) -> str:
        '''1.) If the number is divisible by 3 "set" on redis the number which is 
        divisible by 3 to the key  "Fizz"

        2.) If the number is divisible by 5 "publish" on redis the number which is 
        divisible by 5 to the key "Bang"

        3.) If the number is divisible by 3 and 5 "set" on redis the number that is 
        divisible by both 3 and 5 to the key "FizzBang"
        '''
        if not isinstance(number, int):
            raise TypeError('expects an int got a {}'.format(type(number)))

        if number % 3 == 0:
            if number % 5 == 0:
                self._redis_set('FizzBang', number)
                return 'FizzBang'
            self._redis_set('Fizz', number)
            return 'Fizz'

        if number % 5 == 0:
            self._redis_publish_bang(number)
            return 'Bang'

        return f'{number}'

    def _redis_set(self, key: str, value: int):
        if key not in ['Fizz', 'FizzBang']:
            raise ValueError("key must be in ['Fizz', 'FizzBang']")

        now = datetime.datetime.utcnow()
        r_value = json.dumps({'value': value, 'timestamp': str(now)})
        logging.debug(f"redis set '{key}' -> {r_value}")
        self._r_conn.set(key, r_value)

    def get_from_redis(self, key: str):
        value_json = self._r_conn.get(key)
        if value_json:
            value = json.loads(value_json)
            return value
        return None

    def _redis_publish_bang(self, value: int):
        key = 'Bang'
        logging.debug(f"redis publish '{key}' -> {value}")

        now = datetime.datetime.utcnow()
        r_value = json.dumps({'value': value, 'timestamp': str(now)})
        self._r_conn.publish(key, r_value)

class FizzBangRunner(FizzBang):

    def __init__(self, start: int = 1, end: int = 100,
                 host: str = '127.0.0.1',
                 port: int = 6379,
                 password: str = None) -> None:
        self.start: int = start
        self.end: int = end
        super().__init__(host=host, port=port, password=password)

    def set_range(self, start: int, end: int):
        self.start: int = start
        self.end: int = end

    def run(self):
        for i in range(self.start, self.end+1):
            fb: str = self.input(i)
            logging.debug(fb)
