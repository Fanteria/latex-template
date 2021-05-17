from SettingsWorker import SettingsWorker

import os
import re

class LatexInputWorker:
    
    def __init__(self, settingsWorker: SettingsWorker):
        self.content_path = settingsWorker.get_content_path()
        self.files = os.listdir(self.content_path)
        self.files.sort()

    # Create from input string list of file names, if input is invalid, return None.
    def proccess_files(self, files_string: str):
        files = files_string
        # Substitute filenames with their numbers, formate and split them.
        for i in range(len(self.files)):
            files = re.sub(self.files[i][:-4], str(i+1), files)
        files = re.sub("\s", "", files)
        file_numbers = files.split(",")

        files_list: str = []
        new_pages_list: bool = []
        for i in file_numbers:
            # Set new page, if starts on "n" or "N"
            if i[0] == "n" or i[0] == "N":
                newpage = True
                i = i[1:len(i)]
            else:
                newpage = False

            # Convert number to file name.
            try:
                files_list.append(self.files[int(i)-1])
                new_pages_list.append(newpage)
            except ValueError:
                # If it is not number find "-" for range.
                pos = i.find("-")
                if pos == -1:
                    return None
                else:
                    try:
                        for j in range(int(i[0:pos]), int(i[pos+1:len(i)])+1):
                            files_list.append(self.files[j-1])
                            new_pages_list.append(newpage)
                    except ValueError:
                        return None

        return [files_list, new_pages_list]

    # Return list of all files.
    def all_file_list(self):
        print(self.files)
        return self.files