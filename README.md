# mac-say-mcp-servers

Mac TTS (say command) MCP Server - 让 AI 通过 MCP 调用 Mac 的 say 命令生成语音

## 功能

- 通过 MCP 协议提供 say 命令能力
- 支持 HTTP 模式运行，可供 Docker 容器中的 nanobot 使用
- 支持配置文件

## 安装

```bash
cd ~/workspace/mac-say-mcp-servers
pip install -e .
```

或

```bash
pip install mcp pyyaml
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
```

### 配置项说明

| 配置项 | 类型 | 说明 |
|--------|------|------|
| `host` | string | 服务绑定的地址 |
| `port` | int | 服务监听的端口 |
| `say.default_voice` | string/null | 默认语音，null 使用系统默认 |

### 优先级

命令行参数 > 环境变量 > 配置文件

- CLI: `python server.py --port 9000`
- 环境变量: `SAY_MCP_CONFIG=/path/to/config.yaml`

## 使用

### 启动服务

```bash
python server.py
```

服务默认监听 `http://0.0.0.0:8765/mcp/`

### 配置 nanobot

在 `~/.nanobot/config.json` 中添加：

```json
{
  "tools": {
    "mcp_servers": {
      "say": {
        "url": "http://host.docker.internal:8765/mcp/",
        "tool_timeout": 30
      }
    }
  }
}
```

### 使用示例

在 nanobot 中让 AI 说一段话：

```
请用 say 工具说 "Hello, this is a test"
```

## 开发

```bash
# 安装依赖
pip install -e .

# 测试运行
python server.py
```
