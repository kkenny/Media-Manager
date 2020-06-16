#!/usr/bin/env python

import os
import shutil
import hashlib
import time
import yaml
from pathlib import Path

class GenericErrorHandler(Exception):
    """Exception raised for generic errors."""

    def __init__(self, error="Generic", message="Undefined error."):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.error} -> {self.message}'


with open('config.yml', 'r') as ymlfile:
    CFG = yaml.load(ymlfile, Loader=yaml.SafeLoader)


dir_path = os.path.dirname(os.path.realpath('/'))

def _find_dir(media_dir):
    """Find the directory of the media we want to import"""

    print(f'Searching for directory containing {media_dir}...\t')

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == media_dir:
                print(f'{root}\n')
                return root
                break


def _find_media(source_dir):
    """Find images in the source directory"""

    types = ('*.JPG', '*.jpg',
            '*.JPEG', '*.jpeg',
            '*.NEF', '*.nef',
            '*.RW2', '*.rw2',
            '*.MOV', '*.mov',
            '*.MPEG', '*.mpeg',
            '*.MP4', '*.mp4')

    files = []

    for ft in types:
        files.extend(list(Path(source_dir).rglob(ft)))

    #result = list(Path(source_dir).rglob("*.[jJ][pP][gG]|*.[jJ][pP][eE][gG]"))

    return files

def _check_file_size(s):
    if ( s < CFG['min_file_size'] ):
        return False
    else:
        return True


def _get_md5hash(s):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(s, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(BLOCKSIZE)

    return hasher.hexdigest()


def _copy_media(s, d):
    """Copy media from list of found files to destination directory"""


    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(s)

    c_year = time.strftime("%Y", time.localtime(ctime))
    c_month = time.strftime("%m", time.localtime(ctime))
    c_day = time.strftime("%d", time.localtime(ctime))

    t_path = Path(d) / Path(c_year) / Path(c_month) / Path(c_day)
    t = (t_path) / (s.name)

    # Test if d exists
    if not t_path.exists():
        # Create d
        os.makedirs(t_path)

    if not t_path.is_dir():
        # Raise error, because d exists and is a file
        raise GenericErrorHandler("Files and Directories", f'{Path(d)} is not a directory.')

    # Test if s already exists at d
    if not t.exists():
        if ( _check_file_size(size) == True ):
            print(f'Copying {s} to {t}...')

            shutil.copy(s, t)

            # TODO: move this to a function and call it.
            #try:
            #    with t.open(mode='xb') as fid:
            #        fid.write(s.read_bytes())
            #finally:
            #    fid.close()
    else:
        print(f'Testing md5 hash for {s} against {t}')
        if ( _get_md5hash(s) != _get_md5hash(t) ):
            print(f'WARNING: {s} md5sum does not match {t}')
        else:
            print(f'INFO: {s} already exists at {t} and matches.')


target_dir = _find_dir(CFG['target_indicator'])

print("Starting Import...\n")

for x in _find_media(_find_dir(CFG['source_indicator'])):
    _copy_media(x, target_dir)

print("\nFinished Importing.\n")

# TODO: append a file on the source to notate the timestamp of most recent import
