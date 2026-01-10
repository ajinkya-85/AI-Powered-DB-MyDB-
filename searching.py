"""Utility to search for database files in the project directory.

Provides a `find_databases(path='.')` function that returns a list of filenames
matching common database extensions. Also includes a simple CLI when run as
__main__.
"""
import os
import platform
import string
from pathlib import Path
from typing import List, Optional

COMMON_DB_EXTENSIONS = {'.db', '.sqlite', '.sqlite3', '.db3'}
IGNORED_DIRS = {
    'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData', 'AppData', 'Windows.old',
    'System Volume Information', '$Recycle.Bin', 'Boot', 'Recovery',
    'proc', 'sys', 'dev', 'run', 'var', 'tmp', 'usr', 'bin', 'lib', 'sbin', 'etc', 'Library','DRIVER'
}


def get_drives() -> List[str]:
    drives = []
    if platform.system() == "Windows":
        try:
            import ctypes
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(f"{letter}:\\")
                bitmask >>= 1
        except Exception:
            drives = ['C:\\']
    else:
        drives = ["/"]
    return drives

def find_databases(path: Optional[str] = None) -> List[Path]:
    """Search for database files recursively.
    
    Args:
        path: directory path to scan. If None, scans all available drives.
    """
    paths_to_scan = [path] if path else get_drives()
    results: List[Path] = []
    
    ignored_lower = {d.lower() for d in IGNORED_DIRS}
    
    for search_path in paths_to_scan:
        if not os.path.exists(search_path):
            continue
            
        for root, dirs, files in os.walk(search_path):
            # Skip ignored and hidden directories
            dirs[:] = [d for d in dirs if d.lower() not in ignored_lower and not d.startswith('.')]
            for file in files:
                if Path(file).suffix.lower() in COMMON_DB_EXTENSIONS:
                    try:
                        results.append(Path(root) / file)
                    except Exception:
                        continue
    return results


def _format_paths(paths: List[Path]) -> List[str]:
    return [str(p.resolve()) for p in paths]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Search for database files in a directory')
    parser.add_argument('-p', '--path', default='.', help='Directory to scan (default: current dir)')
    parser.add_argument('-r', '--recursive', action='store_true', help='Search recursively')
    args = parser.parse_args()

    try:
        found = find_databases(args.path if args.path != '.' else None)
    except Exception as e:
        print(f'Error: {e}')
        raise SystemExit(1)

    if not found:
        print('No database files found.')
    else:
        print('Found database files:')
        for p in _format_paths(found):
            print(' -', p)
