# Node.js CLI Tool - File Counter

A simple command-line tool to count lines in files.

## Prerequisites

- Node.js 16+ and npm

## Installation

### 1. Initialize project

```bash
mkdir file-counter
cd file-counter
npm init -y
```

### 2. Install dependencies

```bash
npm install commander chalk
```

### 3. Create the CLI tool

Create `index.js`:

```javascript
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
```

### 4. Make it executable

Add to `package.json`:

```json
{
  "bin": {
    "count-lines": "./index.js"
  }
}
```

Then run:

```bash
chmod +x index.js
npm link
```

### 5. Test the CLI

```bash
echo "line 1
line 2
line 3" > test.txt

count-lines test.txt
```

You should see: `File has 3 lines`

## Verification

The CLI tool should successfully count lines in any file.

