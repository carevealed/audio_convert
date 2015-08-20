# audio_convert
CAVPP Audio Conversion script

Description
===========
Converts wav audio files to mp3 CAVPP standards.

Documentation
=============

* [User Documenation](http://cavpp.github.io/audio_convert/)

To Install
==========

You have two options:



## Option 1: Install using Conda (recommended)


If you are setting up Conda/Anaconda for the first time, please look at the readme document 
[here](https://github.com/cavpp/conda_recipes/tree/master#setting-up-conda) first 

1. In the launcher program, open a Python 3.4 environment or higher.
2. Click on the install button for this script

## Option 2: Install binary (Wheel)


1. Download the latest version from the releases section of the project's Github page https://github.com/cavpp/PBCore/releases and copy the URL of the most current version.
2. Open a terminal and type:
        
        sudo pip3 install #paste the URL here
        
            

## Option 3: pip


1. Download the latest version in the dist folder to your Download folder
2. In a terminal window, type:

        cd Downloads
        sudo pip install CAVPP_Audio_Convert-0.1.1.tar.gz

3. Enter your computer password and the script will install along with all the dependencies. 

**Note:** If you have a problem that pip isn't installed, you can install it with 
 the following command.
 
        sudo easy_install pip

## Option 4: source

1. Open a terminal window and type:

        cd Downloads
        git clone https://github.com/cavpp/audio_convert.git
        cd audio_convert
        sudo python setup.py install 
        
2. Enter your computer password and the script will install along with all the dependencies.

To Use
======

## Anaconda Launcher:

Note: Only works with the Conda installation method. 

1. In a terminal window type:

   ```
   launcher
   ```
  
2. Click Environment and select the correct evironment. 
3. Click on the launch button next to the script name


## To use with the command line:

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
