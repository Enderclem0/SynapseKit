import os
import pytest
import tempfile
import shutil
from synapsekit.base_tools.file_system import (
    file_read,
    file_write,
    directory_list,
    file_delete,
    file_move
)


class TestFileSystem:
    """Tests for the file_system module."""

    def setup_method(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_file.txt")
        self.test_content = "This is test content."
        self.nested_dir = os.path.join(self.temp_dir, "nested")
        self.nested_file = os.path.join(self.nested_dir, "nested_file.txt")

    def teardown_method(self):
        """Clean up temporary directory after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_file_write_and_read(self):
        """Test writing to and reading from a file."""
        # Test writing
        file_write(self.test_file, self.test_content)
        assert os.path.exists(self.test_file)

        # Test reading
        content = file_read(self.test_file)
        assert content == self.test_content

    def test_file_write_creates_directories(self):
        """Test that file_write creates directories if they don't exist."""
        file_write(self.nested_file, self.test_content)
        assert os.path.exists(self.nested_dir)
        assert os.path.exists(self.nested_file)

    def test_file_read_nonexistent(self):
        """Test reading a nonexistent file raises FileNotFoundError."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            file_read(nonexistent_file)

    def test_directory_list(self):
        """Test listing directory contents."""
        # Create some files and directories
        file_write(self.test_file, self.test_content)
        os.makedirs(self.nested_dir)
        file_write(self.nested_file, self.test_content)

        # Test listing the temp directory
        contents = directory_list(self.temp_dir)
        assert "test_file.txt" in contents
        assert "nested" in contents
        assert len(contents) == 2

    def test_directory_list_nonexistent(self):
        """Test listing a nonexistent directory raises FileNotFoundError."""
        nonexistent_dir = os.path.join(self.temp_dir, "nonexistent")
        with pytest.raises(FileNotFoundError):
            directory_list(nonexistent_dir)

    def test_directory_list_not_a_directory(self):
        """Test listing a file as a directory raises NotADirectoryError."""
        file_write(self.test_file, self.test_content)
        with pytest.raises(NotADirectoryError):
            directory_list(self.test_file)

    def test_file_delete(self):
        """Test deleting a file."""
        # Create a file
        file_write(self.test_file, self.test_content)
        assert os.path.exists(self.test_file)

        # Delete the file
        file_delete(self.test_file)
        assert not os.path.exists(self.test_file)

    def test_file_delete_nonexistent(self):
        """Test deleting a nonexistent file raises FileNotFoundError."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        with pytest.raises(FileNotFoundError):
            file_delete(nonexistent_file)

    def test_file_delete_directory(self):
        """Test deleting a directory as a file raises IsADirectoryError."""
        os.makedirs(self.nested_dir)
        with pytest.raises(IsADirectoryError):
            file_delete(self.nested_dir)

    def test_file_move(self):
        """Test moving a file."""
        # Create a file
        file_write(self.test_file, self.test_content)
        assert os.path.exists(self.test_file)

        # Move the file
        destination = os.path.join(self.temp_dir, "moved_file.txt")
        file_move(self.test_file, destination)
        assert not os.path.exists(self.test_file)
        assert os.path.exists(destination)

        # Check content is preserved
        content = file_read(destination)
        assert content == self.test_content

    def test_file_move_to_nested_directory(self):
        """Test moving a file to a nested directory that doesn't exist yet."""
        # Create a file
        file_write(self.test_file, self.test_content)
        
        # Move to a nested directory that doesn't exist yet
        nested_dest_dir = os.path.join(self.temp_dir, "new_nested", "deeper")
        destination = os.path.join(nested_dest_dir, "moved_file.txt")
        
        file_move(self.test_file, destination)
        assert not os.path.exists(self.test_file)
        assert os.path.exists(destination)

    def test_file_move_nonexistent(self):
        """Test moving a nonexistent file raises FileNotFoundError."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        destination = os.path.join(self.temp_dir, "moved_file.txt")
        with pytest.raises(FileNotFoundError):
            file_move(nonexistent_file, destination)

    def test_file_move_directory(self):
        """Test moving a directory as a file raises IsADirectoryError."""
        os.makedirs(self.nested_dir)
        destination = os.path.join(self.temp_dir, "moved_dir")
        with pytest.raises(IsADirectoryError):
            file_move(self.nested_dir, destination)