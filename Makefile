
CUR_DIR = $(shell pwd)

run:
	cd /home/user/42; \
	./42 ../py42/InOut

clean:
	rm -rf InOut/*.42
	rm -rf mc_*
	