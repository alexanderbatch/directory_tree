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
        Initializes a DirectoryTree instance with a fake directory and output file.
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
        Test the initialization of DirectoryTree class.
        Ensures that root_path and safe_root are correctly set using mocked paths.
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
        Verifies that stdout is correctly reconfigured to handle UTF-8 encoding.
        """
        mock_stdout.reconfigure = MagicMock()  # Mock reconfigure method
        self.tree.output_file = None
        self.tree.generate_tree()
        mock_stdout.reconfigure.assert_called_once_with(encoding='utf-8')

    @patch('argparse.ArgumentParser.parse_args')
    def test_command_line_parsing(self, mock_parse_args):
        """
        Test parsing of command-line arguments.
        Verifies that all command-line options are correctly parsed and set.
        """
        mock_parse_args.return_value = argparse.Namespace(
            root_path='path/to/root', output_file='out.txt', follow_symlinks=True,
            safe_mode=False)
        parsed_args = parse_args()
        self.assertEqual(parsed_args.root_path, 'path/to/root')
        self.assertEqual(parsed_args.output_file, 'out.txt')
        self.assertTrue(parsed_args.follow_symlinks)
        self.assertFalse(parsed_args.safe_mode)


if __name__ == '__main__':
    unittest.main()