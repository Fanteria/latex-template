#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess
import zipfile

bin_folder="bin/"
project_path="./"
project_name="projekt"
pdf_name=".pdf"
content_folder="content/"
frsOut = ""
bibOut = ""
secOut = ""

def nonbreaking_space(text):
    text = re.sub(r' ([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r' \1~', text)
    text = re.sub(r' ([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r' \1~', text)
    text = re.sub(r'~([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r'~\1~', text)
    text = re.sub(r'~([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r'~\1~', text)
    text = re.sub(r'\n([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{1}) ', r'\n\1~', text)
    text = re.sub(r'\n([a-zA-Z0-9ěščřžýáíéňťďĚŠČŘŽÝÁÍÉŇŤĎ]{2}) ', r'\n\1~', text)

    return text


def printLog(log):
    #print(str(log).encode("utf-8").decode("unicode_escape"))
    print(log.decode("utf-8"))


def texfile_process(fname, source, dest):
        f = open(source+fname, "r")
        text = nonbreaking_space(f.read())
        f.close()

        o = open(dest+fname, "w")
        o.write(text)
        o.close()



###### BUILD FUNCTION ######

def build():
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

    texfile_process("cestneProhlaseni.tex", project_path, bin)
    texfile_process("titulniStrana.tex", project_path, bin)
    texfile_process("podekovani.tex", project_path, bin)

    for i in os.listdir(sourceContent):
        if i.endswith(".tex"):
            texfile_process(i, sourceContent, content)

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


def clean():
    bin=project_path+bin_folder
    shutil.rmtree(bin,ignore_errors=True)


def clear():
    clean()

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


def pack():
    zip = zipfile.ZipFile(project_name + ".zip", "w",zipfile.ZIP_DEFLATED)

    zip.write(project_path+"LICENSE","./"+"LICENSE")
    zip.write(project_path+"README.md","./"+"README.md")

    zip.write(project_path+project_name+".tex","./"+project_name+".tex")
    zip.write(project_path+"literatura.bib","./"+"literatura.bib")
    zip.write(project_path+"zadani.pdf","./"+"zadani.pdf")

    zip.write(project_path+"cestneProhlaseni.tex","./"+"cestneProhlaseni.tex")
    zip.write(project_path+"titulniStrana.tex","./"+"titulniStrana.tex")
    zip.write(project_path+"podekovani.tex","./"+"podekovani.tex")

    

    zip.close()

def help():
    print("Unimplemented.")


if __name__ == "__main__":
    project_path=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))+"/"
    pdf_name=project_name + pdf_name

    clear()
