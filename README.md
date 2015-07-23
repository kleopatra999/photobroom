
The problem:
You, the trigger-happy photographer, have over the years accumulated digital pictures running into tens of thousands. A good number of those are duplicates - mainly because you imported them from your camera multiple times or just created copies in different folders. Either way you want to get rid of duplicates.

The solution:
photobroom includes a set of tools to identify and delete duplicate photos. Actually, the tools just build a batch file (Windows) or a shell script (Linux). You have to manually run the script which then move the duplicate to a temporary directory which you can delete after you've had a chance to inspect the contents.

Prerequisites:
You need to download and install Python (http://www.python.org) if not already installed. This software has been tested with Python 2.7.

Instructions:

1. Run: python inventory.py YOUR-TOPLEVEL-DIRECTORY. This may take a while to complete. On Windows you must run it on command shell or powershell.

2. Run python process.py from same directory. When duplicates are found you will be presented a list of directories which contain copies of photos. You will have to decide on a "keepdir". The software will keep the copy in the keepdir and delete all others (actually generate a line in the output script which will move the duplicate into a temporary directory when run). For subsequent duplicates, if one of the directories is a keepdir, the software will automatically use it and not ask the question. If multiple keepdirs are found, one is chosen in random. You can kill the session at any time (CTRL-C), and the next time you run process.py, it will not ask you the questions it has already asked (assuming you've not messed around with the database file it creates).

3. After step 2, the software generates script.bat and script.sh. You should take a look at one of the files to make sure everything looks OK. On Windows, run script.bat. On Linux, run script.sh

4. All duplicates should now be in a temp dir. You may now delete the temp dir.
