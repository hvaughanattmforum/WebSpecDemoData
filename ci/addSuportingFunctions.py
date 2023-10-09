import yaml
import os
import json
from pathlib import Path
from git import Repo

ODA_CANVAS_REPO = Path(__file__).parents[2] / "TMForum-ODA-Canvas-Specification"
RELEASE_REPO = Path(__file__).parents[2] / "TMForum-ODA-Ready-for-publication" / "specifications"

def get_functions():
    functions_folder = Path(ODA_CANVAS_REPO) / "supporting-functions"
    print("Functions folder exists: ", functions_folder.exists())
    for function_file in functions_folder.glob("*.yaml"):
        with function_file.open() as f:
            yield yaml.safe_load(f)

def get_specifications(version):
    specs = Path(__file__).parents[1] / "specifications"
    print("Specs folder exists: ", specs.exists())
    for spec_file in specs.glob("TMFC*/**/*.yaml"):
        with spec_file.open() as f:
            yield yaml.safe_load(f), spec_file

def add_supporting_functions(spec, spec_path, functions):
    print("Adding supporting functions to ", spec_path)
    function_names = ["managementFunction", "securityFunction"]
    for name in function_names:
        spec[name] = functions[name]

    OUTPUT_FOLDER = RELEASE_REPO / spec_path.parent.name
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    print("Output folder exists: ", OUTPUT_FOLDER.exists())
    with (OUTPUT_FOLDER / spec_path.name).open("w+") as f:
        yaml.safe_dump(spec, f)

def main():
    for function in get_functions():
        for spec, spec_path in get_specifications():
            add_supporting_functions(spec, spec_path, function)
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())