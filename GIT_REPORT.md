# Git Repository Report

## Repository Overview
**Repository Location:** C:/Code/Rules-account  
**Initialized:** October 27, 2025  
**Status:** Active

## Commit History

### Commit 1: Initial commit
- **Commit Hash:** a595b71
- **Author:** Developer <developer@example.com>
- **Date:** Mon Oct 27 21:54:51 2025 +0000
- **Message:** Initial commit: Add mapper.py, rules.json, and descriptions

### Files Changed:
| File | Status | Lines Added | Lines Deleted |
|------|--------|-------------|---------------|
| descriptions.txt | Created | 9 | 0 |
| descriptions.txt1 | Created | 103 | 0 |
| mapper.py | Created | 150 | 0 |
| rules.json | Created | 659 | 0 |

**Total:** 4 files changed, 921 insertions(+)

## Repository Statistics

### File Breakdown:
- **Python Files:** 1 (mapper.py - 150 lines)
- **JSON Files:** 1 (rules.json - 659 lines)
- **Text Files:** 2 (descriptions.txt - 9 lines, descriptions.txt1 - 103 lines)

### Total Lines of Code: 921

## Project Structure
```
Rules-account/
├── descriptions.txt        # Input descriptions (9 items)
├── descriptions.txt1      # Extended descriptions (103 items)
├── mapper.py             # Mapping engine with normalization and rules
├── rules.json            # Comprehensive rule definitions
└── GIT_REPORT.md         # This report
```

## Project Description

This is a **RSM TAXIOM Mapping Engine** project that processes financial descriptions and maps them to standardized accounting categories using a rules-based system.

### Key Features:
1. **Normalization:** Standardizes text by converting to lowercase, replacing symbols, and removing punctuation
2. **Rules Engine:** Applies prioritized rules with boolean logic (AND, OR, NOT_AND conditions and negations)
3. **Comprehensive Mapping:** 60+ rules covering various financial categories:
   - Fixed Assets (Cost, Depreciation, Disposals)
   - Current Assets (Stock, Debtors, Cash)
   - Current Liabilities (Creditors, Tax, Accruals)
   - P&L Items (Revenue, Expenses, Depreciation)
   - Non-Current Liabilities
   - Equity

### Main Components:
- **mapper.py:** Core engine with normalization and rule application logic
- **rules.json:** Priority-ordered rules with conditions and mappings
- **descriptions.txt/descriptions.txt1:** Test data for the mapping engine

## Next Steps
Consider adding:
- A README.md with usage instructions
- Test cases for the mapper
- Configuration files (if needed)
- .gitignore file
- Documentation for rule priority logic

