from setuptools import setup, find_packages

setup(
    name='CAVPP_Audio_Convert',
    version='0.1.11b4',
    packages=find_packages(),
    url='https://github.com/cavpp/audio_convert',
    install_requires=['OneSheet >= 0.1.5'],
    license='GPL',
    author='Henry Borchers',
    author_email='hborcher@berkeley.edu',
    description='Converts wav files into MP3 files according to CAVPP standards.',
    entry_points={'console_scripts' : ['makemp3 = audio_convert.scripts.audioConvert:installed_start']},
    include_package_data=True,
    package_data={"": ['audio_convert/scripts/gui/images/CAVPPcolor.gif']}
)
