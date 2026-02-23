"""
MCP server that exposes appie CLI commands as tools.
Runs appie from the project at APPIE_PROJECT_DIR (default D:\\git\\ah_app).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SERVER_NAME = "AppieServer"
APPIE_PROJECT_DIR = Path(os.environ.get("APPIE_PROJECT_DIR", r"D:\git\ah_app"))

mcp = FastMCP(SERVER_NAME)


def _run_appie(*args: str, timeout: int = 60) -> str:
    """Run appie CLI from the appie project directory. Returns combined stdout + stderr."""
    cmd = ["uv", "run", "appie", *args]
    result = subprocess.run(
        cmd,
        cwd=APPIE_PROJECT_DIR,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()
    combined = "\n".join(filter(None, [out, err]))
    if result.returncode != 0:
        raise RuntimeError(f"appie exited with code {result.returncode}\n{combined}")
    return combined or "(no output)"


@mcp.tool()
def receipt_list(n: int = 5) -> str:
    """
    List the last n receipts from appie (same as: appie receipt -n N).

    Parameters
    ----------
    n : int, default 5
        Number of receipts to list.
    """
    if n < 1:
        raise ValueError("n must be at least 1.")
    return _run_appie("receipt", "-n", str(n))


@mcp.tool()
def receipt_show(receipt_id: str) -> str:
    """
    Show details for a single receipt by ID (same as: appie receipt show <id>).

    Parameters
    ----------
    receipt_id : str
        The receipt ID, e.g. AH257944ac39cc4b3bacc6de52a6e394b09c96b.
    """
    receipt_id = (receipt_id or "").strip()
    if not receipt_id:
        raise ValueError("receipt_id is required.")
    return _run_appie("receipt", "show", receipt_id)


if __name__ == "__main__":
    mcp.run()
