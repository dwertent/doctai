#!/bin/bash
# Golden script for Node.js CLI tool testing
# This is the CORRECT way to test the Node.js CLI documentation

set -e

echo "=== Node.js CLI Tool Test Script ==="

# Step 1: Create project directory
echo "Creating project directory..."
mkdir -p file-counter
cd file-counter

# Step 2: Initialize npm project
echo "Initializing npm project..."
npm init -y

# Step 3: Install dependencies
echo "Installing dependencies..."
npm install commander chalk

# Step 4: Create the CLI tool
echo "Creating index.js..."
cat > index.js << 'EOF'
#!/usr/bin/env node

const fs = require('fs');
const { program } = require('commander');
const chalk = require('chalk');

program
  .version('1.0.0')
  .argument('<file>', 'file to count lines in')
  .action((file) => {
    try {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n').length;
      console.log(chalk.green(`File has ${lines} lines`));
    } catch (error) {
      console.error(chalk.red(`Error: ${error.message}`));
      process.exit(1);
    }
  });

program.parse();
EOF

# Step 5: Update package.json with bin
echo "Updating package.json..."
npm pkg set bin.count-lines="./index.js"

# Step 6: Make executable and link
echo "Making executable and linking..."
chmod +x index.js
npm link

# Step 7: Create test file
echo "Creating test file..."
cat > test.txt << 'EOF'
line 1
line 2
line 3
EOF

# Step 8: Test the CLI
echo "Testing CLI..."
OUTPUT=$(count-lines test.txt)

# Verify output
if echo "$OUTPUT" | grep -q "3 lines"; then
    echo "✅ CLI test successful!"
else
    echo "❌ CLI test failed!"
    cd ..
    rm -rf file-counter
    exit 1
fi

# Cleanup
cd ..
rm -rf file-counter

echo "=== All tests passed! ==="

