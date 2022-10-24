from unicodedata import ucd_3_2_0
import PySimpleGUI as sg
import os
import urllib
from urllib.request import urlopen
import shutil
import pathlib
import requests
import zipfile_deflate64 as zipfile
from bs4 import BeautifulSoup

class Website:
    def __init__(self, url, file_name, description):
        self.url = url
        self.file_name = file_name
        self.size_checked = False
        self.description = description

class Downloader:
    def __init__(self):
        # Context flags
        self.folder_checked_flag = False
        self.needs_OK_to_continue = False
        self.exit_now = False
        self.disk_check_completed = False
        # File index counter
        self.current_file_index = 0
        # Build window
        self.main_message = "Press OK to get started"
        self.step = "Step 1 of 6"
        layout = [
            [sg.Text(self.step, size=(120, None), key="STEP")], 
            [sg.Text(self.main_message, size=(60, None), key="MAIN_MESSAGE")], 
            [
                sg.Button("OK", key="OK"), 
                sg.Button("CANCEL", key="CANCEL")
            ]
        ]
        # Create the window
        self.window = sg.Window("Installer", icon='TFTC.ico', default_element_size=(20, 1), layout=layout, margins=[60, 100])

    def set_message(self, message):
        self.window.Element("MAIN_MESSAGE").update(message)
        self.window.read()

    def set_step(self, step):
        self.window.Element("STEP").update("Step " + str(step) + " of 6")
        self.window.read()

    def check_size(self, url, local_file):
        url = self.convert_for_moddb(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        }
        content_length = requests.get(url, headers=headers, stream=True).headers['Content-length']
        if int(content_length) != os.stat(local_file).st_size:
            self.set_message("File size unmatch for " + local_file + " from " + url + "\n" + str(f.info()['Content-Length']) + " online vs. " + str(os.stat(local_file).st_size) + " locally.")

    def download_file(self, url, local_filename):
        url = self.convert_for_moddb(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        }
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return local_filename

    def convert_for_moddb(self, url):
        if "moddb" in websites[self.current_file_index].url:
            page = requests.get(websites[self.current_file_index].url)
            soup = BeautifulSoup(page.content, "html.parser")
            results = urllib.parse.urljoin("https://moddb.com", soup.find(id="downloadmirrorstoggle").attrs["href"])
            page = requests.get(results)
            soup = BeautifulSoup(page.content, "html.parser")
            results = urllib.parse.urljoin("https://moddb.com", soup.find("a").attrs["href"])
            url = results
            return url
        return url

    def run(self):
        # Create an event loop
        while True:
            # Get window context, this must always come before all other logic
            event, values = self.window.read(timeout = 100)
            # First thing, end program if user closes window or presses the OK button
            if event == sg.WIN_CLOSED or event == "CANCEL":
                break
            if self.exit_now:
                self.window.close()

            # Check if running from game folder and set flag
            if self.folder_checked_flag == False:
                if not os.path.exists("XwingAlliance.exe"):
                    self.set_message("It's not recommended to run outside of the game folder, are you sure?\nIf you haven't downloaded X-Wing Alliance from GOG, Steam, or Origin, please do so and run this program from within the game folder.")
                    self.needs_OK_to_continue = True
                self.folder_checked_flag = True

            # Check if enough disk space and set flag
            if not self.disk_check_completed:
                self.set_message("Checking available space...")
                available_disk = shutil.disk_usage(pathlib.Path.home().drive).free
                available_disk_in_gb = available_disk / 1073741824
                if available_disk_in_gb < 50:
                    self.set_message("Recommended 50 GB minimum space to install, are you sure you want to continue?")
                    self.needs_OK_to_continue = False
                self.disk_check_completed = True

            # Make sure it's been run once
            # TODO

            # Don't act unless user says yes
            if self.needs_OK_to_continue:
                if event == "OK":
                    self.set_message("Continuing...")
                    self.needs_OK_to_continue = False

            # Download current file (current_file_index variable)
            # If we're requesting an index out of range, great, we've already requested it all
            if not self.current_file_index >= len(websites):
                if not os.path.isfile(websites[self.current_file_index].file_name):
                    self.set_message("Downloading " + websites[self.current_file_index].description + ": " + websites[self.current_file_index].file_name + "\nDownloading thousands of new models, scripts, and events.\n" + "This may take quite a bit, so leave this window open and grab a cup of tea...")
                    try:
                        self.download_file(websites[self.current_file_index].url, websites[self.current_file_index].file_name)
                    except Exception as exc:
                        print(exc)
                        self.set_message('Encountered unknown error: '+ str(exc) + '. Press anything to exit.')
                        self.exit_now = True
                        continue
                # Check the filesize to make sure the files are fully downloaded (large files, so partial downloads are a pain to troubleshoot)
                if websites[self.current_file_index].size_checked == False:
                    self.set_message("Checking file size for downloaded "+ websites[self.current_file_index].file_name +", press NEXT to continue...")
                    self.check_size(websites[self.current_file_index].url, websites[self.current_file_index].file_name)
                    websites[self.current_file_index].size_checked = True
                    self.set_message("Filesize match. Press NEXT to continue...")
                # Attempt unzip if the file exists
                if ".zip" in websites[self.current_file_index].file_name:
                    try:
                        print("Unzipping" + " " + websites[self.current_file_index].file_name)
                        self.set_message("Unzipping" + " " + websites[self.current_file_index].file_name + "...")
                        zipfile.ZipFile(websites[self.current_file_index].file_name).extractall()
                    except RuntimeError:
                        continue
                self.current_file_index += 1
                self.set_step(self.current_file_index+1)
                continue
            
            #The continue above means the following code is unreachable before the websites[] are fully visited/downloaded

            # Install XWAU2020 (checks for install through folder "/TotalConverter"):
            if not os.path.exists("TotalConverter"):
                self.set_message("Please complete the XWAU2020 executable and press NEXT when installation is complete.")
                os.startfile("XWAU2020.exe")
                self.current_file_index += 1
                self.set_step(self.current_file_index+1)
                self.needs_OK_to_continue = True
                continue

            # Install TFTC 1.3:
            if not os.path.exists("TFTCversion.txt"):
                self.set_message("Please complete the TFTC 1.3 executable and press NEXT when installation is complete.")
                os.startfile("TFTC_1.3.exe")
                self.current_file_index += 1
                self.set_step(self.current_file_index+1)
                self.needs_OK_to_continue = True
                continue

            # Install TFTC 1.3.2 Patch:
            if not os.path.exists("TFTC_1.3.2.exe"):
                self.set_message("Please complete the TFTC 1.3.2 Patch executable and press OK when installation is complete.")
                os.startfile("TFTC_1.3.2.exe")
                self.current_file_index += 1
                self.set_step(self.current_file_index+1)
                self.needs_OK_to_continue = True
                continue

            self.set_message("Choose Palpatine Total Converter from the Game Launcher window to start.\nChoose Load a Total Conversion, and then:\n1. TFTC Classic for the original story, remastered\n2. TFTC Reimagined for 8+ new campaigns.\nEnjoy!")
            os.startfile("TFTC_1.3.2.exe")
            self.set_step(6)
            self.exit_now

        self.window.close()


if "__main__":
    websites = [Website("https://www.xwaupgrade.com/download/installers/XWAU2020.exe", "XWAU2020.exe", "X-Wing Alliance Upgrade main patch"), Website("https://www.moddb.com/mods/tie-fighter-total-conversion-tftc/downloads/tie-fighter-total-conversion-tftc-v13-full-patch", "TFTC_1.3.zip", "TIE Fighter Total Conversion (TFTC) v1.3 Full Version"), Website("https://www.moddb.com/mods/tie-fighter-total-conversion-tftc/downloads/tftc-1-3-2", "TFTC_1.3.2.zip", "TIE Fighter Total Conversion (TFTC) 1.3.2 Patch")]
    downloader = Downloader()
    downloader.run()