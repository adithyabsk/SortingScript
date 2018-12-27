#!/usr/bin/env python

import os
import os.path
from glob import glob
from collections import defaultdict
import shutil


def tree():
    return defaultdict(tree)


def get_files(current_path):
    return [
        y
        for x in os.walk(current_path)
        for y in glob(os.path.join(x[0], "*.*"))
        if not any(e in y for e in (".py", ".exe"))
    ]


def get_exec_path():
    return os.path.dirname(os.path.realpath(__file__))


def create_dirs(directory, current_path):
    if len(directory):
        for direc in directory:
            create_dirs(directory[direc], os.path.join(current_path, direc))
    else:
        try:
            os.makedirs(current_path)
        except OSError as e:
            if e.errno != os.errno.EEXIST:
                raise


def get_dedup(file_path):
    if os.path.isfile(file_path):
        dirname = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        fname, ext = os.path.splitext(basename)
        counter = 1
        while True:
            new_path = os.path.join(dirname, "{}copy{}{}".format(fname, counter, ext))
            if not os.path.isfile(new_path):
                break
            else:
                counter += 1

        return new_path
    else:
        return file_path


# Source: https://gist.github.com/jacobtomlinson/9031697
def remove_empty_dirs(path, removeRoot=True):
    """Function to remove empty folders"""

    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_dirs(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0 and removeRoot:
        os.rmdir(path)


def sort_files():
    curr_path = get_exec_path()
    file_list = get_files(curr_path)
    dirs = [s.split(".")[-1].lower() for s in file_list]
    tree_struct = tree()
    for d in dirs:
        tree_struct[d]
    if tree_struct:
        create_dirs(tree_struct, curr_path)
    else:
        print("No files found!")
        quit()
    for f_path in file_list:
        ext = f_path.split(".")[-1].lower()
        new_f_path = os.path.join(curr_path, ext, os.path.basename(f_path))
        if not f_path == new_f_path:
            new_f_path = get_dedup(new_f_path)
            shutil.move(f_path, new_f_path)
        else:
            pass # File is already sorted

    # Clean up
    remove_empty_dirs(curr_path, False)


if __name__ == "__main__":
    sort_files()
