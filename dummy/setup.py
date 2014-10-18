﻿from setuptools import setup

import dummy as validator


package = 'sloth_ci.validators'

setup(
    name=validator.__title__,
    version=validator.__version__,
    author=validator.__author__,
    description=validator.__description__,
    long_description=validator.__doc__,
    author_email=validator.__author_email__,
    url='https://bitbucket.org/moigagoo/sloth-ci-validators',
    py_modules=['%s.%s' % (package, validator.__name__)],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.3'
    ],
    license=validator.__license__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
