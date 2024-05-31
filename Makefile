
CUR_DIR = $(shell pwd)

run: InOut
	cd /42; \
	./42 ../$(CUR_DIR)/InOut

# Copy InOut from 42 to current directory
InOut:
	cp -r /42/InOut .

Demo:
	cd /42; \
	./42 Demo

clean:
	rm -rf InOut/*.42
	rm -rf mc_*
	