#!/bin/bash
# Golden script for Python Data Analysis testing
# This is the CORRECT way to test the Python data analysis documentation

set -e

echo "=== Python Data Analysis Test Script ==="

# Step 1: Install dependencies
echo "Installing pandas and numpy..."
pip install pandas numpy

# Step 2: Create the analysis script
echo "Creating analyze.py..."
cat > analyze.py << 'EOF'
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
EOF

# Step 3: Create sample CSV data
echo "Creating data.csv..."
cat > data.csv << 'EOF'
name,age,score
Alice,25,85
Bob,30,92
Charlie,35,78
Diana,28,95
EOF

# Step 4: Run the analysis
echo "Running analysis..."
OUTPUT=$(python analyze.py data.csv)

# Step 5: Verify output contains expected statistics
echo "Verifying output..."
if echo "$OUTPUT" | grep -q "Rows: 4" && \
   echo "$OUTPUT" | grep -q "Columns: 3" && \
   echo "$OUTPUT" | grep -q "Mean:" && \
   echo "$OUTPUT" | grep -q "Median:" && \
   echo "$OUTPUT" | grep -q "Std Dev:"; then
    echo "✅ Analysis test successful!"
else
    echo "❌ Analysis test failed!"
    rm -f analyze.py data.csv
    exit 1
fi

# Cleanup
rm -f analyze.py data.csv

echo "=== All tests passed! ==="

