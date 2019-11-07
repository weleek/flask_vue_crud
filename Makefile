
.PHONY: install
install:
		pip install -r requirements.txt

.PHONY: clean
clean:
		rm -rf dist

.PHONY: build
build:
		echo "build" $(args)
