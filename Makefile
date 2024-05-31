
CUR_DIR = $(shell pwd)

run:
	cd /42; \
	./42 ../$(CUR_DIR)/InOut

clean:
	rm -rf InOut/*.42
	rm -rf mc_*
	