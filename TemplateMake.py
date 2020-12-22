import os
import re
import shutil
import zipfile
import subprocess
import xml.etree.ElementTree as ET
import xml.dom.minidom as Dom

from FileSettings import FileSettings
from Variables import Variables

class TemplateMake:

    def __init__(self, pic_folder="pics/",
            content_folder="content/", project_name="projekt",
            pdf_name="", ask_pwd=False, usr_pwd="", own_pwd="own", vars=Variables(),
            filesettings=None):

        self.project_path=os.getcwd()

        self.bin_folder="bin/"

        self.settings="settings.tex"

        self.references="references.bib"

        self.main=project_name + ".tex"

        self.pic_folder=pic_folder
        self.pic_folder_abs=os.path.abspath(pic_folder)

        self.content_folder=content_folder

        self.project_name=project_name
        if pdf_name == "":
            self.pdf_name=self.project_name+".pdf"

        self.ask_pwd=ask_pwd
        self.usr_pwd=usr_pwd
        self.own_pwd=own_pwd

        self.vars = vars

        if FileSettings is not None:
            self.filesetting = FileSettings()
            if os.path.exists("settings.tex"):
                self.load("settings.tex")
        else:
            self.filesetting=filesettings


    ###### PRIVATE FUNCTIONS ######
    def __nonbreaking_space(self, text):
        text = re.sub(r' ([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r' \1~', text)
        text = re.sub(r' ([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r' \1~', text)
        text = re.sub(r'~([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r'~\1~', text)
        text = re.sub(r'~([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r'~\1~', text)
        text = re.sub(r'\n([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r'\n\1~', text)
        text = re.sub(r'\n([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r'\n\1~', text)

        return text

    def __printLog(self, log):
        print(log.decode("utf-8"))

    def __texfile_process(self, fname, source):
        f = open(os.path.join(source, fname), "r")
        text = self.__nonbreaking_space(f.read())
        f.close()

        filename = "waved"+fname
        o = open(os.path.join(source, filename), "w")
        o.write(text)
        o.close()

        return filename

    def __zip_folder(self, path, folder, zipClass):
        # Find it all recursively
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            for f in files:
                zipClass.write(os.path.join(root, f), os.path.join(root[len(path):], f))

    def __process_line(self, line):
        command = "\graphicspath{{"
        auxfrs = line.find(command)
        if auxfrs != -1:
            auxsec = line[auxfrs:].find("}}")
            self.pic_folder = line[auxfrs+len(command):auxsec]
            self.pic_folder_abs=os.path.abspath(self.pic_folder)
        command = "\setcontentpath{"
        auxfrs = line.find(command)
        if auxfrs != -1:
            auxsec = line[auxfrs:].find("}")
            self.content_folder = line[auxfrs+len(command):auxsec]
        command = "\\addbibresource{"
        auxfrs = line.find(command)
        if auxfrs != -1:
            auxsec = line[auxfrs:].find("}")
            self.references = line[auxfrs+len(command):auxsec]

    def __get_list_of_file_numbers(self, option, len):
        newpg = []
        pages = []
        newpgbool = False
        fstpage = 0
        secpage = 0

        for i in option + ",":
            if i == " ":
                continue
            if i.isnumeric():
                if fstpage == 0:
                    fstpage = int(i)
                else:
                    fstpage = 10 * fstpage + int(i)
                continue
            if i == "n" or i == "N":
                newpgbool = True
                continue
            if i == ",":
                if secpage == 0:
                    if fstpage == 0:
                        continue
                    newpg.append(newpgbool)
                    pages.append(fstpage)
                    newpgbool = False
                    fstpage = 0
                else:
                    if fstpage == 0:
                        pages.extend(list(range(secpage, len + 1)))
                        newpg.extend([newpgbool] * (len + 1 - secpage))
                    else:
                        pages.extend(list(range(secpage, fstpage + 1)))
                        newpg.extend([newpgbool] * (fstpage + 1 - secpage))
                    fstpage = 0
                    secpage = 0
                    newpgbool = False
                continue
            if i == "-":
                if fstpage == 0:
                    secpage = 1
                else:
                    secpage = fstpage
                fstpage = 0
                continue
        if not pages or max(pages) > len:
            return ([], [])
        return (pages, newpg)

    def __process_content(self, option):
        files = sorted(os.listdir(os.path.join(self.project_path, self.content_folder)))
        pages = self.__get_list_of_file_numbers(option, len(files))
        if not pages[0]:
            return False
        str = "\n"
        for i in range(0, len(pages[0])):
            filename = self.__texfile_process(files[pages[0][i]-1], os.path.join(self.project_path, self.content_folder))
            if pages[1][i]:
                str += "\\addcontentwithnewpagetolist{"
                str += filename
                str += "}\n"
            else:
                str += "\\addcontenttolist{"
                str += filename
                str += "}\n"
        f = open(self.settings, "a")
        f.write(str)
        f.close()
        return True

    def __move_suffix_to_bin(self, suffix):
        files = os.listdir(self.project_path)
        for f in files:
            if f.endswith(suffix):
                src = os.path.join(self.project_path, f)
                dest = os.path.join(self.bin_folder, f)
                if os.path.exists(dest):
                    os.remove(dest)
                shutil.move(src, dest)

    def __move_content_waved_to_bin(self):
        files = os.listdir(self.content_folder)
        for f in files:
            if f[:5] == "waved":
                src = os.path.join(self.content_folder, f)
                dest = os.path.join(self.bin_folder, f)
                if os.path.exists(dest):
                    os.remove(dest)
                shutil.move(src, dest)

    def __move_all_to_bin(self):
        self.__move_suffix_to_bin(".aux")
        self.__move_suffix_to_bin(".bbl")
        self.__move_suffix_to_bin(".bcf")
        self.__move_suffix_to_bin(".blg")
        self.__move_suffix_to_bin(".log")
        self.__move_suffix_to_bin(".out")
        self.__move_suffix_to_bin(".toc")
        self.__move_suffix_to_bin(".mx1")
        self.__move_suffix_to_bin(".ext")
        self.__move_suffix_to_bin(".lof")
        self.__move_suffix_to_bin(".lot")
        self.__move_suffix_to_bin(".run.xml")
        self.__move_content_waved_to_bin()

    def __referencces_check(self):
        if not os.path.exists(self.references):
            return True

        ret = True

        with open(self.references, "r") as f:
            lines = f.readlines()

        f = open(self.references, "w")
        for i in range(len(lines)):
            if re.search("@*{,", lines[i]):
                ret = False
                print("References: On line " + str(i + 1) + " missing citations key.")

            if lines[i][:7] == "url = {":
                lines[i] = lines[i].replace("{\_}","_")
                lines[i] = lines[i].replace("{~}","~")

            f.write(lines[i])

        f.close()

        return ret

    ###### BUILD FUNCTION ######
    def build(self, content_options="-"):
        if not os.path.exists(self.bin_folder):
            os.makedirs(self.bin_folder)

        pdfcmd = " pdflatex -interaction=nonstopmode " + os.path.join(os.path.dirname(os.path.realpath(__file__)), self.main)
        bibcmd = " biber " + self.project_name + ".bcf"

        if not self.__referencces_check():
            print("Please fix it.")
            return

        if os.path.exists(self.settings):
            os.remove(self.settings)

        self.save(self.settings)
        if not self.__process_content(content_options):
            print("Wrong content files sequence.")
            return

        dest = os.path.dirname(os.path.realpath(__file__))
        if dest != self.project_path:
            dest = os.path.join(dest, self.settings)
            if os.path.exists(dest):
                os.remove(dest)
            os.symlink(os.path.join(self.project_path, self.settings), dest)

        try:
            self.frsOut = subprocess.check_output(pdfcmd , shell=True)
        except:
            print("Something in first compilation.tex files is wrong. Exception:", sys.exc_info()[0])
            self.__move_all_to_bin()
            return

        try:
            self.bibOut = subprocess.check_output(bibcmd , shell=True)
        except:
            print("Something in bibliography files is wrong. Exception:", sys.exc_info()[0])
            self.__move_all_to_bin()
            return

        try:
            self.frsOut = subprocess.check_output(pdfcmd , shell=True)
        except:
            print("Something in second compilation.tex files is wrong. Exception:", sys.exc_info()[0])
            self.__move_all_to_bin()
            return

        self.__move_all_to_bin()

    def clean(self):
        shutil.rmtree(self.bin_folder,ignore_errors=True)

    def clear(self):
        self.clean()

        file_path=os.path.join(self.project_path, self.pdf_name)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s : %s" % (file_path, e.strerror))

        file_path=self.project_path + self.project_name + ".zip"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s : %s" % (file_path, e.strerror))

    def only_base(self):
        self.clear()

        try:
            if os.path.exists("references.bib"):
                os.remove("references.bib")
            if os.path.exists("abstract.tex"):
                os.remove("abstract.tex")
            if os.path.exists("acknowledgments.tex"):
                os.remove("acknowledgments.tex")
            if os.path.exists("titlepage.tex"):
                os.remove("titlepage.tex")
            if os.path.exists("affidavit.tex"):
                os.remove("affidavit.tex")
            if os.path.exists("assignment.pdf"):
                os.remove("assignment.pdf")
            if os.path.exists("listofabbreviations.tex"):
                os.remove("listofabbreviations.tex")
            if os.path.exists("settings.tex"):
                os.remove("settings.tex")
            shutil.rmtree("content",ignore_errors=True)
            shutil.rmtree("pics",ignore_errors=True)

        except OSError as e:
            print("Error: %s : %s" % (e.strerror))

    def pack(self):
        zip = zipfile.ZipFile(self.project_name + ".zip", "w",zipfile.ZIP_DEFLATED)

        zip.write(self.project_name+".tex","./"+self.project_name+".tex")

        files = self.filesetting.get_files_list()
        for i in files:
            if "." not in files[i]:
                name = os.path.basename(files[i])
                zip.write(files[i]+".tex","./"+name+".tex")
            else:
                name = os.path.basename(files[i])
                zip.write(files[i],"./"+name)

        zip.write(self.references,"./"+self.references)

        self.__zip_folder(self.project_path, self.content_folder, zip)
        self.__zip_folder(self.project_path, self.pic_folder, zip)

        zip.close()

    def encrypt(self, own_passwd, usr_passwd):
        file_path=os.path.join(self.project_path, self.pdf_name)
        if not os.path.exists(file_path):
            print("Pdf for encryption does not exist.")

        try:
            import pikepdf
        except:
            print("For encryption must be enabled import of pikepdf packge.")
            print("Exitting encrypt.")
            return

        permiss=pikepdf.Permissions(accessibility=True,
                                extract=True,
                                modify_annotation=True,
                                modify_assembly=False,
                                modify_form=False,
                                modify_other=False,
                                print_highres=True,
                                print_lowres=True)
        encrypt=pikepdf.Encryption(user=usr_passwd, owner=own_passwd, allow=permiss)
        pdf=pikepdf.Pdf.open(file_path,allow_overwriting_input=True)
        pdf.save(file_path, encryption=encrypt)
        pdf.close()

        del pikepdf

    def cleanup(self):
        for f in os.listdir(self.project_path):
            if (
            f.endswith(".aux") or f.endswith(".bcf") or
            f.endswith(".log") or f.endswith(".out") or
            f.endswith(".blg") or f.endswith(".toc") or
            f.endswith(".mx1") or f.endswith(".run.xml")):
                try:
                    os.remove(os.path.join(self.project_path, f))
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

    def help(self):
        print("Unimplemented.")



    ###### RUNTIME ######
    def is_runtime(self, arg):
        if (arg == "build" or
            arg == "clean" or
            arg == "clear" or
            arg == "pack" or
            arg == "encrypt" or
            arg == "cleanup" or
            arg == "help" or
            arg == "print_settings" or
            arg == "save" or
            arg == "load" or
            arg == "run" or
            arg == "init" or
            arg == "onlyBase" or
            arg == "test"):
            return True
        return False

    def runtime(self, arg, atr=""):
        if arg == "init":
            if not os.path.exists(self.content_folder):
                os.makedirs(self.content_folder)
            self.save("settings.tex")
            return

        if arg == "build":
            if atr == "":
                self.build()
            else:
                self.build(atr)
            return

        if arg == "clean":
            self.clean()
            return

        if arg == "clear":
            self.clear()
            return

        if arg == "onlyBase":
            self.only_base()
            return

        if arg == "pack":
            self.pack()
            return

        if arg == "encrypt":
            if self.ask_pwd:
                usr=input("User  password: ")
                own=input("Owner password: ")
                self.encrypt(own, usr)
            else:
                self.encrypt(self.own_pwd, self.usr_pwd)
            return

        if arg == "cleanup":
            self.cleanup()
            return

        if arg == "help":
            self.help()
            return

        if arg == "print_settings":
            print(self.__get_settings())
            return

        if arg == "save":
            self.save("settings.tex")
            return

        if arg == "load":
            self.load("settings.tex")
            return

        if arg == "test":
            self.test()
            return

        print("Command " + arg + " does not exist.")

    def test(self):
        print("build")
        self.runtime("build")
        print("pack")
        self.runtime("pack")
        print("encrypt")
        self.runtime("encrypt")
        print("clean")
        self.runtime("clean")
        print("clear")
        self.runtime("clear")
        print("cleanup")
        self.runtime("cleanup")
        print("help")
        self.runtime("help")

    def __get_settings(self):
        str = self.filesetting.file_list_tostring()
        str += "\n"
        str += self.filesetting.print_list_tostring()
        str += "\n\\addbibresource{"
        str += self.references
        str += "}\n"
        str += "\n\graphicspath{{"
        str += self.pic_folder
        str += "}}\n"
        str += "\n"
        str += self.vars.get_commands_string()
        str += "\n\setcontentpath{"
        str += self.content_folder
        str += "}\n"
        return str

    def save(self, file):
        str = self.__get_settings()

        try:
            f = open(file, "w+")
            f.write(str)
            f.close()
        except:
            print("Something went wrong while writing the file.")

    def load(self, file):
        if not os.path.exists(file):
            print("File not found")
            return

        try:
            f = open(file, "r")
            lines = f.readlines()

            for line in lines:
                line = line.strip()
                line = re.sub(r'(?m)^ *%.*\n?', '', line)
                if line != "":
                    self.__process_line(line)
                    self.vars.process_line(line)
                    self.filesetting.process_line(line)
            f.close()
        except:
            print("Something goes wrong while reading the file.")
