import json

class SettingsWorker:
    __file_name="settings.json"


    def __init__(self, base_path: str, working_path: str):
        self.base_path = base_path
        self.working_path = working_path
        with open(base_path + "/" + SettingsWorker.__file_name) as json_base:
            self.data = json.load(json_base)

    #def get_list_of_commands(self):
        
