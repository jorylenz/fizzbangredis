#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from fizzbang import selfie


def main(args):
    ''' this starts listening for step 4
    
    4.) Subscribe to the key "Bang", if a new number is published, take a picture
    from a webcam and "set" the image to the key "selfie" on redis.
    '''
    logging.basicConfig(level=logging.DEBUG)

    selfie_client = selfie.Selfie(host='127.0.0.1',
                                 port=6379,
                                 password='super_secret')
    selfie_client.listen()


if __name__ == '__main__':
    main(sys.argv[1:])
