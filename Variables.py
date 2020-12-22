import unicodedata

class Variables:

    def __init__(self, doctitle="", docauthor="", supervisor="",
                    institution="", faculty="", department="",
                    location="", papertype="", subject="", keywords=""):

        self.vars = {
            "title": ("pdftitle", doctitle),
            "author": ("pdfauthor", docauthor),
            "supervisor": ("", supervisor),
            "institution": ("pdfproducer", institution),
            "faculty": ("", faculty),
            "department": ("", department),
            "location": ("", location),
            "papertype": ("", papertype),
            "subject": ("pdfsubject", subject),
            "keywords": ("pdfkeywords", keywords)
        }

        self.get_metadata_list()

    def __convert(self, data):
        data = unicodedata.normalize('NFKD', data)
        output = ''
        for c in data:
            if not unicodedata.combining(c):
                output += c
        return output

    def get_metadata_list(self):
        list = []
        for i in self.vars:
            if self.vars[i][0] != "":
                list.append((self.vars[i][0], self.__convert(self.vars[i][1])))
        return list

    def get_metadata_string(self):
        ret = ""
        list=self.get_metadata_list()
        ret += "\hypersetup{\n"
        for i in list:
            ret += "\t" + i[0] + "={" + i[1] + "},\n"

        ret += "\tpdfcreator = {\LaTeX\ with\ Bib\LaTeX},\n"
        ret += "\tcolorlinks = false,\n"
        ret += "\thidelinks\n}\n"
        return ret

    def get_commands_list(self):
        list = []
        for i in self.vars:
            list.append((i, self.vars[i][1]))
        return list

    def get_commands_string(self):
        ret = ""
        for i in self.get_commands_list():
            ret+= "\\set" + i[0] + "{" + i[1] + "}\n"
        return ret

    def process_line(self, line):
        command = "\set"
        auxfrs = line.find(command)
        if auxfrs == -1:
            return
        auxsec = line[auxfrs:].find("{")
        commandname = line[auxfrs+len(command):auxsec]
        if commandname not in self.vars:
            return
        auxfrs = auxsec
        auxsec = line[auxfrs:].find("}")
        auxsec += auxfrs
        commandvalue = line[auxfrs+1:auxsec]
        self.vars[commandname] = (self.vars[commandname][0], commandvalue)
