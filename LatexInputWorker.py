from SettingsWorker import SettingsWorker

import os

class LatexInputWorker:
    
    def __init__(self, settingsWorker: SettingsWorker):
        self.content_path = settingsWorker.get_content_path()
        self.files = os.listdir(self.content_path)
        self.files.sort()

    def process_files(self, files_string: str):
        return None

    def all_file_list(self):
        print(self.files)
        return self.files