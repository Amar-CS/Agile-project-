@echo off
rem Builds a single LoaderStore.exe (needs Python + internet once, to install PyInstaller)
python -m pip install --upgrade pyinstaller
python -m PyInstaller --noconfirm --onefile --noconsole --name LoaderStore --icon assets\loader-store.ico --add-data "static;static" desktop.py
echo.
echo Done: dist\LoaderStore.exe  (data is stored in %%APPDATA%%\LoaderStore)
pause
