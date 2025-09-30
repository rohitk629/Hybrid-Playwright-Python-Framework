"""
File Utility Module
Provides comprehensive file operations for the automation framework
"""

import os
import shutil
import json
import yaml
import pickle
import zipfile
import tarfile
import hashlib
import mimetypes
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import logging
import filecmp
import tempfile
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileUtility:
    """
    Utility class for file and directory operations
    Provides methods for file manipulation, reading, writing, and management
    """

    def __init__(self):
        """Initialize File Utility"""
        logger.info("FileUtility initialized")

    # ==================== File Existence and Validation ====================

    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists

        Args:
            file_path: Path to the file

        Returns:
            True if file exists, False otherwise
        """
        exists = Path(file_path).is_file()
        logger.info(f"File exists check for {file_path}: {exists}")
        return exists

    def directory_exists(self, dir_path: str) -> bool:
        """
        Check if directory exists

        Args:
            dir_path: Path to the directory

        Returns:
            True if directory exists, False otherwise
        """
        exists = Path(dir_path).is_dir()
        logger.info(f"Directory exists check for {dir_path}: {exists}")
        return exists

    def path_exists(self, path: str) -> bool:
        """
        Check if path exists (file or directory)

        Args:
            path: Path to check

        Returns:
            True if path exists, False otherwise
        """
        exists = Path(path).exists()
        logger.info(f"Path exists check for {path}: {exists}")
        return exists

    def is_file_empty(self, file_path: str) -> bool:
        """
        Check if file is empty

        Args:
            file_path: Path to the file

        Returns:
            True if file is empty, False otherwise
        """
        try:
            if not self.file_exists(file_path):
                logger.warning(f"File does not exist: {file_path}")
                return True

            is_empty = os.path.getsize(file_path) == 0
            logger.info(f"File empty check for {file_path}: {is_empty}")
            return is_empty

        except Exception as e:
            logger.error(f"Error checking if file is empty: {str(e)}")
            raise

    # ==================== File Reading Operations ====================

    def read_file(self, file_path: str, encoding: str = 'utf-8') -> str:
        """
        Read entire file content as string

        Args:
            file_path: Path to the file
            encoding: File encoding (default: utf-8)

        Returns:
            File content as string
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()

            logger.info(f"Successfully read file: {file_path}")
            return content

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise

    def read_file_lines(self, file_path: str, encoding: str = 'utf-8') -> List[str]:
        """
        Read file content as list of lines

        Args:
            file_path: Path to the file
            encoding: File encoding

        Returns:
            List of lines from the file
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()

            logger.info(f"Successfully read {len(lines)} lines from: {file_path}")
            return lines

        except Exception as e:
            logger.error(f"Error reading file lines {file_path}: {str(e)}")
            raise

    def read_binary_file(self, file_path: str) -> bytes:
        """
        Read file in binary mode

        Args:
            file_path: Path to the file

        Returns:
            File content as bytes
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'rb') as file:
                content = file.read()

            logger.info(f"Successfully read binary file: {file_path}")
            return content

        except Exception as e:
            logger.error(f"Error reading binary file {file_path}: {str(e)}")
            raise

    def read_json_file(self, file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        Read and parse JSON file

        Args:
            file_path: Path to the JSON file
            encoding: File encoding

        Returns:
            Parsed JSON as dictionary
        """
        try:
            content = self.read_file(file_path, encoding)
            data = json.loads(content)

            logger.info(f"Successfully read JSON file: {file_path}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise

    def read_yaml_file(self, file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        Read and parse YAML file

        Args:
            file_path: Path to the YAML file
            encoding: File encoding

        Returns:
            Parsed YAML as dictionary
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                data = yaml.safe_load(file)

            logger.info(f"Successfully read YAML file: {file_path}")
            return data

        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in file {file_path}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading YAML file {file_path}: {str(e)}")
            raise

    # ==================== File Writing Operations ====================

    def write_file(self, file_path: str, content: str, encoding: str = 'utf-8',
                   mode: str = 'w') -> bool:
        """
        Write content to file

        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding
            mode: Write mode ('w' for overwrite, 'a' for append)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, mode, encoding=encoding) as file:
                file.write(content)

            logger.info(f"Successfully wrote to file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing to file {file_path}: {str(e)}")
            return False

    def write_lines(self, file_path: str, lines: List[str],
                    encoding: str = 'utf-8', mode: str = 'w') -> bool:
        """
        Write list of lines to file

        Args:
            file_path: Path to the file
            lines: List of lines to write
            encoding: File encoding
            mode: Write mode

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, mode, encoding=encoding) as file:
                file.writelines(lines)

            logger.info(f"Successfully wrote {len(lines)} lines to: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing lines to file {file_path}: {str(e)}")
            return False

    def write_binary_file(self, file_path: str, content: bytes) -> bool:
        """
        Write binary content to file

        Args:
            file_path: Path to the file
            content: Binary content to write

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'wb') as file:
                file.write(content)

            logger.info(f"Successfully wrote binary file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing binary file {file_path}: {str(e)}")
            return False

    def write_json_file(self, file_path: str, data: Dict[str, Any],
                        indent: int = 4, encoding: str = 'utf-8') -> bool:
        """
        Write data to JSON file

        Args:
            file_path: Path to the JSON file
            data: Data to write
            indent: JSON indentation
            encoding: File encoding

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding=encoding) as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)

            logger.info(f"Successfully wrote JSON file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {str(e)}")
            return False

    def write_yaml_file(self, file_path: str, data: Dict[str, Any],
                        encoding: str = 'utf-8') -> bool:
        """
        Write data to YAML file

        Args:
            file_path: Path to the YAML file
            data: Data to write
            encoding: File encoding

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding=encoding) as file:
                yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)

            logger.info(f"Successfully wrote YAML file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error writing YAML file {file_path}: {str(e)}")
            return False

    def append_to_file(self, file_path: str, content: str,
                       encoding: str = 'utf-8') -> bool:
        """
        Append content to file

        Args:
            file_path: Path to the file
            content: Content to append
            encoding: File encoding

        Returns:
            True if successful, False otherwise
        """
        return self.write_file(file_path, content, encoding, mode='a')

    # ==================== File Operations ====================

    def copy_file(self, source: str, destination: str, overwrite: bool = True) -> bool:
        """
        Copy file from source to destination

        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite if destination exists

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(source):
                raise FileNotFoundError(f"Source file not found: {source}")

            if self.file_exists(destination) and not overwrite:
                logger.warning(f"Destination file exists and overwrite is False: {destination}")
                return False

            # Create destination directory if it doesn't exist
            Path(destination).parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(source, destination)
            logger.info(f"Successfully copied file from {source} to {destination}")
            return True

        except Exception as e:
            logger.error(f"Error copying file: {str(e)}")
            return False

    def move_file(self, source: str, destination: str, overwrite: bool = True) -> bool:
        """
        Move file from source to destination

        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite if destination exists

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(source):
                raise FileNotFoundError(f"Source file not found: {source}")

            if self.file_exists(destination) and not overwrite:
                logger.warning(f"Destination file exists and overwrite is False: {destination}")
                return False

            # Create destination directory if it doesn't exist
            Path(destination).parent.mkdir(parents=True, exist_ok=True)

            shutil.move(source, destination)
            logger.info(f"Successfully moved file from {source} to {destination}")
            return True

        except Exception as e:
            logger.error(f"Error moving file: {str(e)}")
            return False

    def delete_file(self, file_path: str) -> bool:
        """
        Delete file

        Args:
            file_path: Path to the file

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(file_path):
                logger.warning(f"File does not exist: {file_path}")
                return False

            os.remove(file_path)
            logger.info(f"Successfully deleted file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
            return False

    def rename_file(self, old_path: str, new_path: str) -> bool:
        """
        Rename file

        Args:
            old_path: Current file path
            new_path: New file path

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(old_path):
                raise FileNotFoundError(f"File not found: {old_path}")

            os.rename(old_path, new_path)
            logger.info(f"Successfully renamed file from {old_path} to {new_path}")
            return True

        except Exception as e:
            logger.error(f"Error renaming file: {str(e)}")
            return False

    # ==================== Directory Operations ====================

    def create_directory(self, dir_path: str, exist_ok: bool = True) -> bool:
        """
        Create directory

        Args:
            dir_path: Path to the directory
            exist_ok: Don't raise error if directory exists

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=exist_ok)
            logger.info(f"Successfully created directory: {dir_path}")
            return True

        except Exception as e:
            logger.error(f"Error creating directory {dir_path}: {str(e)}")
            return False

    def delete_directory(self, dir_path: str, recursive: bool = False) -> bool:
        """
        Delete directory

        Args:
            dir_path: Path to the directory
            recursive: Delete directory and all contents

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return False

            if recursive:
                shutil.rmtree(dir_path)
            else:
                os.rmdir(dir_path)

            logger.info(f"Successfully deleted directory: {dir_path}")
            return True

        except Exception as e:
            logger.error(f"Error deleting directory {dir_path}: {str(e)}")
            return False

    def copy_directory(self, source: str, destination: str) -> bool:
        """
        Copy directory and all contents

        Args:
            source: Source directory path
            destination: Destination directory path

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.directory_exists(source):
                raise FileNotFoundError(f"Source directory not found: {source}")

            shutil.copytree(source, destination, dirs_exist_ok=True)
            logger.info(f"Successfully copied directory from {source} to {destination}")
            return True

        except Exception as e:
            logger.error(f"Error copying directory: {str(e)}")
            return False

    def list_files(self, dir_path: str, extension: str = None,
                   recursive: bool = False) -> List[str]:
        """
        List all files in directory

        Args:
            dir_path: Path to the directory
            extension: Filter by file extension (e.g., '.txt')
            recursive: Include subdirectories

        Returns:
            List of file paths
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return []

            files = []
            path = Path(dir_path)

            if recursive:
                pattern = f"**/*{extension if extension else ''}"
                files = [str(f) for f in path.glob(pattern) if f.is_file()]
            else:
                pattern = f"*{extension if extension else ''}"
                files = [str(f) for f in path.glob(pattern) if f.is_file()]

            logger.info(f"Found {len(files)} files in {dir_path}")
            return files

        except Exception as e:
            logger.error(f"Error listing files in {dir_path}: {str(e)}")
            return []

    def list_directories(self, dir_path: str, recursive: bool = False) -> List[str]:
        """
        List all subdirectories

        Args:
            dir_path: Path to the directory
            recursive: Include nested subdirectories

        Returns:
            List of directory paths
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return []

            path = Path(dir_path)

            if recursive:
                directories = [str(d) for d in path.rglob('*') if d.is_dir()]
            else:
                directories = [str(d) for d in path.iterdir() if d.is_dir()]

            logger.info(f"Found {len(directories)} directories in {dir_path}")
            return directories

        except Exception as e:
            logger.error(f"Error listing directories in {dir_path}: {str(e)}")
            return []

    def get_directory_size(self, dir_path: str) -> int:
        """
        Get total size of directory in bytes

        Args:
            dir_path: Path to the directory

        Returns:
            Size in bytes
        """
        try:
            total_size = 0

            for dirpath, dirnames, filenames in os.walk(dir_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)

            logger.info(f"Directory size for {dir_path}: {total_size} bytes")
            return total_size

        except Exception as e:
            logger.error(f"Error calculating directory size: {str(e)}")
            return 0

    # ==================== File Information ====================

    def get_file_size(self, file_path: str) -> int:
        """
        Get file size in bytes

        Args:
            file_path: Path to the file

        Returns:
            File size in bytes
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            size = os.path.getsize(file_path)
            logger.info(f"File size for {file_path}: {size} bytes")
            return size

        except Exception as e:
            logger.error(f"Error getting file size: {str(e)}")
            return 0

    def get_file_extension(self, file_path: str) -> str:
        """
        Get file extension

        Args:
            file_path: Path to the file

        Returns:
            File extension including dot (e.g., '.txt')
        """
        extension = Path(file_path).suffix
        logger.info(f"File extension for {file_path}: {extension}")
        return extension

    def get_file_name(self, file_path: str, with_extension: bool = True) -> str:
        """
        Get file name from path

        Args:
            file_path: Path to the file
            with_extension: Include extension in name

        Returns:
            File name
        """
        path = Path(file_path)

        if with_extension:
            name = path.name
        else:
            name = path.stem

        logger.info(f"File name for {file_path}: {name}")
        return name

    def get_file_creation_time(self, file_path: str) -> datetime:
        """
        Get file creation time

        Args:
            file_path: Path to the file

        Returns:
            Creation time as datetime object
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            timestamp = os.path.getctime(file_path)
            creation_time = datetime.fromtimestamp(timestamp)

            logger.info(f"File creation time for {file_path}: {creation_time}")
            return creation_time

        except Exception as e:
            logger.error(f"Error getting file creation time: {str(e)}")
            raise

    def get_file_modification_time(self, file_path: str) -> datetime:
        """
        Get file modification time

        Args:
            file_path: Path to the file

        Returns:
            Modification time as datetime object
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            timestamp = os.path.getmtime(file_path)
            modification_time = datetime.fromtimestamp(timestamp)

            logger.info(f"File modification time for {file_path}: {modification_time}")
            return modification_time

        except Exception as e:
            logger.error(f"Error getting file modification time: {str(e)}")
            raise

    def get_mime_type(self, file_path: str) -> Optional[str]:
        """
        Get MIME type of file

        Args:
            file_path: Path to the file

        Returns:
            MIME type string or None
        """
        mime_type, _ = mimetypes.guess_type(file_path)
        logger.info(f"MIME type for {file_path}: {mime_type}")
        return mime_type

    # ==================== File Comparison ====================

    def compare_files(self, file1: str, file2: str) -> bool:
        """
        Compare two files for equality

        Args:
            file1: Path to first file
            file2: Path to second file

        Returns:
            True if files are identical, False otherwise
        """
        try:
            if not self.file_exists(file1) or not self.file_exists(file2):
                logger.warning("One or both files do not exist")
                return False

            are_equal = filecmp.cmp(file1, file2, shallow=False)
            logger.info(f"Files comparison result: {are_equal}")
            return are_equal

        except Exception as e:
            logger.error(f"Error comparing files: {str(e)}")
            return False

    def get_file_hash(self, file_path: str, algorithm: str = 'md5') -> str:
        """
        Calculate file hash

        Args:
            file_path: Path to the file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')

        Returns:
            Hash string
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            hash_obj = hashlib.new(algorithm)

            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    hash_obj.update(chunk)

            file_hash = hash_obj.hexdigest()
            logger.info(f"File hash ({algorithm}) for {file_path}: {file_hash}")
            return file_hash

        except Exception as e:
            logger.error(f"Error calculating file hash: {str(e)}")
            raise

    # ==================== Archive Operations ====================

    def create_zip(self, source_dir: str, output_file: str) -> bool:
        """
        Create ZIP archive from directory

        Args:
            source_dir: Directory to compress
            output_file: Output ZIP file path

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.directory_exists(source_dir):
                raise FileNotFoundError(f"Source directory not found: {source_dir}")

            Path(output_file).parent.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)

            logger.info(f"Successfully created ZIP archive: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error creating ZIP archive: {str(e)}")
            return False

    def extract_zip(self, zip_file: str, extract_to: str) -> bool:
        """
        Extract ZIP archive

        Args:
            zip_file: Path to ZIP file
            extract_to: Extraction destination

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(zip_file):
                raise FileNotFoundError(f"ZIP file not found: {zip_file}")

            Path(extract_to).mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(zip_file, 'r') as zipf:
                zipf.extractall(extract_to)

            logger.info(f"Successfully extracted ZIP archive to: {extract_to}")
            return True

        except Exception as e:
            logger.error(f"Error extracting ZIP archive: {str(e)}")
            return False

    # ==================== Search Operations ====================

    def search_files(self, dir_path: str, pattern: str, recursive: bool = True) -> List[str]:
        """
        Search for files matching pattern

        Args:
            dir_path: Directory to search
            pattern: Search pattern (supports wildcards)
            recursive: Search in subdirectories

        Returns:
            List of matching file paths
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return []

            if recursive:
                search_pattern = os.path.join(dir_path, '**', pattern)
                files = glob.glob(search_pattern, recursive=True)
            else:
                search_pattern = os.path.join(dir_path, pattern)
                files = glob.glob(search_pattern)

            logger.info(f"Found {len(files)} files matching pattern: {pattern}")
            return files

        except Exception as e:
            logger.error(f"Error searching files: {str(e)}")
            return []

    def search_in_files(self, dir_path: str, search_text: str,
                        extension: str = None, recursive: bool = True) -> Dict[str, List[int]]:
        """
        Search for text in files

        Args:
            dir_path: Directory to search
            search_text: Text to search for
            extension: File extension filter
            recursive: Search in subdirectories

        Returns:
            Dictionary mapping file paths to line numbers containing text
        """
        try:
            results = {}
            files = self.list_files(dir_path, extension, recursive)

            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        line_numbers = []
                        for line_num, line in enumerate(file, 1):
                            if search_text in line:
                                line_numbers.append(line_num)

                        if line_numbers:
                            results[file_path] = line_numbers

                except Exception:
                    continue

            logger.info(f"Found text in {len(results)} files")
            return results

        except Exception as e:
            logger.error(f"Error searching in files: {str(e)}")
            return {}

    # ==================== Temporary File Operations ====================

    def create_temp_file(self, suffix: str = '', prefix: str = 'tmp',
                         dir: str = None, text: bool = True) -> str:
        """
        Create temporary file

        Args:
            suffix: File suffix
            prefix: File prefix
            dir: Directory for temp file
            text: Text mode or binary mode

        Returns:
            Path to temporary file
        """
        try:
            mode = 'w+' if text else 'w+b'
            temp_file = tempfile.NamedTemporaryFile(
                mode=mode, suffix=suffix, prefix=prefix,
                dir=dir, delete=False
            )
            temp_path = temp_file.name
            temp_file.close()

            logger.info(f"Created temporary file: {temp_path}")
            return temp_path

        except Exception as e:
            logger.error(f"Error creating temporary file: {str(e)}")
            raise

    def create_temp_directory(self, suffix: str = '', prefix: str = 'tmp',
                              dir: str = None) -> str:
        """
        Create temporary directory

        Args:
            suffix: Directory suffix
            prefix: Directory prefix
            dir: Parent directory

        Returns:
            Path to temporary directory
        """
        try:
            temp_dir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
            logger.info(f"Created temporary directory: {temp_dir}")
            return temp_dir

        except Exception as e:
            logger.error(f"Error creating temporary directory: {str(e)}")
            raise

    def get_file_permissions(self, file_path: str) -> str:
        """
        Get file permissions in octal format

        Args:
            file_path: Path to the file

        Returns:
            Permission string (e.g., '755')
        """
        try:
            if not self.path_exists(file_path):
                raise FileNotFoundError(f"Path not found: {file_path}")

            permissions = oct(os.stat(file_path).st_mode)[-3:]
            logger.info(f"File permissions for {file_path}: {permissions}")
            return permissions

        except Exception as e:
            logger.error(f"Error getting file permissions: {str(e)}")
            raise

    def set_file_permissions(self, file_path: str, permissions: int) -> bool:
        """
        Set file permissions

        Args:
            file_path: Path to the file
            permissions: Permission in octal (e.g., 0o755)

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.path_exists(file_path):
                raise FileNotFoundError(f"Path not found: {file_path}")

            os.chmod(file_path, permissions)
            logger.info(f"Set permissions for {file_path}: {oct(permissions)}")
            return True

        except Exception as e:
            logger.error(f"Error setting file permissions: {str(e)}")
            return False

    def is_readable(self, file_path: str) -> bool:
        """
        Check if file is readable

        Args:
            file_path: Path to the file

        Returns:
            True if readable, False otherwise
        """
        readable = os.access(file_path, os.R_OK)
        logger.info(f"File readable check for {file_path}: {readable}")
        return readable

    def is_writable(self, file_path: str) -> bool:
        """
        Check if file is writable

        Args:
            file_path: Path to the file

        Returns:
            True if writable, False otherwise
        """
        writable = os.access(file_path, os.W_OK)
        logger.info(f"File writable check for {file_path}: {writable}")
        return writable

    def is_executable(self, file_path: str) -> bool:
        """
        Check if file is executable

        Args:
            file_path: Path to the file

        Returns:
            True if executable, False otherwise
        """
        executable = os.access(file_path, os.X_OK)
        logger.info(f"File executable check for {file_path}: {executable}")
        return executable

    # ==================== Path Operations ====================

    def get_absolute_path(self, file_path: str) -> str:
        """
        Get absolute path of file

        Args:
            file_path: File path (relative or absolute)

        Returns:
            Absolute path
        """
        absolute_path = str(Path(file_path).resolve())
        logger.info(f"Absolute path for {file_path}: {absolute_path}")
        return absolute_path

    def get_relative_path(self, file_path: str, start: str = None) -> str:
        """
        Get relative path

        Args:
            file_path: Target file path
            start: Starting directory (default: current directory)

        Returns:
            Relative path
        """
        if start is None:
            start = os.getcwd()

        relative_path = os.path.relpath(file_path, start)
        logger.info(f"Relative path from {start} to {file_path}: {relative_path}")
        return relative_path

    def get_parent_directory(self, file_path: str) -> str:
        """
        Get parent directory of file

        Args:
            file_path: Path to the file

        Returns:
            Parent directory path
        """
        parent = str(Path(file_path).parent)
        logger.info(f"Parent directory for {file_path}: {parent}")
        return parent

    def join_paths(self, *paths: str) -> str:
        """
        Join multiple path components

        Args:
            *paths: Path components to join

        Returns:
            Joined path
        """
        joined_path = str(Path(*paths))
        logger.info(f"Joined path: {joined_path}")
        return joined_path

    def normalize_path(self, file_path: str) -> str:
        """
        Normalize path (resolve . and ..)

        Args:
            file_path: Path to normalize

        Returns:
            Normalized path
        """
        normalized = os.path.normpath(file_path)
        logger.info(f"Normalized path for {file_path}: {normalized}")
        return normalized

    # ==================== Pickle Operations ====================

    def save_pickle(self, file_path: str, data: Any) -> bool:
        """
        Save data to pickle file

        Args:
            file_path: Path to pickle file
            data: Data to serialize

        Returns:
            True if successful, False otherwise
        """
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'wb') as file:
                pickle.dump(data, file)

            logger.info(f"Successfully saved pickle file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving pickle file {file_path}: {str(e)}")
            return False

    def load_pickle(self, file_path: str) -> Any:
        """
        Load data from pickle file

        Args:
            file_path: Path to pickle file

        Returns:
            Deserialized data
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"Pickle file not found: {file_path}")

            with open(file_path, 'rb') as file:
                data = pickle.load(file)

            logger.info(f"Successfully loaded pickle file: {file_path}")
            return data

        except Exception as e:
            logger.error(f"Error loading pickle file {file_path}: {str(e)}")
            raise

    # ==================== File Cleanup Operations ====================

    def clean_directory(self, dir_path: str, older_than_days: int = None,
                        extension: str = None) -> int:
        """
        Clean files from directory based on criteria

        Args:
            dir_path: Directory to clean
            older_than_days: Delete files older than specified days
            extension: Filter by file extension

        Returns:
            Number of files deleted
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return 0

            files = self.list_files(dir_path, extension, recursive=False)
            deleted_count = 0

            for file_path in files:
                should_delete = True

                if older_than_days is not None:
                    mod_time = self.get_file_modification_time(file_path)
                    age_days = (datetime.now() - mod_time).days
                    should_delete = age_days > older_than_days

                if should_delete:
                    if self.delete_file(file_path):
                        deleted_count += 1

            logger.info(f"Cleaned {deleted_count} files from {dir_path}")
            return deleted_count

        except Exception as e:
            logger.error(f"Error cleaning directory: {str(e)}")
            return 0

    def delete_empty_directories(self, dir_path: str) -> int:
        """
        Delete all empty subdirectories

        Args:
            dir_path: Root directory to search

        Returns:
            Number of directories deleted
        """
        try:
            if not self.directory_exists(dir_path):
                logger.warning(f"Directory does not exist: {dir_path}")
                return 0

            deleted_count = 0

            # Walk bottom-up to delete nested empty directories
            for root, dirs, files in os.walk(dir_path, topdown=False):
                for directory in dirs:
                    dir_to_check = os.path.join(root, directory)
                    try:
                        if not os.listdir(dir_to_check):  # Directory is empty
                            os.rmdir(dir_to_check)
                            deleted_count += 1
                            logger.info(f"Deleted empty directory: {dir_to_check}")
                    except Exception:
                        continue

            logger.info(f"Deleted {deleted_count} empty directories")
            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting empty directories: {str(e)}")
            return 0

    # ==================== File Backup Operations ====================

    def backup_file(self, file_path: str, backup_dir: str = None,
                    timestamp: bool = True) -> Optional[str]:
        """
        Create backup of file

        Args:
            file_path: Path to file to backup
            backup_dir: Backup directory (default: same directory)
            timestamp: Add timestamp to backup filename

        Returns:
            Path to backup file or None if failed
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            file_name = self.get_file_name(file_path, with_extension=False)
            extension = self.get_file_extension(file_path)

            if timestamp:
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{file_name}_backup_{timestamp_str}{extension}"
            else:
                backup_name = f"{file_name}_backup{extension}"

            if backup_dir is None:
                backup_dir = self.get_parent_directory(file_path)

            backup_path = os.path.join(backup_dir, backup_name)

            if self.copy_file(file_path, backup_path):
                logger.info(f"Created backup: {backup_path}")
                return backup_path
            else:
                return None

        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return None

    def restore_backup(self, backup_path: str, original_path: str,
                       overwrite: bool = True) -> bool:
        """
        Restore file from backup

        Args:
            backup_path: Path to backup file
            original_path: Path to restore to
            overwrite: Overwrite if original exists

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")

            if self.file_exists(original_path) and not overwrite:
                logger.warning(f"Original file exists and overwrite is False: {original_path}")
                return False

            success = self.copy_file(backup_path, original_path, overwrite)

            if success:
                logger.info(f"Restored backup from {backup_path} to {original_path}")

            return success

        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            return False

    # ==================== File Encoding Operations ====================

    def detect_encoding(self, file_path: str) -> str:
        """
        Detect file encoding (simple detection)

        Args:
            file_path: Path to the file

        Returns:
            Detected encoding
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'ascii', 'utf-16', 'cp1252']

            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        file.read()
                    logger.info(f"Detected encoding for {file_path}: {encoding}")
                    return encoding
                except (UnicodeDecodeError, UnicodeError):
                    continue

            logger.warning(f"Could not detect encoding for {file_path}, defaulting to utf-8")
            return 'utf-8'

        except Exception as e:
            logger.error(f"Error detecting encoding: {str(e)}")
            return 'utf-8'

    def convert_encoding(self, file_path: str, from_encoding: str,
                         to_encoding: str, output_path: str = None) -> bool:
        """
        Convert file encoding

        Args:
            file_path: Path to input file
            from_encoding: Source encoding
            to_encoding: Target encoding
            output_path: Output file path (default: overwrite original)

        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read with source encoding
            with open(file_path, 'r', encoding=from_encoding) as file:
                content = file.read()

            # Write with target encoding
            output = output_path if output_path else file_path
            with open(output, 'w', encoding=to_encoding) as file:
                file.write(content)

            logger.info(f"Converted encoding from {from_encoding} to {to_encoding}")
            return True

        except Exception as e:
            logger.error(f"Error converting encoding: {str(e)}")
            return False

    # ==================== Utility Methods ====================

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get comprehensive file information

        Args:
            file_path: Path to the file

        Returns:
            Dictionary containing file information
        """
        try:
            if not self.path_exists(file_path):
                raise FileNotFoundError(f"Path not found: {file_path}")

            info = {
                'path': file_path,
                'absolute_path': self.get_absolute_path(file_path),
                'name': self.get_file_name(file_path),
                'extension': self.get_file_extension(file_path),
                'size_bytes': self.get_file_size(file_path) if self.file_exists(file_path) else None,
                'is_file': self.file_exists(file_path),
                'is_directory': self.directory_exists(file_path),
                'created': self.get_file_creation_time(file_path) if self.file_exists(file_path) else None,
                'modified': self.get_file_modification_time(file_path) if self.file_exists(file_path) else None,
                'permissions': self.get_file_permissions(file_path),
                'readable': self.is_readable(file_path),
                'writable': self.is_writable(file_path),
                'executable': self.is_executable(file_path),
                'mime_type': self.get_mime_type(file_path)
            }

            logger.info(f"Retrieved file info for: {file_path}")
            return info

        except Exception as e:
            logger.error(f"Error getting file info: {str(e)}")
            return {}

    def format_file_size(self, size_bytes: int) -> str:
        """
        Format file size in human-readable format

        Args:
            size_bytes: Size in bytes

        Returns:
            Formatted size string (e.g., '1.5 MB')
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    def get_disk_usage(self, path: str = None) -> Dict[str, Any]:
        """
        Get disk usage statistics

        Args:
            path: Path to check (default: current directory)

        Returns:
            Dictionary with total, used, and free space
        """
        try:
            if path is None:
                path = os.getcwd()

            stat = shutil.disk_usage(path)

            usage = {
                'total': stat.total,
                'used': stat.used,
                'free': stat.free,
                'total_formatted': self.format_file_size(stat.total),
                'used_formatted': self.format_file_size(stat.used),
                'free_formatted': self.format_file_size(stat.free),
                'percent_used': (stat.used / stat.total) * 100
            }

            logger.info(f"Disk usage for {path}: {usage['percent_used']:.2f}% used")
            return usage

        except Exception as e:
            logger.error(f"Error getting disk usage: {str(e)}")
            return {}

    def count_lines_in_file(self, file_path: str, encoding: str = 'utf-8') -> int:
        """
        Count number of lines in file

        Args:
            file_path: Path to the file
            encoding: File encoding

        Returns:
            Number of lines
        """
        try:
            if not self.file_exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
                line_count = sum(1 for _ in file)

            logger.info(f"Line count for {file_path}: {line_count}")
            return line_count

        except Exception as e:
            logger.error(f"Error counting lines: {str(e)}")
            return 0

    def get_file_statistics(self, dir_path: str, recursive: bool = True) -> Dict[str, Any]:
        """
        Get statistics for files in directory

        Args:
            dir_path: Directory path
            recursive: Include subdirectories

        Returns:
            Dictionary with file statistics
        """
        try:
            if not self.directory_exists(dir_path):
                raise FileNotFoundError(f"Directory not found: {dir_path}")

            files = self.list_files(dir_path, recursive=recursive)

            if not files:
                return {'total_files': 0}

            total_size = sum(self.get_file_size(f) for f in files)
            extensions = {}

            for file in files:
                ext = self.get_file_extension(file)
                extensions[ext] = extensions.get(ext, 0) + 1

            stats = {
                'total_files': len(files),
                'total_size_bytes': total_size,
                'total_size_formatted': self.format_file_size(total_size),
                'average_size_bytes': total_size / len(files),
                'extensions': extensions,
                'largest_file': max(files, key=lambda f: self.get_file_size(f)),
                'smallest_file': min(files, key=lambda f: self.get_file_size(f))
            }

            logger.info(f"File statistics for {dir_path}: {stats['total_files']} files")
            return stats

        except Exception as e:
            logger.error(f"Error getting file statistics: {str(e)}")
            return {}

