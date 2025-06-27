import os
import shutil
from typing import List


def file_read(path: str) -> str:
    """
    Reads the content of a file.

    Args:
        path: The path to the file.

    Returns:
        The content of the file as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: For other I/O errors.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except Exception as e:
        raise IOError(f"Error reading file '{path}': {e}")


def file_write(path: str, content: str) -> None:
    """
    Writes content to a file. Overwrites if the file already exists.

    Args:
        path: The path to the file.
        content: The string content to write.

    Raises:
        IOError: For I/O related errors.
    """
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise IOError(f"Error writing to file '{path}': {e}")


def directory_list(path: str) -> List[str]:
    """
    Lists the contents (files and directories) of a given path.

    Args:
        path: The path to the directory.

    Returns:
        A list of strings, where each string is the name of an item
        within the directory.

    Raises:
        FileNotFoundError: If the directory does not exist.
        NotADirectoryError: If the path is not a directory.
        IOError: For other I/O errors.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Directory not found: {path}")
        if not os.path.isdir(path):
            raise NotADirectoryError(f"Path is not a directory: {path}")
        return os.listdir(path)
    except (FileNotFoundError, NotADirectoryError) as e:
        raise e
    except Exception as e:
        raise IOError(f"Error listing directory '{path}': {e}")


def file_delete(path: str) -> None:
    """
    Deletes a file at the specified path.

    Args:
        path: The path to the file to delete.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If the path is a directory.
        IOError: For other I/O errors.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        if os.path.isdir(path):
            raise IsADirectoryError(f"Path is a directory, not a file: {path}")
        os.remove(path)
    except (FileNotFoundError, IsADirectoryError) as e:
        raise e
    except Exception as e:
        raise IOError(f"Error deleting file '{path}': {e}")


def file_move(source: str, destination: str) -> None:
    """
    Moves a file from source to destination.

    Args:
        source: The path to the source file.
        destination: The path to the destination.

    Raises:
        FileNotFoundError: If the source file does not exist.
        IsADirectoryError: If the source path is a directory.
        IOError: For other I/O errors.
    """
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source file not found: {source}")
        if os.path.isdir(source):
            raise IsADirectoryError(f"Source path is a directory, not a file: {source}")

        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(destination)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)

        shutil.move(source, destination)
    except (FileNotFoundError, IsADirectoryError) as e:
        raise e
    except Exception as e:
        raise IOError(f"Error moving file from '{source}' to '{destination}': {e}")
