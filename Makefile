unix: # Linux and macOS
	pyinstaller --onefile --console src/main.py
	mv dist/main NBody

windows: # Windows release
	pyinstaller --onefile --console .\src\main.py
	move .\dist\main.exe .\NBody.exe

clean: # Linux and macOS only
	rm -rf src/__pycache__ build dist data release
	rm -rf *.spec NBody