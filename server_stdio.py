#!/usr/bin/env python3
"""
MCP Server for Mac say command (TTS) - Stdio Mode

Usage:
    python server_stdio.py

This version uses stdio mode, meant to be run directly or via SSH.
"""

from mcp.server.fastmcp import FastMCP
import subprocess
import os
import yaml
from pathlib import Path


def load_config(config_path: str | None = None) -> dict:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = os.environ.get("SAY_MCP_CONFIG", "config.yaml")

    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}


config = load_config()
mcp = FastMCP("say-tts")


@mcp.tool()
def say(text: str, voice: str | None = None) -> str:
    """
    Speak text using Mac's say command. Useful for TTS output.

    Args:
        text: Text to speak
        voice: Optional voice name (e.g., 'Alex', 'Samantha'). If not specified, uses default voice from config.
    """
    if not voice:
        voice = config.get("say", {}).get("default_voice")

    cmd = ["say"]
    if voice:
        cmd.extend(["-v", voice])
    cmd.append(text)

    subprocess.run(cmd, check=True)
    return f"Spoken: {text}"


if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.run_stdio_async())
