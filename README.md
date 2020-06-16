# media_manager
## Description
This utility will take a directory tree and scour it for photos and videos with a size greater than 250KB and sort them into a target directory structure based on the creation date of the object.

## Requirements
Python 3

## Usage
1. Create an empty file called .media_manager_source in the directory of media you want to organize
2. Create an empty file called .media_manager_target in the directory of the target parent folder to copy the media to
3. `python3 import_media.py`

These filenames can be changed in config.yml
The Minimum file size can be changed in config.yml

## Future Improvements
1. Keep history of found source and target files to speed up searching when importing from the same place in the future (useful for importing from SD card
2. Put a graphical front end on this to increase the WAFactor
3. Create option for deleting source files that are successfully imported after integrity check
4. Find a faster method to compare files when a conflict arises
5. Build in decision making for resolving conflicts
