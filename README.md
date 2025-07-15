# Nana 2

Nana 2 是一个使用 `tkinter` 构建的桌面助手，依托 DashScope 提供的 OpenAI 兼容接口进行自然语言识别，并通过插件系统扩展能力。

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

## 插件接口

如需扩展功能，可在 `plugins` 目录新建文件夹并实现模块，提供 `get_plugin()`
函数并返回继承 `BasePlugin` 的实例。

插件需实现以下方法：

* `get_name()` - 插件的唯一标识
* `get_commands()` - 插件支持的命令列表
* `execute(command, args, controller)` - 执行具体任务

`CommandExecutor` 会根据 `get_plugin()` 动态导入插件并注册命令。

## 运行测试

项目内含若干单元测试，可使用 `pytest` 执行：

```bash
pytest
```

确保测试依赖已正确安装。

