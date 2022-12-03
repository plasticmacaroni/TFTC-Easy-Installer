# TFTC Easy Installer

## What does this do?!
This tool makes installing TFTC easy! While we still recommend the most recent [Youtube Video](https://www.youtube.com/watch?v=qui9X4gjVtc) outlining installation steps for TFTC, **bottom line: if you want to get right to the action, this tool can be used to download everything you need!**

## But what does it *do*?!
1. Checks that your install location, space available, and environment are correct
2. Automagically download every installer you'll need to get into the cockpit ASAP
3. Run each upgrade and installer (there are several!) in the correct order, suggesting recommended settings for each
4. Verify downloaded files, and that installations are successful
5. Let you know you're ready to fly!

## How to run the tool!
### The easy way:
1. Download `TFTC-Easy-Installer-Executable-v1.0.zip` from the Releases page
2. Unzip it into your game folder (wherever alliance.exe is)
3. Run the `easy-installer.exe` file and press next to go step by step through everything you need

### The Python way:
1. Have Python installed
2. Run the tool by following the steps below:
3. ```git clone https://github.com/plasticmacaroni/TFTC-Easy-Installer.git```
4. ```pip install -r requirements.txt```
5. ```python easy-installer.py```
6. Follow the on-screen prompts to install step by step

## Executable information
The executable has been created (and can be recreated) by running `pip install pysimplegui` and then running
`python -m pysimplegui-exemaker.pysimplegui-exemaker`.
