# Python Data Analysis - CSV Statistics

A simple script to analyze CSV files and compute statistics.

## Prerequisites

- Python 3.8+
- pip

## Installation

### 1. Install required libraries

```bash
pip install pandas numpy
```

### 2. Create the analysis script

Create `analyze.py`:

```python
import pandas as pd
import numpy as np
import sys

def analyze_csv(filename):
    """Analyze a CSV file and print statistics."""
    try:
        df = pd.read_csv(filename)
        
        print(f"Dataset: {filename}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")
        print("\nColumn Statistics:")
        
        for col in df.select_dtypes(include=[np.number]).columns:
            print(f"\n{col}:")
            print(f"  Mean: {df[col].mean():.2f}")
            print(f"  Median: {df[col].median():.2f}")
            print(f"  Std Dev: {df[col].std():.2f}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze.py <csv_file>")
        sys.exit(1)
    
    success = analyze_csv(sys.argv[1])
    sys.exit(0 if success else 1)
```

### 3. Create sample data

Create `data.csv`:

```csv
name,age,score
Alice,25,85
Bob,30,92
Charlie,35,78
Diana,28,95
```

### 4. Run the analysis

```bash
python analyze.py data.csv
```

You should see statistics for age and score columns!

## Verification

The script should display mean, median, and standard deviation for numeric columns.

