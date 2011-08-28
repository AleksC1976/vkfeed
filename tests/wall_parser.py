#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests vk.com wall parser.'''

import unittest

from vkfeed.tools.wall_parser import WallPageParser, ParseError


class TestWallParser(unittest.TestCase):
    '''Tests vk.com wall parser.'''


    def setUp(self):
        self.__parser = WallPageParser()


    def test_invalid_page(self):
        '''Testing parsing of invalid page.'''

        self.assertRaises(ParseError, lambda:
            self.__parser.parse(open('wall_parser/invalid_page.html').read().decode('cp1251')))


    def test_group_wall(self):
        '''Testing parsing of group wall'''

        self.__test_parsing(
            open('wall_parser/group_profile_page.html').read().decode('cp1251'), {
                'user_name':  u'Хабрахабр',
                'user_photo': 'http://cs11159.vk.com/g20629724/a_ba3bb3dc.jpg',
                'posts':      10,
            }
        )


    def test_user_empty_wall(self):
        '''Testing parsing of empty wall'''

        self.__test_parsing(
            open('wall_parser/user_profile_page_with_empty_wall.html').read().decode('cp1251'), {
                'user_name':  u'Дмитрий Конищев',
                'user_photo': 'http://cs9567.vkontakte.ru/u122138358/a_4fd18ce6.jpg',
                'posts':      0,
            }
        )


    def test_user_wall(self):
        '''Testing parsing of user wall'''

        self.__test_parsing(
            open('wall_parser/user_profile_page.html').read().decode('cp1251'), {
                'user_name':  u'Павел Дуров',
                'user_photo': 'http://cs1495.vkontakte.ru/u00001/a_04766c4c.jpg',
                'posts':      10,
            }
        )


    def __test_parsing(self, html, etalon):
        '''Runs the test with the specified data.'''

        clear_run_data = self.__normalize_data(self.__parser.parse(html))
        self.assertEqual(etalon, clear_run_data)

        dirty_run_data = self.__normalize_data(self.__parser.parse(html))
        self.assertEqual(etalon, clear_run_data)
        self.assertEqual(etalon, dirty_run_data)


    def __normalize_data(self, data):
        '''Removes fields that don't exist in the etalon.'''

        if 'posts' in data:
            for post in data['posts']:
                self.assertNotEqual(post['text'].strip(), '')
            data['posts'] = len(data['posts'])

        return data



if __name__ == '__main__':
    # For test debugging
    #import logging
    #logging.getLogger().setLevel(logging.DEBUG)
    #logging.getLogger("vkfeed").addHandler(logging.StreamHandler())

    unittest.main()

