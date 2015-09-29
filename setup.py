#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010 Logica


from setuptools import setup

PACKAGE = 'UserQueriesPlugin'
VERSION = '0.0.0'

setup(
    name=PACKAGE, version=VERSION,
    description='Allows users to save their own queries privately',
    author="Nick Piper", author_email="nick.piper@logica.com",
    url='http://trac.uk.logica.com/',
    packages = ['userqueries'],
    package_data={
        'userqueries': [
            'templates/*.html',
            'htdocs/*.css'
        ]
    },
    entry_points = {
        'trac.plugins': [
            'userqueries.web_ui = userqueries.web_ui',
            'userqueries.report = userqueries.report',
        ]
    }
)
