from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP


SERVER_NAME = "LocalUtilsServer"
SERVER_VERSION = "0.1.0"
BASE_DIR = Path.cwd()


mcp = FastMCP(SERVER_NAME)


def _resolve_safe_path(relative_path: str) -> Path:
    """
    Resolve a user-provided path safely within BASE_DIR to prevent path traversal.
    """
    target = (BASE_DIR / relative_path).resolve()
    base_resolved = BASE_DIR.resolve()
    if base_resolved not in target.parents and target != base_resolved:
        raise ValueError(f"Path '{relative_path}' escapes the allowed base directory.")
    return target


@mcp.tool()
def get_info() -> Dict[str, Any]:
    """
    Return basic information about this MCP server and environment.
    """
    return {
        "server_name": SERVER_NAME,
        "version": SERVER_VERSION,
        "cwd": str(BASE_DIR),
        "python_version": sys.version,
        "platform": platform.platform(),
    }


@mcp.tool()
def list_directory(path: str = ".", max_entries: int = 100) -> List[Dict[str, Any]]:
    """
    List files and directories under the given path relative to the base directory.

    Parameters
    ----------
    path:
        Relative path inside the allowed base directory. Defaults to the base directory itself.
    max_entries:
        Maximum number of entries to return.
    """
    if max_entries <= 0:
        raise ValueError("max_entries must be a positive integer.")

    target = _resolve_safe_path(path)
    if not target.exists():
        raise FileNotFoundError(f"Path '{path}' does not exist.")
    if not target.is_dir():
        raise NotADirectoryError(f"Path '{path}' is not a directory.")

    entries: List[Dict[str, Any]] = []
    with os.scandir(target) as it:
        for entry in it:
            entries.append(
                {
                    "name": entry.name,
                    "is_dir": entry.is_dir(),
                    "is_file": entry.is_file(),
                    "size": entry.stat().st_size if entry.is_file() else None,
                }
            )
            if len(entries) >= max_entries:
                break
    return entries


@mcp.tool()
def read_text_file(path: str, max_bytes: int = 8192) -> str:
    """
    Read a text file from within the base directory, with a size limit.

    Parameters
    ----------
    path:
        Relative path to the file inside the allowed base directory.
    max_bytes:
        Maximum number of bytes to read from the file.
    """
    if max_bytes <= 0:
        raise ValueError("max_bytes must be a positive integer.")

    target = _resolve_safe_path(path)
    if not target.exists():
        raise FileNotFoundError(f"File '{path}' does not exist.")
    if not target.is_file():
        raise IsADirectoryError(f"Path '{path}' is not a file.")

    data = target.read_bytes()
    truncated = False
    if len(data) > max_bytes:
        data = data[:max_bytes]
        truncated = True

    text = data.decode("utf-8", errors="replace")
    if truncated:
        text += "\n...[truncated]"
    return text


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.
    """
    return a + b


if __name__ == "__main__":
    mcp.run()