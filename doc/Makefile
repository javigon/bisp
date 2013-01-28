TARGETS = \
	manual.pdf \

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

# main targets

manual.pdf: manual.tex manual.includes.timestamp
	pdflatex manual.tex
	pdflatex manual.tex

