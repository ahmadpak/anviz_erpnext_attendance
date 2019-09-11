# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in anviz_erpnext_attendance/__init__.py
from anviz_erpnext_attendance import __version__ as version

setup(
	name='anviz_erpnext_attendance',
	version=version,
	description='Connects with anviz sql database and pulls attendance according to the status 0 for IN 1 for Out 2 for Break',
	author='Havenir',
	author_email='info@havenir.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
