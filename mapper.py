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

def read_descriptions_from_file(file_path="descriptions.txt"):
    """
    Reads descriptions from a plain text file, one description per line.
    """
    if not os.path.exists(file_path):
        print(f"Error: Input file '{file_path}' not found.")
        print("Please create a file named 'descriptions.txt' with one description per line.")
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
    
    # 1. Load Rules
    mapping_rules = load_rules()

    if not mapping_rules:
        print("\nExiting. Rules could not be loaded.")
    else:
        # 2. Load Descriptions from File
        description_file = "descriptions.txt"
        test_descriptions = read_descriptions_from_file(description_file)

        if not test_descriptions:
            print(f"\nExiting. No descriptions found in '{description_file}'.")
        else:
            print("--- ABC TAXIOM MAPPING ENGINE ---")
            print(f"Processing {len(test_descriptions)} descriptions from '{description_file}'...")
            
            # 3. Apply Rules to each description
            for desc in test_descriptions:
                results = apply_rules(desc, mapping_rules)
                
                print(f"\nINPUT: '{desc}'")
                
                if results:
                    print(f"  Normalized: '{normalize(desc)}'")
                    print(f"  Match Count: {len(results)}")
                    for i, result in enumerate(results):
                        print(f"    Mapping {i+1} Short Name: {result['short_name']}")
                        print(f"    Mapping {i+1} Identifier: {result['identifier']}")
                else:
                    print(f"  Normalized: '{normalize(desc)}'")
                    print("  => NO MATCH FOUND. (Review rules.json)")