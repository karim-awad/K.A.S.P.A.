from setuptools import setup, find_packages

setup(
    name='K.A.S.P.A',
    version='0.5',
    packages=find_packages(),
    url='https://github.com/karim-awad/K.A.S.P.A.',
    license='MIT',
    author='Karim Awad',
    author_email='dev@awad.cloud',
    description='K.A.S.P.A, a simple python assistant',
    install_requires=['beautifulsoup4', 'praw', 'python-forecastio', 'googlemaps', 'phue', 'textblob', 'wikipedia',
                      'requests', 'python-mpd', 'spotipy']
)
