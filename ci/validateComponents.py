from pathlib import Path
from jsonschema import validate

import json
import re
import yaml

COMPONENTS = Path(__file__).parents[1] / "specifications"
CI = Path(__file__).parents[1] / "ci"

# Components excluded from framework-format enforcement for now (pre-existing data
# issues not yet cleaned up). Remove an id here once its componentMetadata is fixed.
FRAMEWORK_FORMAT_SKIP_IDS = set()

ETOM_CODE_RE = re.compile(r'^\d+(\.\d+)+$')
FF_ID_RE = re.compile(r'^\d+$')
VERSION_RE = re.compile(r'^v\d+(\.\d+)*$')
SID_DOMAIN_RE = re.compile(r'.*_Domain$')

def str_constructor(loader, node):
    return loader.construct_scalar(node)

def validate_component_file_names_and_content():
    for spec in COMPONENTS.glob("TMFC*/*"):
        if not spec.name.startswith("TMFC") or not spec.name.endswith(".yaml"):
            if spec.suffix.lower() == ".pdf":
                continue  # skip PDF files
            if "BDD" in spec.parts or "ComponentRI" in spec.parts or "ComponentConformanceProfile" in spec.parts or "Diagrams" in spec.parts:
                continue
            print(f"::group::TMFC File Naming is invalid")
            print(f"::error::{spec.name}")
            print("::endgroup::")
            return 1

        try:
            with spec.open("r") as f:
                yaml.load(f, Loader=yaml.SafeLoader)
                print(f"{spec.name} content is valid")
        except yaml.parser.ParserError as e:
            print(f"::group::Error while parsing {spec.name}  .yaml; Content is invalid")
            print(f"::error::{e}")
            print("::endgroup::")
            return 1
        except Exception as e:
            print(f"::group::{spec.name} Content is invalid")
            print(f"::error::{e}")
            print("::endgroup::")
            return 1

    for spec in COMPONENTS.rglob("*"):
        if " " in spec.name:
            print(f"::group::TMFC File Naming is invalid")
            print(f"::error::{spec.relative_to(COMPONENTS)} contains a space")
            print("::endgroup::")
            return 1

    return 0

def load_components():
    for spec in COMPONENTS.glob("TMFC*/*.yaml"):
        with spec.open("r") as f:
            yield spec, yaml.load(f, Loader=yaml.SafeLoader)

def load_json_schema():
    with CI.joinpath("component.schema.json").open("r") as f:
        return json.load(f)

def validate_apis(component):
    functions = ["coreFunction", "securityFunction", "managementFunction"]
    pass


def _check_pipe_delimited_list(name, field_name, values, code_re, code_label):
    """Validate a componentMetadata list of '<code>|<Name>|v<version>' strings
    (used by eTOMs and functionalFrameworkFunctions)."""
    errors = 0
    if values is None:
        # Missing key or explicit `null` is treated the same as an empty array - valid.
        return 0
    if not isinstance(values, list):
        print(f"::group::{name}")
        print(f"::error::componentMetadata.{field_name} is not an array: {type(values).__name__}")
        print("::endgroup::")
        return 1

    seen = {}
    for entry in values:
        if not isinstance(entry, str):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.{field_name} entry is not a string: {entry!r}")
            print("::endgroup::")
            errors = 1
            continue

        parts = entry.split('|')
        if len(parts) != 3:
            print(f"::group::{name}")
            print(f"::error::componentMetadata.{field_name} entry '{entry}' must have exactly 3 "
                  f"pipe-delimited fields (code|name|version), found {len(parts)}")
            print("::endgroup::")
            errors = 1
            continue

        code, entry_name, version = parts
        if not code_re.match(code):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.{field_name} entry '{entry}': {code_label} '{code}' "
                  f"does not match the expected pattern")
            print("::endgroup::")
            errors = 1
        if ' ' in code or ' ' in entry_name:
            print(f"::group::{name}")
            print(f"::error::componentMetadata.{field_name} entry '{entry}' contains a raw space "
                  f"(expected underscore in code/name fields)")
            print("::endgroup::")
            errors = 1
        if not VERSION_RE.match(version):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.{field_name} entry '{entry}': version '{version}' "
                  f"does not match the expected vN[.N...] pattern")
            print("::endgroup::")
            errors = 1

        if code in seen:
            print(f"::group::{name}")
            if seen[code] == entry:
                print(f"::error::componentMetadata.{field_name} has an exact duplicate entry: '{entry}'")
            else:
                print(f"::error::componentMetadata.{field_name} id '{code}' is used by two different "
                      f"entries: '{seen[code]}' and '{entry}'")
            print("::endgroup::")
            errors = 1
        seen[code] = entry

    return errors


def _check_sid_list(name, values):
    """Validate componentMetadata.SIDs: '<Domain>|<...ABE/BE segments...>|v<version>' strings."""
    errors = 0
    if values is None:
        # Missing key or explicit `null` is treated the same as an empty array - valid.
        return 0
    if not isinstance(values, list):
        print(f"::group::{name}")
        print(f"::error::componentMetadata.SIDs is not an array: {type(values).__name__}")
        print("::endgroup::")
        return 1

    seen = set()
    for entry in values:
        if not isinstance(entry, str):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs entry is not a string: {entry!r}")
            print("::endgroup::")
            errors = 1
            continue

        parts = entry.split('|')
        if len(parts) < 3:
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs entry '{entry}' must have at least 3 pipe-delimited "
                  f"fields (domain|...ABE segments...|version), found {len(parts)}")
            print("::endgroup::")
            errors = 1
            continue

        domain = parts[0]
        version = parts[-1]
        if not SID_DOMAIN_RE.match(domain):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs entry '{entry}': first field '{domain}' does not "
                  f"end in '_Domain'")
            print("::endgroup::")
            errors = 1
        if any(' ' in seg for seg in parts):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs entry '{entry}' contains a raw space "
                  f"(expected underscore in path segments)")
            print("::endgroup::")
            errors = 1
        if not VERSION_RE.match(version):
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs entry '{entry}': version '{version}' does not "
                  f"match the expected vN[.N...] pattern")
            print("::endgroup::")
            errors = 1

        if entry in seen:
            print(f"::group::{name}")
            print(f"::error::componentMetadata.SIDs has an exact duplicate entry: '{entry}'")
            print("::endgroup::")
            errors = 1
        seen.add(entry)

    return errors


def validate_framework_formats(component, name):
    cm = component.get("spec", {}).get("componentMetadata", {}) or {}
    if cm.get("id") in FRAMEWORK_FORMAT_SKIP_IDS:
        return 0

    errors = 0
    errors |= _check_pipe_delimited_list(name, "eTOMs", cm.get("eTOMs"), ETOM_CODE_RE, "eTOM code")
    errors |= _check_pipe_delimited_list(
        name, "functionalFrameworkFunctions", cm.get("functionalFrameworkFunctions"), FF_ID_RE, "FF id"
    )
    errors |= _check_sid_list(name, cm.get("SIDs"))
    return errors


def validate_component(schema, component, name):
    errors = 0
    try:
        validate(instance=component, schema=schema)
        #validate_apis(component)
    except Exception as e:
        errors = 1
        print(f"::group::{name}")
        print(f"::error::{e}")
        print("::endgroup::")
    return errors


def main():
    component_schema = load_json_schema()
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:timestamp', str_constructor)
    return_code = 0
    return_code |= validate_component_file_names_and_content()
    for file_path, component in load_components():
        name = file_path.parent.name
        return_code |= validate_component(component_schema, component, name)
        return_code |= validate_framework_formats(component, name)

    if return_code == 0:
        print("All components are valid")
    return return_code


if __name__ == "__main__":
    import sys
    sys.exit(main())
