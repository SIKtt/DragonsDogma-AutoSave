# Dragon's Dogma 2 Auto Save
Auto backup and restore your steam savefile.  \
Steam's remote storage path ``*\Steam\userdate\uid\2054970\remote\win64_save``

### with wxpython requirements
```
python gui.py
```
or package with `PyInstaller`
```
pyi-makespec --onefile --windowed gui.py
pyinstaller gui.spec
.\dist\gui.exe
```

### Run as windows service
```
PS >  python test.py install
PS > Start-Service -Name "DDAutoSave"
```
