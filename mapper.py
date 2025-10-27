import json
import re
import os

# --- STEP 1: NORMALIZATION ---

def normalize(description):
    """
    Standardizes the description text as required by the methodology.
    """
    if not description:
        return ""
        
    # 1. Convert to lowercase
    normalized = description.lower()
    
    # 2. Replace common symbols and standardize words
    normalized = normalized.replace('&', 'and')
    
    # 3. Remove punctuation and extra spacing (e.g., 'P.A.Y.E.' becomes 'paye')
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

# --- STEP 2: FILE UTILITIES ---

def load_rules(file_path="rules.json"):
    """
    Loads rules from a JSON file and sorts them by priority.
    """
    try:
        with open(file_path, 'r') as f:
            rules = json.load(f)
    except FileNotFoundError:
        print(f"Error: Rules file not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in {file_path}. Check for trailing commas or comments.")
        print(f"Details: {e}")
        return []

    # Sort rules by 'priority' (lower number = higher priority/more specific)
    return sorted(rules, key=lambda x: x.get('priority', 999))

def get_description_files():
    """
    Returns a list of available description files in the current directory.
    Filters for .txt files that start with 'description'.
    """
    description_files = []
    for file in os.listdir('.'):
        if file.startswith('description') and file.endswith('.txt'):
            description_files.append(file)
    return sorted(description_files)

def select_input_file():
    """
    Displays available description files and allows user to select one.
    Returns the selected file path.
    """
    description_files = get_description_files()
    
    if not description_files:
        print("\nNo description files found in the current directory.")
        print("Looking for files starting with 'description' and ending with '.txt'")
        return None
    
    if len(description_files) == 1:
        print(f"\nFound one description file: {description_files[0]}")
        return description_files[0]
    
    print("\nAvailable description files:")
    for i, file in enumerate(description_files, 1):
        print(f"  {i}. {file}")
    
    while True:
        try:
            choice = input(f"\nSelect a file (1-{len(description_files)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(description_files):
                return description_files[choice_num - 1]
            else:
                print(f"Please enter a number between 1 and {len(description_files)}")
        except ValueError:
            print("Please enter a valid number or 'q' to quit")

def read_descriptions_from_file(file_path):
    """
    Reads descriptions from a plain text file, one description per line.
    """
    if not file_path:
        return []
        
    if not os.path.exists(file_path):
        print(f"Error: Input file '{file_path}' not found.")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # Read lines, strip leading/trailing whitespace, and filter out blank lines
            descriptions = [line.strip() for line in f if line.strip()]
        return descriptions
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return []


# --- STEP 3: THE RULES ENGINE ---

def apply_rules(description, rules):
    """
    Applies the rule set to the description based on priority and boolean logic.
    Returns a list of matching mappings (for multi-mappings) or an empty list.
    """
    normalized_desc = normalize(description)
    
    for rule in rules:
        
        # 1. Check Negations (NOT logic)
        is_negated = False
        for neg_keyword in rule.get('negations', []):
            if neg_keyword in normalized_desc:
                is_negated = True
                break
        if is_negated:
            continue
            
        # 2. Check Conditions (AND/OR/NOT_AND logic)
        is_match = True
        for condition in rule.get('conditions', []):
            keywords = condition.get('keywords', [])
            condition_type = condition.get('type')
            
            if condition_type == 'AND':
                # All keywords must be present
                if not all(k in normalized_desc for k in keywords):
                    is_match = False
                    break 
            
            elif condition_type == 'OR':
                # At least one keyword must be present
                if not any(k in normalized_desc for k in keywords):
                    is_match = False
                    break
            
            elif condition_type == 'NOT_AND':
                # If ALL keywords in NOT_AND list are present, it fails the rule
                if all(k in normalized_desc for k in keywords):
                    is_match = False
                    break
        
        # 3. If matched, return the mappings and stop (Rule Prioritization)
        if is_match:
            return rule.get('mappings', []) 
            
    # No rule matched
    return []

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    
    print("--- ABC TAXIOM MAPPING ENGINE ---\n")
    
    # 1. Load Rules
    mapping_rules = load_rules()

    if not mapping_rules:
        print("Exiting. Rules could not be loaded.")
    else:
        # 2. Let user select description file
        description_file = select_input_file()
        
        if not description_file:
            print("Exiting. No file selected.")
        else:
            # 3. Load Descriptions from Selected File
            test_descriptions = read_descriptions_from_file(description_file)

            if not test_descriptions:
                print(f"\nExiting. No descriptions found in '{description_file}'.")
            else:
                print(f"\nProcessing {len(test_descriptions)} descriptions from '{description_file}'...\n")
                
                # 4. Apply Rules to each description
                for desc in test_descriptions:
                    results = apply_rules(desc, mapping_rules)
                    
                    print(f"INPUT: '{desc}'")
                    
                    if results:
                        print(f"  Normalized: '{normalize(desc)}'")
                        print(f"  Match Count: {len(results)}")
                        for i, result in enumerate(results):
                            print(f"    Mapping {i+1} Short Name: {result['short_name']}")
                            print(f"    Mapping {i+1} Identifier: {result['identifier']}")
                    else:
                        print(f"  Normalized: '{normalize(desc)}'")
                        print("  => NO MATCH FOUND. (Review rules.json)")
                    print()