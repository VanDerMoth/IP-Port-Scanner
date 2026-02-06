.PHONY: help install run build clean

help:
	@echo "IP Port Scanner - Makefile Commands"
	@echo "===================================="
	@echo "make install    - Install dependencies"
	@echo "make run        - Run the application"
	@echo "make build      - Build Linux executable"
	@echo "make clean      - Clean build artifacts"

install:
	@echo "Installing dependencies..."
	pip3 install -r requirements.txt

run:
	@echo "Running IP Port Scanner..."
	python3 port_scanner.py

build:
	@echo "Building Linux executable..."
	@mkdir -p dist
	pyinstaller --onefile --windowed --name=ip-port-scanner port_scanner.py
	@echo "Build complete! Executable available at: dist/ip-port-scanner"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist __pycache__ *.spec
	@echo "Clean complete!"
