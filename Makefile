darwin: # macOS release
	pyinstaller --onefile --console src/main.py
	mv dist/main NBody
	mkdir -p release
	zip -r "release/NBody-darwin.zip" NBody resources/

linux: # Linux release
	pyinstaller --onefile --console src/main.py
	mv dist/main NBody
	mkdir -p release
	zip -r "release/NBody-linux.zip" NBody resources/

windows: # Windows release
	pyinstaller --onefile --console .\src\main.py
	move .\dist\main.exe .\NBody.exe
	if exist .\release rd /s /q .\release
	mkdir release
	zip -r "release/NBody-windows.zip" .\NBody.exe .\resources\

clean: # Linux and macOS only
	rm -rf __pycache__ build dist data release
	rm -rf *.spec NBody