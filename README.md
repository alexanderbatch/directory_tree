# Directory Tree Generator

## Overview
The `directory_tree.py` script generates a visual representation of the directory structure 
from a specified root directory. This output can be directed to either the standard output 
(console) or a specified file. The script is designed to help visualize the layout of files and 
directories in a project and includes configurable options for handling symbolic links.

## Features
- Generate a directory tree for any specified directory.
- Output the directory tree to the console or to a file.
- Optional following of symbolic links (shortcuts).
- Safe mode to restrict following symbolic links (shortcuts) to prevent loops.

## How It Can Be Helpful & Use Cases
The `directory_tree.py` helper script is useful for scenarios including:

### Documentation and Analysis
- **Project Documentation**: Automatically generate a directory structure for project documentation,
  making it easier for new contributors to understand the project layout.
- **Code Analysis**: Quickly analyze the structure of a codebase to understand file organization and
  module relationships.

### Development and Debugging
- **Debugging**: Helps in identifying how files are organized in a project which can be crucial for
  debugging issues related to file paths.
- **Refactoring**: Provides a clear view before and after refactoring to validate changes in the
  directory structure.

### Backup and Archiving
- **Pre-Archive Overview**: Generate a tree view before archiving projects for a clear understanding
  of what is being archived.
- **Backup Logs**: Create logs of directory structures to keep track of what has been backed up.  

## Setup and Usage

### Requirements
- Python 3.x

### Installation
No installation is required, just ensure Python is installed.

### Note
While a mock output file (`directory_tree_output.txt`) and a unit test file (`test_directory_tree.py`)
are included in this repository for demonstration purposes, you only need to keep and use the
`directory_tree.py` file for generating directory trees. These additional files are provided to help
you understand the expected output and to facilitate testing of the script.

### Running the Script
Place the `directory_tree.py` file in any directory you wish. Open a command line interface:

#### For Windows
1. Open Command Prompt.
2. Navigate to the directory containing `directory_tree.py`.
3. Execute the script with Python, specifying the root directory:
   ```cmd
   python directory_tree.py "C:\path\to\directory"
   ```
   Replace `"C:\path\to\directory"` with the path to the directory you want to visualize.

#### For macOS and Linux
1. Open Terminal.
2. Navigate to the directory containing `directory_tree.py`.
3. Execute the script with Python, specifying the root directory:
   ```bash
   python3 directory_tree.py "/path/to/directory"
   ```
   Replace `"/path/to/directory"` with the path to the directory you want to visualize.

### Optional Arguments
- `-o` or `--output_file`: Specify a file to write the output to.
- `-l` or `--follow_symlinks`: Enable following symbolic links.
- `-s` or `--safe_mode`: Enable safe mode to restrict following symbolic links.

Example command with all options:
```cmd (or bash)
python directory_tree.py "C:\path\to\directory" -o "C:\path\to\output.txt" -l -s
```
Replace `"C:\path\to\directory"` with the path to the directory you want to visualize 
and `"C:\path\to\output.txt"` with the path where you want the output file to be saved. 
The `-l` option enables following symbolic links (shortcuts), 
and `-s` enables safe mode to restrict following symbolic links to prevent loops.

## TODO List

- **Ignore Files or Paths**: Implement functionality to exclude specific files or 
  directories from the generated directory tree.
- **Improve Format Output**: Enhance the visual formatting of the output to increase 
  readability and include more detailed information about each file and directory.
- **Additional Information**: Add options to include additional information such as 
  file sizes, permissions, and last modified in the directory tree.
- **Performance Optimization**: Optimize the script for faster execution, especially 
  for large directory structures.
- **Export Options**: Allow exporting the directory tree to formats like JSON, XML, 
  or HTML for easy integration with other tools.

## Created by:
Alexander Batch