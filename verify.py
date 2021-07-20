import json
import zlib
import os
import numpy as np

def crc(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def verify():
    data = os.listdir("data")

    manifest = open("manifest.json", "rb")
    manifest  = json.load(manifest)

    entries = [file for file in manifest]

    extra_files = np.setdiff1d(data, entries)
    missing_files = np.setdiff1d(entries, data)
    present_files = list(set(entries) - set(missing_files))
    available_files = []
    corrupted_files = []

    for file in present_files:
        if manifest[file]['crc'] == crc("data/{}".format(file)):
            available_files.append(file)
        else:
            corrupted_files.append(file)

    print("Available Files:")
    if (len(available_files) == 0):
        print("None")
    else:
        print("\n".join(available_files))
    print()

    print("Missing Files:")
    if (len(missing_files) == 0):
        print("None")
    else:
        print("\n".join(missing_files))
    print()

    print("Corrupted Files:")
    if (len(corrupted_files) == 0):
        print("None")
    else:
        print("\n".join(corrupted_files))   
    print()

    print("Extra Files:")
    if (len(extra_files) == 0):
        print("None")
    else:
        print("\n".join(extra_files))
    print()

    return available_files