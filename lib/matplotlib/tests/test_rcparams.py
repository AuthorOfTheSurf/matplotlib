from __future__ import absolute_import, division, print_function, unicode_literals

import six

import os

import matplotlib as mpl
from matplotlib.tests import assert_str_equal


mpl.rc('text', usetex=False)
mpl.rc('lines', linewidth=22)

fname = os.path.join(os.path.dirname(__file__), 'test_rcparams.rc')

def test_rcparams():

    usetex = mpl.rcParams['text.usetex']
    linewidth = mpl.rcParams['lines.linewidth']

    # test context given dictionary
    with mpl.rc_context(rc={'text.usetex': not usetex}):
        assert mpl.rcParams['text.usetex'] == (not usetex)
    assert mpl.rcParams['text.usetex'] == usetex

    # test context given filename (mpl.rc sets linewdith to 33)
    with mpl.rc_context(fname=fname):
        assert mpl.rcParams['lines.linewidth'] == 33
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test context given filename and dictionary
    with mpl.rc_context(fname=fname, rc={'lines.linewidth': 44}):
        assert mpl.rcParams['lines.linewidth'] == 44
    assert mpl.rcParams['lines.linewidth'] == linewidth

    # test rc_file
    try:
        mpl.rc_file(fname)
        assert mpl.rcParams['lines.linewidth'] == 33
    finally:
        mpl.rcParams['lines.linewidth'] = linewidth


def test_RcParams_class():
    rc = mpl.RcParams({'font.cursive': ['Apple Chancery',
                                        'Textile',
                                        'Zapf Chancery',
                                        'cursive'],
                       'font.family': 'sans-serif',
                       'font.weight': 'normal',
                       'font.size': 12})


    if six.PY3:
        expected_repr = """
RcParams({'font.cursive': ['Apple Chancery',
                           'Textile',
                           'Zapf Chancery',
                           'cursive'],
          'font.family': 'sans-serif',
          'font.size': 12,
          'font.weight': 'normal'})""".lstrip()
    else:
        expected_repr = """
RcParams({u'font.cursive': [u'Apple Chancery',
                            u'Textile',
                            u'Zapf Chancery',
                            u'cursive'],
          u'font.family': u'sans-serif',
          u'font.size': 12,
          u'font.weight': u'normal'})""".lstrip()

    assert_str_equal(expected_repr, repr(rc))

    if six.PY3:
        expected_str = """
font.cursive: ['Apple Chancery', 'Textile', 'Zapf Chancery', 'cursive']
font.family: sans-serif
font.size: 12
font.weight: normal""".lstrip()
    else:
        expected_str = """
font.cursive: [u'Apple Chancery', u'Textile', u'Zapf Chancery', u'cursive']
font.family: sans-serif
font.size: 12
font.weight: normal""".lstrip()

    assert_str_equal(expected_str, str(rc))

    # test the find_all functionality
    assert ['font.cursive', 'font.size'] == sorted(rc.find_all('i[vz]').keys())
    assert ['font.family'] == list(six.iterkeys(rc.find_all('family')))

if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)
