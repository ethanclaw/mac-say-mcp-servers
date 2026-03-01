# mac-say-mcp-servers

Mac TTS (say command) MCP Server - 让 AI 通过 MCP 调用 Mac 的 say 命令生成语音

## 功能

- `say` - 生成音频文件（返回文件路径，可用于 Telegram 语音消息）
- `say_play` - 直接播放语音（即时播放，不生成文件）

## 支持的 AI 助手

- nanobot
- 其他支持 MCP HTTP 模式的 AI 助手

## 安装

```bash
cd ~/workspace/mac-say-mcp-servers
pip install -e .
```

或

```bash
pip install mcp pyyaml uvicorn
```

## 配置

配置文件为 `config.yaml`：

```yaml
# Server settings
host: "0.0.0.0"
port: 8765

# say command settings
say:
  # 可用的语音列表，通过 say -v | head -20 查看
  default_voice: null  # null 表示使用系统默认
  # 输出目录
  output_dir: "/Users/ethan/.nanobot/workspace/media/say"
  # Docker容器内的挂载路径（用于返回给nanobot的路径）
  container_path: "/root/.nanobot/workspace/media/say"
```

### 配置项说明

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `host` | string | 服务绑定的地址 |
| `port` | int | 服务监听的端口 |
| `say.default_voice` | string/null | 默认语音，null 使用系统默认 |
| `say.output_dir` | string | 音频文件输出目录 |
| `say.container_path` | string | Docker 容器内访问路径 |

## 使用

### 启动服务

```bash
python server.py
```

服务默认监听 `http://0.0.0.0:8765/mcp/`

### 在 nanobot 中使用

在 `~/.nanobot/config.json` 中添加：

```json
{
  "tools": {
    "mcp_servers": {
      "say": {
        "url": "http://host.docker.internal:8765/mcp",
        "toolTimeout": 30
      }
    }
  }
}
```

### 使用示例

生成音频文件（用于发送语音消息）：

```
用 mcp_say_say 说 "你好"
```

直接播放：

```
用 mcp_say_say_play 说 "你好"
```

## 常见问题

### Docker 容器无法连接

如果 Docker 容器中的 nanobot 无法连接 MCP 服务，确保：

1. MCP 服务绑定到 `0.0.0.0` 而不是 `127.0.0.1`
2. 使用 `host.docker.internal` 访问宿主机
3. 端口已正确开放

### 端口被占用

```bash
# 查看端口占用
lsof -i :8765

# 杀掉占用进程
kill <PID>
```

## License

MIT
