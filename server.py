#!/usr/bin/env python3
"""
MCP Server for Mac say command (TTS)

Usage:
    python server.py

The server will start on http://0.0.0.0:8765/mcp/

Configuration:
    All settings can be configured in config.yaml
"""

from mcp.server import Server
from mcp.server.streamable_http import StreamableHTTPServer
from mcp.types import TextContent
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


app = Server("say-tts")


@app.list_tools()
async def list_tools():
    return [
        type(
            "Tool",
            (),
            {
                "name": "say",
                "description": "Speak text using Mac's say command. Useful for TTS output.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to speak",
                        },
                        "voice": {
                            "type": "string",
                            "description": "Optional voice name (e.g., 'Alex', 'Samantha'). If not specified, uses default voice from config.",
                        },
                    },
                    "required": ["text"],
                },
            },
        )()
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict, config: dict | None = None):
    if name == "say":
        text = arguments.get("text", "")
        voice = arguments.get("voice")

        # Use default voice from config if not specified
        if not voice and config:
            voice = config.get("say", {}).get("default_voice")

        cmd = ["say"]
        if voice:
            cmd.extend(["-v", voice])
        cmd.append(text)

        subprocess.run(cmd, check=True)
        return [TextContent(type="text", text=f"Spoken: {text}")]

    raise ValueError(f"Unknown tool: {name}")


async def main(host: str = "0.0.0.0", port: int = 8765, config: dict | None = None):
    # Store config in app context for access in call_tool
    app._config = config or {}
    server = StreamableHTTPServer(app, host=host, port=port)
    print(f"MCP say-tts server running on http://{host}:{port}/mcp/")
    print(f"Config: {app._config}")
    await server.run()


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="MCP Server for Mac say command")
    parser.add_argument("--config", "-c", help="Path to config file (default: config.yaml)")
    parser.add_argument("--host", help="Host to bind to (overrides config)")
    parser.add_argument("--port", type=int, help="Port to bind to (overrides config)")
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)

    # CLI args override config file
    host = args.host or config.get("host", "0.0.0.0")
    port = args.port or config.get("port", 8765)

    asyncio.run(main(host, port, config))
