from setuptools import setup

setup(
    name='Kaspa',
    version='0.6',
    packages=['Kaspa', 'Kaspa.modules', 'Kaspa.modules.core_modules', 'Kaspa.modules.abstract_modules',
              'Kaspa.modules.extension_modules', 'Kaspa.modules.extension_modules.helper', 'Kaspa.communicators',
              'Kaspa.communicators.abstract_communicators'],
    url='https://github.com/karim-awad/Kaspa',
    license='MIT',
    author='Karim Awad',
    author_email='dev@awad.cloud',
    description='Kaspa, a simple python assistant',
    install_requires=['beautifulsoup4', 'praw', 'python-forecastio', 'googlemaps', 'phue', 'textblob', 'wikipedia',
                      'requests', 'python-mpd2', 'spotipy', 'configparser', 'lxml', 'telepot', 'telegram', 'wakeonlan']
)
