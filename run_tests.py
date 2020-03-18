#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from fizzbang.fizzbang import FizzBang


class Test(unittest.TestCase):
    '''Testing for the fizzbang module
    todo: test publish Bang and test selfie
    '''
    def test_0_input(self):
        print('Start FizzBang fb.input(n) test.')

        fb = FizzBang(host='127.0.0.1', port=6379, password='super_secret')

        # set
        self.assertEqual(fb.input(3), 'Fizz', "Should be 'Fizz'")
        value = fb.get_from_redis('Fizz')
        self.assertIsInstance(value, dict, "should be type 'dict'")
        self.assertEqual(value['value'], 3, 'should be value 3')

        # publish
        self.assertEqual(fb.input(5), 'Bang', "Should be 'Bang'")

        # set
        self.assertEqual(fb.input(15), 'FizzBang', "Should be 'FizzBang'")
        value = fb.get_from_redis('FizzBang')
        self.assertIsInstance(value, dict, "should be type 'dict'")
        self.assertEqual(value['value'], 15, 'should be value 15')

        # nothing to redis
        self.assertEqual(fb.input(2), '2', "Should be '2'")

        # cannot input None
        self.assertRaises(TypeError, fb.input, None)

        print('Finished FizzBang fb.get(n) test.')


if __name__ == '__main__':
    unittest.main()
