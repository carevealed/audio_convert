# audio_convert
CAVPP Audio Conversion script

Description
===========
Converts wav audio files to mp3 CAVPP standards.

To Install
==========

You have two options:


Option 1: Standard
------------------

1. Open a terminal window and type:

        cd Downloads
        git clone https://github.com/cavpp/audio_convert.git
        cd audio_convert
        sudo python setup.py install 
        
2. Enter your computer password and the script will install along with all the dependencies.


Option 2: pip
-------------

1. Download the latest version in the dist folder to your Download folder
2. In a terminal window, type:

        cd Downloads
        sudo pip install CAVPP_Audio_Convert-0.1.1.tar.gz

3. Enter your computer password and the script will install along with all the dependencies. 

**Note:** If you have a problem that pip isn't installed, you can install it with 
 the following command.
 
        sudo easy_install pip


To Use
======

To use with the command line:
-----------------------------
In a terminal, simply type "makemp3" followed by a single file or directory.

**Note:** This will save the mp3 files to the same folder location as the wav 
files they are converting from.
    
### Example 1: Single wav file.

    
        makemp3 /Users/lpsdesk/PycharmProjects/audioConvert/OtherFolder/ALLEY_B.wav
            
### Example 2: Entire folder of wav files.


        makemp3 /Users/lpsdesk/PycharmProjects/audioConvert/testFolder
  
  
To use the graphical user interface:
------------------------------------
In a terminal windows, simple type the following command::
  
      makemp3 -g

Credits
=======
Author: Henry Borchers 