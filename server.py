#!/usr/bin/env python3
"""
MCP Server for Mac say command (TTS)

Usage:
    python server.py

The server will start on http://0.0.0.0:8765/mcp/

Configuration:
    All settings can be configured in config.yaml
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
import subprocess
import argparse
import os
import yaml
from pathlib import Path
from typing import Any


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = os.environ.get("SAY_MCP_CONFIG", "config.yaml")

    path = Path(config_path)
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f) or {}
    return {}


# Load config
config = load_config()

# Create MCP server with transport security disabled for localhost/host.docker.internal
transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=False
)

mcp = FastMCP("say-tts", transport_security=transport_security)


@mcp.tool()
def say(text: str, voice: str | None = None) -> str:
    """
    Speak text using Mac's say command. Useful for TTS output.

    Args:
        text: Text to speak
        voice: Optional voice name (e.g., 'Alex', 'Samantha'). If not specified, uses default voice from config.
    """
    # Use default voice from config if not specified
    if not voice:
        voice = config.get("say", {}).get("default_voice")

    cmd = ["say"]
    if voice:
        cmd.extend(["-v", voice])
    cmd.append(text)

    subprocess.run(cmd, check=True)
    return f"Spoken: {text}"


async def main(host: str = "0.0.0.0", port: int = 8765):
    import uvicorn
    import asyncio
    # 使用 streamable_http 模式
    app = mcp.streamable_http_app()
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    print(f"MCP say-tts server running on http://{host}:{port}/mcp/")
    await server.serve()


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="MCP Server for Mac say command")
    parser.add_argument("--config", "-c", help="Path to config file (default: config.yaml)")
    parser.add_argument("--host", help="Host to bind to (overrides config)")
    parser.add_argument("--port", type=int, help="Port to bind to (overrides config)")
    args = parser.parse_args()

    # Reload config with custom path if specified
    if args.config:
        config = load_config(args.config)

    # CLI args override config file
    host = args.host or config.get("host", "0.0.0.0")
    port = args.port or config.get("port", 8765)

    asyncio.run(main(host, port))
