from pathlib import Path
import json
import os

FILE_CHANGES = Path(__file__).parents[2] / "filechanges"

def read_file_changes():
    with open(FILE_CHANGES, 'r') as f:
        return f.readlines()


def fileter_changes(changes):
    for line in changes:
        if "template" in line:
            continue
        if "specifications" in line:
            yield line.strip()

def main():
    changes = read_file_changes()
    changes = fileter_changes(changes)
    print(list(changes))
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())