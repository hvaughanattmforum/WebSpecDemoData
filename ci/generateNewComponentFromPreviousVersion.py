from pathlib import Path

import yaml
import json
import re
import os

##Enter the new version here
NEW_COMPONENT_VERSION= "v1beta3"

# Example usage:
specifications_folder = Path(__file__).parents[1] / "specifications"  # Replace with your specifications folder path
schema_file = 'component.schema.json'  # Replace with your component.schema.json file path

def new_Component_yaml_Template(old_yaml):
    new_yaml = {
        'apiVersion': "oda.tmforum.org/" + NEW_COMPONENT_VERSION,
        'kind': old_yaml.get('kind'),
        'metadata': {
            'name': old_yaml['metadata'].get('name')
        },
        'spec': {
            'name': old_yaml['spec'].get('name'),
            'id': old_yaml['spec'].get('id'),
            'functionalBlock': old_yaml['spec'].get('functionalBlock'),
            'description': old_yaml['spec'].get('description'),
            'publicationDate': old_yaml['spec'].get('publicationDate', None),
            'status': old_yaml['spec'].get('status', None),
            'version': old_yaml['spec'].get('version'),
            'coreFunction': {
                'dependentAPIs': old_yaml['spec']['coreFunction'].get('dependentAPIs', []),
                'exposedAPIs': old_yaml['spec']['coreFunction'].get('exposedAPIs', [])
            }
        }
    }
    
    # Add 'maintainers' and 'owners' if they exist in old YAML
    if old_yaml['spec'].get('maintainers'):
        new_yaml['spec']['maintainers'] = old_yaml['spec'].get('maintainers')
    
    if old_yaml['spec'].get('owners'):
        new_yaml['spec']['owners'] = old_yaml['spec'].get('owners')

    # Add 'eventNotification' only if published or subscribed events are in the old YAML
    if old_yaml['spec'].get('eventNotification'):
        new_yaml['spec']['eventNotification'] = {
            'publishedEvents': old_yaml['spec']['eventNotification'].get('publishedEvents', []),
            'subscribedEvents': old_yaml['spec']['eventNotification'].get('subscribedEvents', [])
        }
        add_v1beta3_event_notification_changes(new_yaml, old_yaml)
    elif old_yaml['spec']['coreFunction'].get('publishedEvents') or old_yaml['spec']['coreFunction'].get('subscribedEvents'):
        # Adding published and subscribed events data from old YAML
        new_yaml['spec']['eventNotification'] = {
            'publishedEvents': old_yaml['spec']['coreFunction'].get('publishedEvents', []),
            'subscribedEvents': old_yaml['spec']['coreFunction'].get('subscribedEvents', [])
        }
        add_v1beta3_event_notification_changes(new_yaml, old_yaml)

    # Add 'managementFunction' only if it exists in old YAML
    if old_yaml['spec'].get('managementFunction'):
        new_yaml['spec']['managementFunction'] = {
            'dependentAPIs': old_yaml['spec']['managementFunction'].get('dependentAPIs', []),
            'exposedAPIs': old_yaml['spec']['managementFunction'].get('exposedAPIs', [])
        }

    # Add 'securityFunction' only if it exists in old YAML
    if old_yaml['spec'].get('securityFunction'):
        new_yaml['spec']['securityFunction'] = {
            'secretsManagement': {
                'type': old_yaml['spec']['securityFunction'].get('secretsManagement', {}).get('secretManagementType', None),
                'sideCar': old_yaml['spec']['securityFunction'].get('secretsManagement', {}).get('sideCar', None),
                'podSelector': old_yaml['spec']['securityFunction'].get('secretsManagement', {}).get('podSelector', None)
            },
            'dependentAPIs': old_yaml['spec']['securityFunction'].get('dependentAPIs', []),
            'exposedAPIs': old_yaml['spec']['securityFunction'].get('exposedAPIs', []),
            'controllerRole': old_yaml['spec']['securityFunction'].get('controllerRole', None)
        }
    
    return new_yaml

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

def add_v1beta3_event_notification_changes(new_yaml, old_yaml):
    
    # Extract and Add the publishedEvents and subscribedEvents IDs
    for event_type in ['publishedEvents', 'subscribedEvents']:
        if event_type in new_yaml['spec']['eventNotification']:
            for event in new_yaml['spec']['eventNotification'][event_type]:
                spec_url = event.get('specification', '')
                event_id = extract_tmf_id(spec_url)
                event['id'] = event_id
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


def add_requiredFields_to_functionSection(new_yaml, old_yaml, schema):
    #functionNamesWithAPIs = ["coreFunction", "managementFunction", "securityFunction"]
    functionNamesWithAPIs= get_propertyList_with_Apis(new_yaml)
    # Handle the `functions` section based on the required fields in the schema definition
    for functionName in functionNamesWithAPIs:
        exposedAPIs_schema = schema['definitions'].get('apiSchemaExposed', {}).get('required', [])
        print("exposedAPIs_schema before", exposedAPIs_schema)
        if(exposedAPIs_schema == None):
            exposedAPIs_schema = schema['properties'].get('spec', {}).get('properties', {}).get(functionName, {}).get('properties', {}).get('exposedAPIs', []).get('required', [])

        print("exposedAPIs_schema after", exposedAPIs_schema)
        exposed_apis_oldyaml = old_yaml['spec'].get(functionName, {}).get('exposedAPIs', [])

        dependentAPIs_schema = schema['definitions'].get('apiSchemaDependent', {}).get('required', [])
        print("dependentAPIs_schema before", dependentAPIs_schema)
        if(dependentAPIs_schema == None):
            dependentAPIs_schema = schema['properties'].get('spec', {}).get('properties', {}).get(functionName, {}).get('properties', {}).get('dependentAPIs', []).get('required', [])
        print("dependentAPIs_schema after", dependentAPIs_schema)

        dependent_apis_oldyaml = old_yaml['spec'].get(functionName, {}).get('dependentAPIs', [])
    
        for required_prop in exposedAPIs_schema:
            for index, api in enumerate(exposed_apis_oldyaml):
                print(f"! index  {index}, API  {api}")
                # Ensure required properties are checked inside each API in 'exposedAPIs'
                if required_prop not in api:
                    print(f"! spec missing required field {required_prop} in {functionName} -> exposedAPIs[{index}]")
                    if(required_prop == "apiType"):
                        new_yaml['spec'][functionName]['exposedAPIs'][index][required_prop] = 'openapi'
                    elif(required_prop == "port"):
                        new_yaml['spec'][functionName]['exposedAPIs'][index][required_prop] = 80
                    else:
                        new_yaml['spec'][functionName]['exposedAPIs'][index][required_prop] = '_must_be_defined'
       
        for required_prop in dependentAPIs_schema:
            for index, api in enumerate(dependent_apis_oldyaml):
                # Ensure required properties are checked inside each API in 'dependentAPIs'
                if required_prop not in api:
                    print(f"! spec missing required field {required_prop} in {functionName} -> dependentAPIs[{index}]")
                    if(required_prop == "apiType"):
                        new_yaml['spec'][functionName]['dependentAPIs'][index][required_prop] = 'openapi'
                    elif(required_prop == "port"):
                        new_yaml['spec'][functionName]['dependentAPIs'][index][required_prop] = 80
                    else:
                        new_yaml['spec'][functionName]['dependentAPIs'][index][required_prop] = '_must_be_defined'

def add_requiredFields_to_specSection(new_yaml,old_yaml, schema):
    # Handle the `spec` section based on the schema definition
    spec_required_fields = schema['properties'].get('spec', {}).get('required', [])
    for required_prop in spec_required_fields:
        if required_prop not in old_yaml['spec']:
            print("! spec missing required field", required_prop)
            if(required_prop == "apiType"):
                new_yaml['spec'][required_prop] = old_yaml['spec'].get(required_prop, 'openapi')
            elif(required_prop == "port"):
                new_yaml['spec'][required_prop] = old_yaml['spec'].get(required_prop, 80)
            else:
                new_yaml['spec'][required_prop] = old_yaml['spec'].get(required_prop, '_must_be_defined')
            

def add_requiredFields_to_metadataSection(new_yaml, old_yaml, schema):
    metadata_required_fields = schema['properties'].get('metadata', {}).get('required', [])
    for field in metadata_required_fields:
        if field not in new_yaml['metadata']:
            print("! metadata missing field", field)
            new_yaml['metadata'][field] = old_yaml['metadata'].get(required_prop, '_must_be_defined')

def add_requiredFields_to_topLevelSection(new_yaml, old_yaml, schema):
    # Handling required top-level required fields
    top_level_required_fields = schema.get('required', [])
    for field in top_level_required_fields:
        if field not in new_yaml:
            print("! top level missing field", field)
            new_yaml[field] = old_yaml.get(field, '_must_be_defined')



def fill_template_with_values(schema, old_yaml):
    component_name = old_yaml['spec'].get('name')
    id = old_yaml['spec'].get('id')
    print("creating new yaml for ", component_name, id)

    # Step 1: Create a new YAML template based on new version component schema and old component specification YAML
    new_yaml = new_Component_yaml_Template(old_yaml)


    # Step 2: Apply the required fileds if they are missing to the new YAML template
    add_requiredFields_to_functionSection(new_yaml, old_yaml, schema)
    add_requiredFields_to_specSection(new_yaml, old_yaml, schema)
    add_requiredFields_to_metadataSection(new_yaml, old_yaml, schema)
    add_requiredFields_to_topLevelSection(new_yaml, old_yaml, schema)

    # Step 3: Return the new YAML file
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

    # Define the new output folder based on the apiVersion
    output_folder = os.path.join(specifications_folder, new_api_version)
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
