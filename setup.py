from distutils.core import setup

setup(
    name='barpy',
    version='1.0',
    description='barpy - a flask web server that interfaces with a drink robot',
    author='Brian Hendriks',
    url='https://github.com/bheni/barpy',
    packages=['barpy'],
    install_requires=['flask', 'gpiozero'],
)
