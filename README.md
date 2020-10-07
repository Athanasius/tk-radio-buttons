# Introduction
During development of the [Elite Dangerous Market Connector](https://github.com/EDCD/EDMarketConnector)
(EDMC) project we were made aware of an issue when using Windows 10 UI Scaling.
This appears to be a Tk bug with python tkinter.ttk.RadioButton elements when
using some level of UI scaling if the executable involved has the `dpiAware`
manifest setting set true.

## Windows UI Scaling
Some users with high resolution/DPI monitors don't want a small application
window so they make use of a Windows 10 feature to scale their UI up.

Specifically this is accessed via:

1. Right-click desktop.
1. Select `Display settings`.
1. Ensure the desired display is selected.
1. Scroll down to `Scale and layout`.
1. Change the scaling option `Change the size of text, apps and other items`
  to e.g. 150%.

Any application run after changing this setting will respect that new setting.

## dpiAware manifest option
There is a manifest option you can set on Windows executables, as per
[Application Manifests](https://docs.microsoft.com/en-us/windows/win32/sbscs/application-manifests#dpiaware),
which informs the OS that the application is DPI aware.

The effect of this in practice is that, when used in conjunction with UI
Scaling as documented above, the rendered text and other UI elements will be
much sharper than without it.

The EDMC application is processed into a .exe using [py2exe](https://github.com/albertosottile/py2exe)
upon which the manifest is then set.

## The bug
Unfortunately when you have some UI Scaling set along with dpiAware set true
you might find that radio buttons are mis-rendered.  The usual manifestation
of this is that the currently selected button will be properly sized initially,
with the others being undersized.  If you even only mouse-over the selected
radio button it will then become undersized as well.

This does not occur either without UI Scaling active (have it set to 100%), or
if dpiAware is not set true.

## Reproducing the bug
In order to more simply reproduce the bug the `edmc.py` script in this
repository was created.  In EDMC we observe this in the Settings/Preferences
dialog, so this `edmc.py` script re-creates the same circumstances with a main
window that has a `File` menu with a `Prefs` entry that then opens a new
`ttk.TopLevel` window to contain a `ttk.Notebook` which then contains a frame
with the test `ttk.RadioButton` elements.

As the bug depengs on `dpiAware` being true you can't just run the script with
a normal python.exe.  Instead you will need to:

1. If you want to package to a .exe using py2exe then you can use either Python
3.7.x or 3.8.x.  We've specifically tested using Python 3.7.9 and py2exe
[0.9.3.2](https://github.com/albertosottile/py2exe/releases/tag/v0.9.3.2).
We've done some basic testing with Python 3.8.6 and py2exe 0.10.0.1 and have
no reason to believe this bug would change between the versions.
    1. `python setup.py py2exe` will produce a binary as `dist.win32\edmc-like-tk-radio-buttons.exe`
    1. `cd dist.win32` and run the .exe from there (else it won't find
      necessary files).
    1. To set the manifest you need `mt.exe` from a Windows SDK, e.g.
    `"c:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\mt.exe"`.
    
        `"c:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\mt.exe"
        -manifest ..\edmc-like-tk-radio-buttons_dpiaware.manifest
        -outputresource:edmc-like-tk-radio-buttons.exe`

1. If you don't trust what py2exe does then alternatively:
    1. Make a copy of python.exe into your clone of this project.
    1. Use mt.exe to set an alternate manifest on it:
    
        `"c:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\mt.exe"
        -manifest python_dpiAware.manifest
        -outputresource:python.exe`
    
        That manifest file was produced by using:
    
        `"c:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x86\mt.exe
        " -inputresource:python.exe -out:python.manifest`
        
        to extract the default manifest, then adding:
    
        `<dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>`
    
        to the `<windowsSettings>` section.
    
    1. Now you need to set PYTHONPATH so that your copied python.exe can find
    its libraries.
        1. Run the actually installed python.exe (so change directory out of
        this project).
            ```
            python.exe -i
            >>> import sys
            >>> sys.path
            ```
        1. Then use `set PYTHONPATH=<that output without the [] brackets>` 
        
        The file `python-local-edmc.bat` contains an example of this, but
        specific to my setup.
       
    1. Run the script:
        `python.exe edmc.py`
        
Now use the `File` menu and select the `Prefs` option to open the additional
window and observe the state of the radio buttons.