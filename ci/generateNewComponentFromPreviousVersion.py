from pathlib import Path

import yaml
import json
import re
import os

##Enter the new version here
NEW_COMPONENT_VERSION= "v1.0.0"

# Example usage:
specifications_folder = Path(__file__).parents[1] / "specifications"  # Replace with your specifications folder path
schema_file = 'component.schema.json'  # Replace with your component.schema.json file path

def new_Component_yaml_Template(old_yaml):
    new_yaml = old_yaml.copy()
   
    #add_v1beta3_event_notification_changes(new_yaml, old_yaml)
    new_yaml['apiVersion'] = "oda.tmforum.org/" + NEW_COMPONENT_VERSION
    #Modify componentMetadata data
    addComponentMetadata(new_yaml)
    #ConvertDelimitersinETOMandFF
    convertDelimitersofETOMsFFs(new_yaml)
    #addAPISDO
    add_v1_api_SDO_changes(new_yaml)

    return new_yaml

def addComponentMetadata(spec):
    print("spec", spec)
    if 'componentMetadata' not in spec['spec']:
        spec['spec']['componentMetadata'] = {}
    spec_name=spec['spec']['name']
    spec_id=spec['spec']['id']
    spec['spec']['componentMetadata']['id'] = spec['spec'].pop('id')
    spec['spec']['componentMetadata']['name'] = spec['spec'].pop('name')
    spec['spec']['componentMetadata']['version'] = spec['spec'].pop('version')
    spec['spec']['componentMetadata']['description'] = spec['spec'].pop('description')
    spec['spec']['componentMetadata']['publicationDate'] = spec['spec'].pop('publicationDate')
    spec['spec']['componentMetadata']['status'] = spec['spec'].pop('status')
    spec['spec']['componentMetadata']['functionalBlock'] = spec['spec'].pop('functionalBlock')
    if 'owners' in spec['spec'] and isinstance(spec['spec']['owners'], list):
        spec['spec']['componentMetadata']['owners'] = spec['spec'].pop('owners')
        for owner in spec['spec']['componentMetadata']['owners']:
            if isinstance(owner, dict) and 'url' not in owner:
                owner['url'] = 'Redacted'
    if 'maintainers' in spec['spec'] and isinstance(spec['spec']['maintainers'], list):
        spec['spec']['componentMetadata']['maintainers'] = spec['spec'].pop('maintainers')
        for maintainer in spec['spec']['componentMetadata']['maintainers']:
            if isinstance(maintainer, dict) and 'url' not in maintainer:
                maintainer['url'] = 'Redacted'
    if 'eTOMs'in spec['spec'] and isinstance(spec['spec']['eTOMs'], list):
        spec['spec']['componentMetadata']['eTOMs'] = spec['spec'].pop('eTOMs')
    if 'functionalFrameworkFunctions'in spec['spec'] and isinstance(spec['spec']['functionalFrameworkFunctions'], list):
        spec['spec']['componentMetadata']['functionalFrameworkFunctions'] = spec['spec'].pop('functionalFrameworkFunctions')

def convertDelimitersofETOMsFFs(new_yaml):
    eTOMs = new_yaml['spec']['componentMetadata'].get("eTOMs",[])
    new_yaml['spec']['componentMetadata']['eTOMs'] = convert_etoms_format(eTOMs)
    functionalFrameworks = new_yaml['spec']['componentMetadata'].get("functionalFrameworkFunctions",[])
    new_yaml['spec']['componentMetadata']['functionalFrameworkFunctions'] = convert_etoms_format(functionalFrameworks)


def convert_etoms_format(etoms_list):
    converted_list = []
    for etom in etoms_list:
        # Replace the first underscore with a hyphen
        etom = re.sub(r'_', '-', etom, count=1)
        # Replace the last underscore before 'v' with a hyphen
        etom = re.sub(r'_(?=v\d+\.\d+$)', '-', etom)
        converted_list.append(etom)
    return converted_list

def extract_tmf_id(spec_url):
    """Extracts the TMF ID from the specification URL."""
    match = re.search(r'TMF\d+', spec_url)
    return match.group(0) if match else None

def load_yaml(file_path):
    """Loads a YAML file and returns the content as a Python dictionary."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_json(file_path):
    """Loads a JSON file and returns the content as a Python dictionary."""
    with open(file_path, 'r') as file:
        return json.load(file)

def save_yaml(data, file_path):
    """Saves a Python dictionary to a YAML file."""
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file, sort_keys=False)

def add_v1_api_SDO_changes(new_yaml):
    # Add the apiSDO in exposedAPIs and DependentAPIs 
    for apis in ['dependentAPIs','exposedAPIs']:
        if apis in new_yaml['spec']['coreFunction']:
            for api in new_yaml['spec']['coreFunction'][apis]:
                if api.get("id", "").startswith("TMF"):
                    api["apiSDO"] = "tmForum"

def add_v1beta3_event_notification_changes(new_yaml, old_yaml):
    
    # Extract and Add the publishedEvents
    for event_type in ['publishedEvents', 'subscribedEvents']:
        if event_type in new_yaml['spec']['coreFunction']:
            for event in new_yaml['spec']['coreFunction'][event_type]:
                if 'apitype' in event:
                    event['apiType'] = event.pop('apitype')
    

    
def apply_new_version_property_changes(new_yaml):
    changes_collection = get_newVersion_property_change_collection()
    for change in changes_collection:
        change_property_names(new_yaml, change['from_property'], change['to_property'])

    return new_yaml

def get_propertyList_with_Apis(yaml_data):
    properties_with_apis = []
    for functionName in yaml_data.get('spec', {}):
        # Check if dependentAPIs or exposedAPIs exist in the function section
        if isinstance(yaml_data['spec'].get(functionName, {}), (list, dict)):
            function_data = yaml_data['spec'].get(functionName, {})
            print("function_data", function_data)
            if 'dependentAPIs' in function_data:
                properties_with_apis.append(functionName)
        
            if 'exposedAPIs' in function_data:
                properties_with_apis.append(functionName)

    return properties_with_apis


def fill_template_with_values(schema, old_yaml):
    component_name = old_yaml['spec'].get('name')
    id = old_yaml['spec'].get('id')
    print("creating new yaml for ", component_name, id)

    # Step 1: Create a new YAML template based on new version component schema and old component specification YAML
    new_yaml = new_Component_yaml_Template(old_yaml)

    # Step 2: Return the new YAML file
    return new_yaml


def generate_new_version(schema_file, old_yaml_file, new_yaml_file):
    # Load the component schema and the previous version YAML file
    schema = load_json(schema_file)
    old_yaml = load_yaml(old_yaml_file)

    # Step 1: Validate if the apiVersion needs to be updated
    schema_api_version = NEW_COMPONENT_VERSION
    old_api_version = old_yaml['apiVersion']

    if schema_api_version == old_api_version:
        print(f"No version increment needed for {old_yaml_file}")
        return

    # Step 2: Apply the schema template to the old YAML values
    new_yaml = fill_template_with_values(schema, old_yaml)

    # Save the new YAML file
    save_yaml(new_yaml, new_yaml_file)
    print(f"New component version YAML saved to: {new_yaml_file}")

def process_all_yaml_files(specifications_folder, schema_file):
    print(f"Processing all YAML files in {specifications_folder}...")
    print("Schema file:", schema_file)
    print("Specifications folder:", specifications_folder)
    # Load the component schema to get the new apiVersion
    schema = load_json(schema_file)
    new_api_version = NEW_COMPONENT_VERSION

    
    # Get the parent directory of `specifications_folder`
    parent_dir = os.path.dirname(specifications_folder)
    # Define the new output folder based on the apiVersion
    output_folder = os.path.join(parent_dir, new_api_version)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Walk through the specifications folder, skipping the 'Template' folder
    for root, dirs, files in os.walk(specifications_folder):
        # Skip the 'Template' folder
        if 'Template' in dirs:
            dirs.remove('Template')

        for file in files:
            if file.endswith('.yaml'):
                # Get the full path of the current YAML file
                old_yaml_path = os.path.join(root, file)
                
                # Create the output path within the new apiVersion folder
                relative_path = os.path.relpath(root, specifications_folder)
                new_yaml_dir = os.path.join(output_folder, relative_path)
                if not os.path.exists(new_yaml_dir):
                    os.makedirs(new_yaml_dir)
                
                print('processing file: ', old_yaml_path)
                print('new yaml dir: ', new_yaml_dir)
                print('output folder: ', output_folder)

                new_yaml_path = os.path.join(new_yaml_dir, file)

                # Generate a new version of the YAML file
                generate_new_version(schema_file, old_yaml_path, new_yaml_path)

if __name__ == "__main__":
    process_all_yaml_files(specifications_folder, schema_file)
