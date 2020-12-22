
class FileSettings:

    def __init__(self, titlepage="titlepage", abstract="abstract",
                assignment="assignment.pdf", affidavit="affidavit",
                acknowledgments="acknowledgments",
                listofabbreviations="listofabbreviations",
                appendiceslist="appendices"):

        self.fset = {
            "titlepage" : ("false", titlepage),
            "abstract" : ("false", abstract),
            "assignment" : ("false", assignment),
            "affidavit" : ("false", affidavit),
            "acknowledgments" : ("false", acknowledgments),
            "tableofcontents" : ("true", ""),
            "listofabbreviations" : ("false", listofabbreviations),
            "listoffigures" : ("false", ""),
            "listofgraphs" : ("false", ""),
            "listoftables" : ("false", ""),
            "appendiceslist" : ("false", appendiceslist)
        }

    def get_files_list(self):
        return { "titlepage" : self.fset["titlepage"][1],
                 "abstract" : self.fset["abstract"][1],
                 "assignment" : self.fset["assignment"][1],
                 "affidavit" : self.fset["affidavit"][1],
                 "acknowledgments" : self.fset["acknowledgments"][1],
                 "listofabbreviations" : self.fset["listofabbreviations"][1],
                 "appendiceslist" : self.fset["appendiceslist"][1]}

    def file_list_tostring(self):
        list = self.get_files_list()
        ret = ""
        for i in list:
            ret += "\set" + i + "file{"
            ret += self.fset[i][1]
            ret += "}\n"
        return ret

    def print_list_tostring(self):
        ret = ""
        for i in self.fset:
            ret += "\setboolean{"
            ret += i
            ret += "}{"
            ret += self.fset[i][0]
            ret += "}\n"
        return ret

    def __process_boolean(self, line):
        command = "\setboolean{"
        auxfrs = line.find(command)
        if auxfrs == -1:
            return
        auxsec = line[auxfrs:].find("}")
        commandname = line[auxfrs+len(command):auxsec]
        auxfrs = line[auxsec:].find("{")
        auxfrs += auxsec
        auxsec = line[auxfrs:].find("}")
        auxsec += auxfrs
        commandval = line[auxfrs+1:auxsec]
        self.fset[commandname] = (commandval, self.fset[commandname][1])

    def __process_file(self, line):
        commandstart = "\set"
        auxfrs = line.find(commandstart)
        if auxfrs == -1:
            return
        commandend = "file{"
        auxsec = line[auxfrs+len(commandstart):].find(commandend)
        if auxsec == -1:
            return
        commandname = line[auxfrs+len(commandstart):auxsec+auxfrs+len(commandstart)]
        auxfrs = auxsec+auxfrs+len(commandstart)+len(commandend)
        auxsec = line[auxfrs:].find("}")
        commandval = line[auxfrs:auxsec+auxfrs]
        self.fset[commandname] = (self.fset[commandname][0], commandval)

    def process_line(self, line):
        self.__process_boolean(line)
        self.__process_file(line)
