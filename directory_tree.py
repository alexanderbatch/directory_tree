import os
import sys
import argparse
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


class DirectoryTree:
    """
    Class to generate visual directory tree starting from specified root path.
    """
    def __init__(self, root_path, output_file=None, follow_symlinks=False,
                 safe_mode=True, ignore_list=None):
        """
        Initialize DirectoryTree object with root path and configuration.

        Args:
            root_path (str): Root directory path from which to generate tree.
            output_file (str, optional): Path to file where tree will be written.
            follow_symlinks (bool, optional): Whether to follow symbolic links.
            safe_mode (bool, optional): If True, restricts following symbolic links.
            ignore_list (list, optional): List of file/directory names to ignore.
        """
        self.root_path = os.path.abspath(root_path)
        self.output_file = output_file
        self.follow_symlinks = follow_symlinks # shortcuts
        self.safe_mode = safe_mode
        self.ignore_list = ignore_list or []
        self.visited = set()
        self.safe_root = os.path.realpath(self.root_path)

    def generate_tree(self):
        """
        Generate directory tree and output it to specified file or stdout.
        """
        output = self.open_output_file()
        logger.info(
            f"Outputting directory tree to: {self.output_file if self.output_file else 'stdout'}"
        )
        try:
            self.walk_directory(output)
        finally:
            if self.output_file:
                output.close()

    def open_output_file(self):
        """
        Open output file in write mode or configure stdout for writing.

        Returns:
            file object: File object or sys.stdout configured for writing.
        """
        if self.output_file:
            return open(self.output_file, 'w', encoding='utf-8')
        else:
            sys.stdout.reconfigure(encoding='utf-8')
            return sys.stdout

    def walk_directory(self, output):
        """
        Walk through directory tree and process each directory and file.

        Args:
            output (file object): Output file or stdout to write tree to.
        """
        for root, dirs, files in os.walk(self.root_path, topdown=True,
                                         followlinks=self.follow_symlinks):
            dirs.sort()  # Ensure consistent order
            self.process_directory(root, dirs, files, output)

    def process_directory(self, root, dirs, files, output):
        """
        Process each directory, writing its structure to output.

        Args:
            root (str): Current directory path.
            dirs (list): List of subdirectories in current directory.
            files (list): List of files in current directory.
            output (file object): Output file or stdout to write to.
        """
        # Calculate depth level of current directory relative to root
        level = root.replace(self.root_path, '').count(os.sep)
        # Create indentation based on directory level
        indent = '|   ' * (level - 1) if level > 0 else ''
        if level > 0:
            parent_path, _ = os.path.split(root)
            parent_dirs = next(os.walk(parent_path))[1]
            # Choose appropriate branch symbol based on position in parent
            if root == os.path.join(parent_path, parent_dirs[-1]):
                indent += '└── '
            else:
                indent += '├── '
        output.write(f"{indent}{os.path.basename(root)}/\n")
        if os.path.basename(root) in self.ignore_list:
            output.write(f"{indent}|   ...\n")
            dirs[:] = []  # Clear dirs list to prevent walking into them
            return  # Skip processing children
        self.process_files(files, level, output)
        # Only add vertical bar if there are subdirectories or files
        if dirs:
            subindent = '|   ' * level + '|'
            output.write(f"{subindent}\n")

    def process_files(self, files, level, output):
        """
        Process each file in current directory, writing to output.

        Args:
            files (list): List of files in current directory.
            level (int): Depth level of current directory.
            output (file object): Output file or stdout to write to.
        """
        subindent = '|   ' * level
        for f in files:
            if f not in self.ignore_list:
                output.write(f"{subindent}|   {f}\n")
        # Do not add extra vertical bar after last file
        if not files and not dir:
            subindent = '|   ' * level
            output.write(f"{subindent}\n")

def parse_args():
    """
    Parse command-line arguments.

    Returns:
        Namespace: Namespace with command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate a directory tree")
    parser.add_argument('root_path', type=str, help="Directory path to list")
    parser.add_argument('-o', '--output_file', type=str, help="Output to file")
    parser.add_argument('-i', '--ignore_list', nargs='*', default=[],
                        help="List of directories or files to ignore")
    parser.add_argument('-l', '--follow_symlinks', action='store_true',
                        help="Follow symbolic links") # aka shortcuts
    parser.add_argument('-s', '--safe_mode', action='store_true',
                        help="Enable safe mode to restrict symlink following")
    return parser.parse_args()


def main():
    if len(sys.argv) > 1: # checks if user added args
        args = parse_args()
        tree = DirectoryTree(args.root_path, output_file=args.output_file,
                             follow_symlinks=args.follow_symlinks,
                             safe_mode=args.safe_mode)
    else: # hardcode in file directions
        root_path = os.path.dirname(__file__)
        output_file = os.path.join(root_path, 'directory_tree_output.txt')
        ignore_list = ['venv','.git', '.gitignore','.DS_Store','.vscode'] # example

        tree = DirectoryTree(root_path, output_file=output_file,
                             follow_symlinks=False, safe_mode=True,
                             ignore_list=ignore_list)
        
    tree.generate_tree()


if __name__ == "__main__":
    main()