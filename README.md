# SpotlightToBackground
Simple Python script to import Windows Spotlight images into a slideshow directory for screen saver
Requires Python 3.6 or greater and the Pillow library:
* pip install Pillow>=5.4.1

To install so that it runs at bootup:
1.  Copy the SpotlightToBackground.py file to your local disk. Mine is in Documents,
  - e.g., C:\Users\\<username\>\Documents\SpotlightToBackground.py
2. Navigate to C:\Users\\<username\>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup in Explorer
  - You may have to enable visbility of hidden directories to do this
3. Create a new Shortcut with:
  - Target: "python.exe C:\Users\\<username\>\Documents\SpotlightToBackground.py"
  - Run: Minimized
