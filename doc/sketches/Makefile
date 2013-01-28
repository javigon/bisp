TARGETS = \
	SimBuilding_overview.pdf \


all: $(TARGETS)

clean:
	rm -f $(TARGETS)

mrproper: clean
	rm -f *~


SimBuilding_overview.pdf: SimBuilding_overview.svg
	inkscape SimBuilding_overview.svg -z -C -A SimBuilding_overview.pdf
