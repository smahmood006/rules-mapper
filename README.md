# ABC TAXIOM Mapping Engine

A Python-based rules engine that processes financial descriptions and maps them to standardized accounting categories using prioritized rules and boolean logic.

## Features

- **Text Normalization:** Standardizes descriptions (lowercase, removes punctuation, replaces symbols)
- **Rules Engine:** Applies 60+ prioritized mapping rules with complex boolean logic
- **Multi-Mapping Support:** Returns multiple mappings when applicable
- **Priority-Based Matching:** Highest priority matches take precedence

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd Rules-account

# Ensure Python 3.x is installed
python --version
```

## Usage

```bash
python mapper.py
```

The script will:
1. Load rules from `rules.json`
2. Read descriptions from `descriptions.txt`
3. Apply normalization and matching rules
4. Output mapping results

## Project Structure

```
Rules-account/
├── mapper.py             # Core mapping engine
├── rules.json            # Rule definitions (60+ rules)
├── descriptions.txt      # Input descriptions
├── descriptions.txt1     # Extended test data
├── README.md             # This file
└── GIT_REPORT.md         # Git repository report
```

## Rules

The mapping engine uses a priority-based rule system with:
- **Conditions:** AND, OR, NOT_AND logic
- **Negations:** Exclude patterns
- **Mappings:** Return standardized short names and identifiers
- **Priority:** Lower numbers = higher priority

## Example Output

```
INPUT: 'Trade Debtors'
  Normalized: 'trade debtors'
  Match Count: 1
    Mapping 1 Short Name: Trade Debtors (Default)
    Mapping 1 Identifier: currentAssets.tradeReceivables.tradeDebtors
```

## File Descriptions

- **mapper.py:** Contains normalization function, rules loading, and matching logic
- **rules.json:** JSON file with rule definitions including priorities, conditions, negations, and mappings
- **descriptions.txt:** Sample input data for testing

## Contributing

When adding new rules to `rules.json`:
1. Assign a unique `priority` number
2. Define `conditions` with type (AND/OR/NOT_AND) and keywords
3. Add `negations` to exclude patterns
4. Specify `mappings` with short_name and identifier

## License

[Specify your license here]

