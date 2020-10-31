#!/usr/bin/env python3
import os
import re
import sys
import shutil
import zipfile
import subprocess

bin_folder="bin/"
pic_folder="pics/"
project_path="./"
project_name="projekt"
pdf_name=".pdf"
content_folder="content/"

usr_pwd=""
own_pwd="own"

frsOut = ""
bibOut = ""
secOut = ""

class TemplateMake:

    def __init__(self):
        print("TemplateMake init.")

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

    def __texfile_process(self, fname, source, dest):
        f = open(source+fname, "r")
        text = self.__nonbreaking_space(f.read())
        f.close()

        o = open(dest+fname, "w")
        o.write(text)
        o.close()

    def __zip_folder(self, path, folder, zipClass):
        # Find it all recursively
        for root, dirs, files in os.walk(os.path.join(path, folder)):
            for f in files:
                zipClass.write(os.path.join(root, f), os.path.join(root[len(path):], f))


    ###### BUILD FUNCTION ######
    def build(self):
        bin=project_path+bin_folder
        if not os.path.exists(bin):
            os.makedirs(bin)

        sourceContent=project_path+content_folder
        content=project_path+bin_folder+content_folder
        if not os.path.exists(content):
            os.makedirs(content)

        shutil.copy(project_path+project_name+".tex",bin+project_name+".tex")
        shutil.copy(project_path+"literatura.bib",bin+"literatura.bib")
        shutil.copy(project_path+"zadani.pdf",bin+"zadani.pdf")

        self.__texfile_process("cestneProhlaseni.tex", project_path, bin)
        self.__texfile_process("titulniStrana.tex", project_path, bin)
        self.__texfile_process("podekovani.tex", project_path, bin)

        for i in os.listdir(sourceContent):
            if i.endswith(".tex"):
                self.__texfile_process(i, sourceContent, content)

        if os.system("cd " + bin):
            print("Something went wrong. Cannot acess bin folder.")
            return

        pdfcmd = "cd " + bin + "; pdflatex -interaction=nonstopmode " + project_name + ".tex"
        bibcmd = "cd " + bin + "; biber " + project_name + ".bcf"

        try:
            frsOut = subprocess.check_output(pdfcmd , shell=True)
        except:
            print("Something in firs compilation.tex files is wrong. Exception:", sys.exc_info()[0])

        try:
            bibOut = subprocess.check_output(bibcmd , shell=True)
        except:
            print("Something in bibliography files is wrong. Exception:", sys.exc_info()[0])

        try:
            frsOut = subprocess.check_output(pdfcmd , shell=True)
        except:
            print("Something in second compilation.tex files is wrong. Exception:", sys.exc_info()[0])

        shutil.move(bin+pdf_name, project_path+pdf_name)

    def clean(self):
        bin=project_path+bin_folder
        shutil.rmtree(bin,ignore_errors=True)

    def clear(self):
        self.clean()

        file_path=project_path+pdf_name
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s : %s" % (file_path, e.strerror))

        file_path=project_path + project_name + ".zip"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError as e:
                print("Error: %s : %s" % (file_path, e.strerror))

    def pack(self):
        zip = zipfile.ZipFile(project_name + ".zip", "w",zipfile.ZIP_DEFLATED)

        zip.write(project_path+"LICENSE","./"+"LICENSE")
        zip.write(project_path+"README.md","./"+"README.md")

        zip.write(project_path+project_name+".tex","./"+project_name+".tex")
        zip.write(project_path+"literatura.bib","./"+"literatura.bib")
        zip.write(project_path+"zadani.pdf","./"+"zadani.pdf")

        zip.write(project_path+"cestneProhlaseni.tex","./"+"cestneProhlaseni.tex")
        zip.write(project_path+"titulniStrana.tex","./"+"titulniStrana.tex")
        zip.write(project_path+"podekovani.tex","./"+"podekovani.tex")

        self.__zip_folder(project_path, content_folder, zip)
        self.__zip_folder(project_path, pic_folder, zip)

        zip.close()

    def encrypt(self, own_passwd, usr_passwd=""):
        file_path=project_path+pdf_name
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
        for f in os.listdir(project_path):
            if (
            f.endswith(".aux") or f.endswith(".bcf") or
            f.endswith(".log") or f.endswith(".out") or
            f.endswith(".blg") or f.endswith(".toc") or
            f.endswith(".run.xml")):
                try:
                    os.remove(os.path.join(project_path, f))
                except OSError as e:
                    print("Error: %s : %s" % (f, e.strerror))

    def help(self):
        print("Unimplemented.")



    ###### RUNTIME ######
    def runtime(self, arg):

        if arg == "build":
            self.build()
            return

        if arg == "clean":
            self.clean()
            return

        if arg == "clear":
            self.clear()
            return

        if arg == "pack":
            self.pack()
            return

        if arg == "encrypt":
            self.encrypt(own_pwd)
            return

        if arg == "cleanup":
            self.cleanup()
            return

        if arg == "help":
            self.help()
            return

        print("Command " + arg + " does not exist.")


###### MAIN ######
if __name__ == "__main__":
    project_path=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))+"/"
    pdf_name=project_name+pdf_name


    run=TemplateMake()

    if len(sys.argv) == 1:
        run.runtime("build")
        exit()

    for i in range(1, len(sys.argv)):
        run.runtime(sys.argv[i])
