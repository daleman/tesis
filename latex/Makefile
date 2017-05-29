options= -bibtex -interaction=nonstopmode -auxdir="../tmp" -output-directory="../tmp"


all: tesis presentacion concurso presentacion_eci

tesis:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

presentacion:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

concurso:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

presentacion_eci:
	cd src/ && \
	latexmk -pdf $@.tex $(options)
	cd tmp/ && \
	mv $@.pdf ..

clean:
	cd src/ && \
	latexmk -c tesis.tex $(options)
	rm -f tesis.pdf 
