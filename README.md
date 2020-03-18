# fizzbangredis
Sample python module that uses redis and cv2

# If you have docker-compose installed and need a redis server
cd redis_docker/
./start_redis_container.sh

# To remove the installed container.
./remove_redis_container.sh

# For step 4 of the instructions
4.) Subscribe to the key "Bang", if a new number is published, take a picture
from a webcam and set the image to the key "selfie" on redis.

./run_selfie_subscribe.py

# For steps 1-3 of the instructions
1.) If the number is divisible by 3 "set" on redis the number which is
divisible by 3 to the key  "Fizz"

2.) If the number is divisible by 5 "publish" on redis the number which is
divisible by 5 to the key "Bang"

3.) If the number is divisible by 3 and 5 "set" on redis the number that is
divisible by both 3 and 5 to the key "FizzBang"

./run_fizzbang_runner.py

# To run tests
./run_tests.py
