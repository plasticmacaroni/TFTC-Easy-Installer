# MVP of TFTC Easy Installer

To use:

1. Download the script into your game folder
2. Run it and it will download each required mod (XWAU, TFTC 1.3, TFTC 1.3.2, as well as all patches on the [Quick Fixes official page](https://sites.google.com/view/tie-fighter-total-conversion/installation/quick-fixes)
3. It will automatically open and start the required installers for you to complete, recommending settings as you go
4. Checks if you have run the game at least once

**It will also check that you have enough space to download and that you're running from the right place.**

## Updated as of patch 1.3.2

This installer performs several other steps:

1. Check if the game executable is in the current folder
2. Check if there's more than 50 GB on the main drive
3. Confirm each downloaded zip file matches the filesize listed on the servers

## Running the script as an exe

If you'd like to run it as an executable file, you can install pysimplegui with "pip3 install pysimplegui" and then run:
`python -m pysimplegui-exemaker.pysimplegui-exemaker`

Running the python script from within the game installation folder does work fine. 
