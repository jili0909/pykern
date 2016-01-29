# -*- coding: utf-8 -*-
u"""pytest for `pykern.pkconfig`

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

import dateutil.parser
import pytest
import sys

import py.path

def test_init(monkeypatch):
    """Validate initializing a module"""
    # Can't import anything yet
    data_dir = py.path.local(__file__).dirpath('pkconfig_data')
    home = str(data_dir)
    monkeypatch.setenv('HOME', home)
    #TODO(robnagler) test for this
    monkeypatch.setenv('p1_m1_dict1_d4', 'env4')
    sys.path.insert(0, str(data_dir))
    from pykern import pkconfig
    pkconfig._root_pkg = None
    pkconfig.append_load_path('p1')
    from p1.m1 import cfg
    assert 'replace1' == cfg['dict1']['d1'], \
        '~/.p1_pkconfig.py should replace dict1[d1]'
    assert 'default2' == cfg['dict1']['d2'], \
        'Nothing should change dict1[d2]'
    assert 'd3' in cfg['dict1'], \
        'd3 should appear in dict1 from the merge in ~/.p1_pkconfig.py'
    assert 'new3' == cfg.dict1.d3, \
        'dict1[d3] should be set to the value in new3'
    assert 'env4' == cfg.dict1.d4, \
        'dict1[d4] should be set by env'
    assert ['first1', 'second1'] == cfg['list2'], \
        '~/.p1_pkconfig.py should prepend list2'
    assert 55 == cfg['p3'], \
        '~/.p1_pkconfig.py should set p3'
    assert 550 == cfg['p4'], \
        '~/.p1_pkconfig.py should set p4 to 10*p3'
    assert home == cfg['p5'], \
        'environment variables should be visible in formatted params'
    assert dateutil.parser.parse('2012-12-12T12:12:12Z') == cfg['p6'], \
        'pkconfig_base.py sets time value and m1._custom_p6'
    assert 999 == cfg.dynamic_default10, \
        'When value is None, calls parser'


def xtest_init_deviance(monkeypatch):
    # TODO(robnagler) test Verbatim: fails if inserted in a formatted string
    #    * bad format string
    #    * non-existent format string
    #    * incorrect type values for dict/list/value
    pass
