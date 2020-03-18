#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
from fizzbang import fizzbang


def main(args):
    '''this will loop through a range of integers and pass them to FizzBang
    to be processed. 

    note: run run_selfie_subscribe.py before this for step 4.
    '''
    logging.basicConfig(level=logging.DEBUG)

    fbr = fizzbang.FizzBangRunner(start=1, end=100,
                                        host='127.0.0.1',
                                        port=6379,
                                        password='super_secret')
    fbr.run()


if __name__ == '__main__':
    main(sys.argv[1:])
