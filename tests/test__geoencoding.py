#!/user/bin/python
# -*- coding: utf-8 -*-

from nose.tools import eq_
from geoencode import locate_with_google


def test_locate_success():
    addr = u"שבי ציון 14 אשדוד"
    loc = locate_with_google(addr)
    print(loc)
    eq_(str(loc['lng']), '34.6472683')
    eq_(str(loc['lat']), '31.8077975')

def test_locate_failure():
    addr = u"אין מקום כזה באמת, שום מקום"
    loc = locate_with_google(addr)
    print(loc)
    eq_(loc, False)
