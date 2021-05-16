from SettingsWorker import SettingsWorker

class LatexInputWorker:
    
    def __init__(self, settingsWorker: SettingsWorker):
        self.content_path = settingsWorker.get_content_path()
        print(self.content_path)

    def process_files(self, files_string: str):
        return None

    def all_file_list(self):
        return None