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
    def __init__(self, url, file_name, description, download_message):
        self.url = url
        self.file_name = file_name
        self.size_checked = False
        self.description = description
        self.download_message = download_message

class Downloader:
    def __init__(self):
        # Context flags
        self.folder_checked_flag = False
        self.needs_OK_to_continue = False
        self.exit_now = False
        self.disk_check_completed = False
        # File index counter
        self.current_file_index = 0
        # Install step counter
        self.set_step = 1
        # Build window
        self.main_message = "Press NEXT to get started"
        self.step = "Step 1 of 6"
        layout = [
            [sg.Text(self.step, size=(None, None), font='ANY 42', key="STEP")], 
            [sg.Text(self.main_message, size=(60, None), font = "ANY 20",key="MAIN_MESSAGE")], 
            [
                sg.Button("NEXT", key="OK", font='ANY 42', size=(20, None))
            ]
        ]
        # Create the window
        self.window = sg.Window("Installer", icon='TFTC.ico', default_element_size=(20, 1), layout=layout, margins=[60, 100], element_justification='c')

    def set_message(self, message):
        self.window.Element("MAIN_MESSAGE").update(message)
        self.window.read()

    def check_size(self, url, local_file):
        url = self.convert_for_moddb(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        }
        content_length = requests.get(url, headers=headers, stream=True).headers['Content-length']
        if int(content_length) != os.stat(local_file).st_size:
            self.set_message("File size unmatch for " + local_file + " from " + url + "\n" + content_length + " online vs. " + str(os.stat(local_file).st_size) + " locally.")
            return False
        return True

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
            # Get window context
            event, values = self.window.read(timeout = 100)
            # First thing, end program if user closes window or presses the NEXT button
            if event == sg.WIN_CLOSED:
                break
            if self.exit_now:
                self.window.close()
                exit()

            # Set step, which is arbitrary
            self.step = "Step " + str(self.set_step) + " of 7"
            self.window.Element("STEP").update(self.step)
            self.window.read()

            # Don't act unless user says yes
            if self.needs_OK_to_continue:
                if event == "OK":
                    self.set_message("Continuing...")
                    self.needs_OK_to_continue = False

            # Step 1: Check if running from game folder and set flag
            if self.set_step == 1:
                if self.folder_checked_flag == False:
                    if not os.path.exists("XwingAlliance.exe"):
                        self.set_message("It's not recommended to run outside of the game folder, are you sure?\nIf you haven't downloaded X-Wing Alliance from GOG, Steam, or Origin, please do so and run this program from within the game folder.")
                        self.needs_OK_to_continue = True
                    self.folder_checked_flag = True
                self.set_step += 1
                continue

            # Step 2: Check if enough disk space and set flag
            if self.set_step == 2:
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
                self.set_step += 1
                continue

            # Step 3: Download necessary files (current_file_index variable)
            if self.set_step == 3:
                # If we're requesting an index out of range, great, we've already requested it all
                if not self.current_file_index >= len(websites):
                    if not os.path.isfile(websites[self.current_file_index].file_name):
                        self.set_message("Downloading " + websites[self.current_file_index].description + ": " + websites[self.current_file_index].file_name + "\n"+ websites[self.current_file_index].download_message +"\n" + "This may take quite a bit, so leave this window open and grab a cup of tea...")
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
                        result_bool = self.check_size(websites[self.current_file_index].url, websites[self.current_file_index].file_name)
                        if result_bool == False:
                            os.remove( websites[self.current_file_index].file_name) 
                            continue
                        else: 
                            websites[self.current_file_index].size_checked = True
                            self.set_message("Filesize match. Press NEXT to continue...")
                    # Attempt unzip if the file exists
                    if ".zip" in websites[self.current_file_index].file_name:
                        try:
                            self.set_message("Press NEXT to unzip" + " " + websites[self.current_file_index].file_name + "...")
                            zipfile.ZipFile(websites[self.current_file_index].file_name).extractall()
                        except RuntimeError:
                            continue
                    self.current_file_index += 1
                    continue
            self.set_step += 1
            #The continue above means the following code is unreachable before the websites[] are fully visited/downloaded
            
            # Step 3: Install XWAU2020 (checks for install through folder "/TotalConverter"):
            if self.set_step == 4:
                if not os.path.exists("TotalConverter"):
                    self.set_message("Please complete the XWAU2020 executable install process and press NEXT when installation is complete.\n\nDefault settings are recommended.")
                    os.startfile("XWAU2020.exe")
                    self.current_file_index += 1
                    self.needs_OK_to_continue = True
                    continue
                self.set_step += 1
                continue

            # Install TFTC 1.3:
            if self.set_step == 5:            
                if not os.path.exists("TFTCversion.txt"):
                    self.set_message("Please complete the TFTC 1.3 executable install process and press NEXT when installation is complete.\n\nIf using this tool to download for the first time, use \"Clean Install\" as the installation type. Under Tutorial Missions, \"Updated Tutorial Missions\" is recommended.")
                    os.startfile("TFTC_1.3.exe")
                    self.current_file_index += 1
                    self.needs_OK_to_continue = True
                    continue
                self.set_step += 1
                continue

            # Install TFTC 1.3.2 Patch:
            if self.set_step == 6:    
                if os.path.exists("TFTCversion.txt"):
                    with open(r'TFTCversion.txt', 'r') as file:
                        content = file.read()
                        if not '1.3.2' in content:
                            print('string exist')
                            self.set_message("Please complete the TFTC 1.3.2 Patch executable install process and press NEXT when installation is complete.")
                            os.startfile("TFTC_1.3.2.exe")
                            self.current_file_index += 1
                            self.needs_OK_to_continue = True
                            continue
                self.set_step += 1
                continue

            # Step 6: Launch
            if self.set_step == 7:   
                self.set_message("Choose Palpatine Total Converter from the Game Launcher window to start.\nChoose Load a Total Conversion, and then:\n1. TFTC Classic for the original story, remastered\n2. TFTC Reimagined for 8+ new campaigns.\nEnjoy!")
                os.startfile("XwingAlliance.exe")
                self.exit_now

        self.window.close()

if "__main__":
    websites = [Website("https://www.xwaupgrade.com/download/installers/XWAU2020.exe", "XWAU2020.exe", "X-Wing Alliance Upgrade main patch", "This update will provide thousands of surfaces, textures, and ship models to achieve higher detail."), Website("https://www.moddb.com/mods/tie-fighter-total-conversion-tftc/downloads/tie-fighter-total-conversion-tftc-v13-full-patch", "TFTC_1.3.zip", "TIE Fighter Total Conversion (TFTC) v1.3 Full Version", "Press NEXT to download the core update with thousands of new models, scripts, and events."), Website("https://www.moddb.com/mods/tie-fighter-total-conversion-tftc/downloads/tftc-1-3-2", "TFTC_1.3.2.zip", "TIE Fighter Total Conversion (TFTC) 1.3.2 Patch", "Press NEXT to download the patch up to the newest possible version.")]
    downloader = Downloader()
    downloader.run()
