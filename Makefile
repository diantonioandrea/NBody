clean:
	rm -rf __pycache__ build dist data release
	rm -rf *.spec NBody

darwin: # macOS release
	pyinstaller --onefile --console main.py
	mv dist/main NBody
	mkdir -p release
	zip -r "release/NBody-darwin.zip" NBody resources/