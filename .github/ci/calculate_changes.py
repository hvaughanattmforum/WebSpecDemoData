from pathlib import Path
import json
import os

FILE_CHANGES = Path(__file__).parents[2] / "filechanges"

def read_file_changes():
    with open(FILE_CHANGES, 'r') as f:
        return f.readlines()


def fileter_changes(changes):
    for line in changes:
        if "Template" in line:
            continue
        if "specifications" in line:
            yield line.strip()

def main(args):
    changes = read_file_changes()
    changes = fileter_changes(changes)
    components_changes = [Path(p).stem for p in changes]
    output = f"components={json.dumps(components_changes)}"
    print(output)
    print(args[1])

    with Path(args[1]).open('a+') as f:
        f.write(output + "\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))