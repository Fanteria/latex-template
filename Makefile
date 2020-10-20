#
# Makefile for generate pdf
#

name = projekt
folder = bin

.PHONY: build
.PHONY: encrypt
.PHONY: clean
.PHONY: clear
.PHONY: help

build:
	@pdflatex $(name).tex; \
	 biber $(name).bcf; \
	 pdflatex $(name).tex; \
	 mkdir -p $(folder); \
	 mv -f *.aux $(folder); \
	 mv -f *.bbl  $(folder); \
	 mv -f *.bcf  $(folder); \
	 mv -f *.log  $(folder); \
	 mv -f *.out  $(folder); \
	 mv -f *.blg  $(folder); \
	 mv -f *.toc  $(folder); \
	 mv -f *.run.xml  $(folder); \

encrypt: build
	@qpdf projekt.pdf --encrypt "" own 128 --accessibility=y --extract=y --print=full --assemble=n --$
	 mv out.pdf $(name).pdf

clean:
	@rm -rf bin

clear: clean
	@rm -f $(name).pdf

help:
	@echo "build:    Generate pdf file."; \
	 echo "encrypt   Encrypt pdf file."; \
	 echo "clear:    Delete all generated files."; \
	 echo "clean:    Delete all temporary files."; \
	 echo "help:     Print help for Makefile."

