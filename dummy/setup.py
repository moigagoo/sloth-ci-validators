from setuptools import setup

import dummy as validator


package = 'sloth_ci.validators'

setup(
    name=validator.__title__,
    version=validator.__version__,
    author=validator.__author__,
    description='Dummy validator for Sloth CI',
    long_description='Dummy Sloth CI validator that checks if the ``message`` param in a ``GET`` request is the same the ``message`` value in the ``provider_data`` config section.',
    author_email='moigagoo@live.com',
    url='https://bitbucket.org/moigagoo/sloth-ci-validators',
    py_modules=['%s.dummy' % package],
    package_dir={package: '.'},
    install_requires = [
        'sloth_ci>=0.6.3'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
    )
