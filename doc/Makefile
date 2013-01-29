TARGETS = \
	manual.pdf \
	presentation.pdf \

# general targets

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

mrproper: clean
	rm -f *~

# helper targets

includes:
	mkdir includes

manual.includes.timestamp: includes manual.tex
	cd .. ; generate-tex-includes PDF doc/manual.tex doc/
	touch manual.includes.timestamp

presentation.includes.timestamp: includes presentation.tex
	cd .. ; generate-tex-includes PDF doc/presentation.tex doc/
	touch presentation.includes.timestamp

# main targets

manual.pdf: manual.tex manual.includes.timestamp
	pdflatex manual.tex
	pdflatex manual.tex

presentation.pdf: presentation.tex presentation.includes.timestamp
	pdflatex presentation.tex
	pdflatex presentation.tex

