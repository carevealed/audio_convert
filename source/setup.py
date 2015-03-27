from setuptools import setup, find_packages

setup(
    name='Audio Convert',
    version='0.1',
    packages=find_packages(),
    # packages=['audio_convert', 'audio_convert.scripts', 'audio_convert.scripts.gui',
    #           'audio_convert.scripts.modules'],
    url='https://github.com/cavpp/audio_convert',
    install_requires=['OneSheet == 0.1.3.26'],
    license='TBD',
    author='Henry Borchers',
    author_email='hborcher@berkeley.edu',
    entry_points={'console_scripts' : ['audioconvert = audio_convert.scripts.audioConvert:installed_start']},
    description='Converts wav files into MP3 files according to CAVPP standards.'
)
