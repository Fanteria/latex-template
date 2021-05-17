import os
import json

class SettingsWorker:
    __file_name="settings.json"


    def __init__(self, base_path: str, working_path: str):
        self.base_path = base_path
        self.working_path = working_path
        base_file = os.path.join(base_path, SettingsWorker.__file_name)
        working_file = os.path.join(working_path, SettingsWorker.__file_name)

        with open(base_file) as json_base:
            self.data = json.load(json_base)

        if os.path.isfile(working_file):
            with open(working_file) as json_working:
                aux = json.load(json_working)
            for i in aux:
                if i == "commands":
                    for j in aux[i]:
                        self.data[i].append(j)
                else:
                    self.data[i] = aux[i]

    def get_list_of_commands(self):
        ret = {}
        for i in self.data["commands"]:
            ret[i["name"]] = i["command"]

        return ret

    def get_content_path(self, relative=True):
        if relative:
            return os.path.join(".", self.data["content-folder"])
        else:
            return os.path.join(self.working_path, self.data["content-folder"])

    def get_gen_path(self, relative=True):
        if relative:
            return os.path.join(".", self.data["generated-folder"])
        else:
            return os.path.join(self.working_path, self.data["generated-folder"])
        
