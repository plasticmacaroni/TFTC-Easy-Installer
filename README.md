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
Steps to type in if you're unfamiliar with Python:

Have X-Wing Alliance installed from Steam, GOG, or Origin. Have Python installed.

Run the tool by following the steps below:
1. ```git clone https://github.com/plasticmacaroni/TFTC-Easy-Installer.git```
2. ```pip install -r requirements.txt```
3. ```python easy-installer.py```

## Running the script as an exe
If you'd like to run it as an executable file, you can install pysimplegui with `pip3 install pysimplegui` and then run:
`python -m pysimplegui-exemaker.pysimplegui-exemaker`
