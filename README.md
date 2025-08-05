# Nana 2

Nana 2 是一个使用 `tkinter` 构建的桌面助手，依托 DashScope 提供的 OpenAI 兼容接口进行自然语言识别，并通过插件系统扩展能力。

## 主要特性

* 简洁的图形界面，基于 `tkinter` 实现。
* 兼容 OpenAI 接口，可直接调用 DashScope 服务。
* 插件化设计，便于扩展新能力。
* 内置命令执行器，可根据意图调用插件提供的功能。

## 环境准备

1. **创建虚拟环境**（可选）：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 使用 venv\Scripts\activate
   ```
2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```
3. **配置 API 密钥**：在项目根目录创建 `.env` 文件，内容如下：
   ```env
   DASHSCOPE_API_KEY=your_openai_key
   ```
4. **启动程序**：
   ```bash
   python main.py
   ```

程序启动后会连接 AI 服务，并自动加载 `plugins` 目录下的插件。

## 项目结构

```
./
├── core              # 核心逻辑与工具
├── plugins           # 插件目录，每个子文件夹即一个插件
├── tests             # 单元测试
├── main.py           # 程序入口
└── requirements.txt  # 依赖列表
```

## 插件接口

如需扩展功能，可在 `plugins` 目录新建文件夹并实现模块，提供 `get_plugin()`
函数并返回继承 `BasePlugin` 的实例。

插件需实现以下方法：

* `get_name()` - 插件的唯一标识
* `get_commands()` - 插件支持的命令列表
* `execute(command, args, controller)` - 执行具体任务

`CommandExecutor` 会根据 `get_plugin()` 动态导入插件并注册命令。

### 插件开发示例

以下示例展示了一个最简单的插件结构：

```python
from core.plugins import BasePlugin

class HelloPlugin(BasePlugin):
    def get_name(self):
        return "hello"

    def get_commands(self):
        return {"hello": []}

    def execute(self, command, args, controller):
        if command == "hello":
            controller.speak("你好，世界！")


def get_plugin():
    return HelloPlugin()
```

将上述代码放入 `plugins/hello` 目录中并确保包含 `__init__.py` 文件即可在启动时自动加载。

## 运行测试

项目内含若干单元测试，可使用 `pytest` 执行：

```bash
pytest
```

确保测试依赖已正确安装。

