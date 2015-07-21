
The problem:
You, the trigger-happy photographer, have over the years accumulated digital pictures running into tens of thousands. A good number of those are duplicates - mainly because you imported them from your camera multiple times or just created copies in different folders. Either way you want to get rid of duplicates.

The solution:
photobroom includes a set of tools to identify and delete duplicate photos. Actually, the tools just build a batch file (Windows) or a shell script (Linux). You have to manually run the script which then move the duplicate to a temporary directory which you can delete after you've had a chance to inspect the contents.

instructions:
1. Run: python inventory.py YOUR-TOPLEVEL-DIRECTORY. This may take a while to complete.
2. Run python parse.py from same directory. When duplicates are found you will be presented a list of directories which contain copies of photos. You will have to decide on a "keepdir". The software will keep the copy in the keepdir and delete all others (actually generate a line in the script which will move the duplicate into a temporary directory). For subsequent duplicates, if one of the directories is a keepdir, the software will automatically use it and not ask the question. If multiple keepdirs are found, one is chosen in random.
3. After step 2, the software generates script.bat and script.sh. On Windows, run script.bat. On Linux, run script.sh
4. All duplicates should now be in a tempdir. You may now delete the tempdir.
