import argparse
import logging
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from directory_tree import DirectoryTree, parse_args

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class TestDirectoryTree(unittest.TestCase):
    """
    Test suite for DirectoryTree class.
    """
    def setUp(self):
        """
        Set up test environment for each test method.
        Initializes DirectoryTree instance with fake directory and output file.
        """
        self.logger = logging.getLogger(__name__)
        self.root_path = "fake_directory"
        self.output_file = "fake_output.txt"
        self.tree = DirectoryTree(self.root_path, self.output_file)
        self.logger.debug("Test setup complete with root_path: %s and output_file: %s",
                          self.root_path, self.output_file)

    @patch('os.path.abspath')
    @patch('os.path.realpath')
    def test_init(self, mock_realpath, mock_abspath):
        """
        Test initialization of DirectoryTree class.
        Ensures root_path and safe_root are set using mocked paths.
        """
        mock_abspath.return_value = "/absolute/fake_directory"
        mock_realpath.return_value = "/real/fake_directory"
        tree = DirectoryTree("fake_directory")
        self.assertEqual(tree.root_path, "/absolute/fake_directory")
        self.assertEqual(tree.safe_root, "/real/fake_directory")

    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=MagicMock)
    def test_generate_tree_stdout(self, mock_stdout, mock_file):
        """
        Test generate_tree method when outputting to stdout.
        Verifies stdout reconfiguration for UTF-8 encoding.
        """
        mock_stdout.reconfigure = MagicMock()  # Mock reconfigure method
        self.tree.output_file = None
        self.tree.generate_tree()
        mock_stdout.reconfigure.assert_called_once_with(encoding='utf-8')

    @patch('argparse.ArgumentParser.parse_args')
    def test_command_line_parsing(self, mock_parse_args):
        """
        Test parsing of command-line arguments.
        Verifies correct parsing and setting of command-line options.
        """
        mock_parse_args.return_value = argparse.Namespace(
            root_path='path/to/root', output_file='out.txt', follow_symlinks=True,
            safe_mode=False)
        parsed_args = parse_args()
        self.assertEqual(parsed_args.root_path, 'path/to/root')
        self.assertEqual(parsed_args.output_file, 'out.txt')
        self.assertTrue(parsed_args.follow_symlinks)
        self.assertFalse(parsed_args.safe_mode)

    
    @patch('os.walk')
    def test_walk_directory(self, mock_walk):
        """
        Test walk_directory method.
        Verifies correct processing of directories and files.
        """
        mock_walk.return_value = [
            ("fake_directory", ["subdir"], ["file1.txt"]),
            ("fake_directory/subdir", [], ["file2.txt"])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("fake_directory/\n"),
            call("|   file1.txt\n"),
            call("|\n"),
            call("subdir/\n"),
            call("|   file2.txt\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)

    @patch('os.path.join')
    def test_process_files(self, mock_join):
        """
        Test process_files method.
        Verifies correct output of files.
        """
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        output = MagicMock()
        files = ["file1.txt", "file2.txt"]
        self.tree.process_files(files, 1, output)
        expected_calls = [
            call("|   |   file1.txt\n"),
            call("|   |   file2.txt\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)
        
        
    @patch('os.walk')
    def test_directory_indentation_and_branching(self, mock_walk):
        """
        Test directory indentation and branching symbols.
        Verifies correct indentation and branching symbols in directory output.
        """
        mock_walk.return_value = [
            ("root", ["dir1", "dir2"], []),
            ("root/dir1", [], ["file1.txt"]),
            ("root/dir2", [], [])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("root/\n"),
            call("|\n"),
            call("dir1/\n"),
            call("|   file1.txt\n"),
            call("dir2/\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)

    @patch('os.walk')
    def test_empty_directory_handling(self, mock_walk):
        """
        Test empty directory handling.
        """
        mock_walk.return_value = [
            ("root", ["empty_dir"], []),
            ("root/empty_dir", [], [])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("root/\n"),
            call("|\n"),
            call("empty_dir/\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)

    @patch('os.walk')
    def test_ignore_list_functionality(self, mock_walk):
        """
        Test ignore list functionality.
        Verifies directories in ignore_list are not processed.
        """
        self.tree.ignore_list = ["dir2"]
        mock_walk.return_value = [
            ("root", ["dir1", "dir2"], []),
            ("root/dir1", [], ["file1.txt"]),
            ("root/dir2", [], ["file2.txt"])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("root/\n"),
            call("|\n"),
            call("dir1/\n"),
            call("|   file1.txt\n"),
            call("dir2/\n"),
            call("|   ...\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)
        
    @patch('os.walk')
    def test_single_file_directory(self, mock_walk):
        """
        Test handling of directory with only a single file.
        """
        mock_walk.return_value = [
            ("single_file_dir", [], ["onlyfile.txt"])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("single_file_dir/\n"),
            call("|   onlyfile.txt\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)

    @patch('os.walk')
    def test_nested_empty_directories(self, mock_walk):
        """
        Test handling of nested directories that are all empty.
        """
        mock_walk.return_value = [
            ("root", ["empty1"], []),
            ("root/empty1", ["empty2"], []),
            ("root/empty1/empty2", [], [])
        ]
        output = MagicMock()
        self.tree.walk_directory(output)
        expected_calls = [
            call("root/\n"),
            call("|\n"),
            call("empty1/\n"),
            call("|\n"),
            call("empty2/\n")
        ]
        output.write.assert_has_calls(expected_calls, any_order=False)


if __name__ == '__main__':
    unittest.main()