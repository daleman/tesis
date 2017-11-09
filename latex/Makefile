.PHONY: all tesis presentacion clean
    
options= -bibtex -interaction=nonstopmode -auxdir="../tmp" -output-directory="../tmp"


all: tesis presentacion

tesis:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

presentacion:
	cd presentacion/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

clean:
	cd src/ && \
	latexmk -c tesis.tex $(options)
	rm -f tesis.pdf 
