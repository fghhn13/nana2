# 文件路径: nana_2/plugins/post_it_note/post_it_note_app.py

import tkinter as tk
import keyboard
import json
import os
import sys
import ctypes

# --- 全局变量和配置 ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# 文件路径现在从脚本所在目录计算，确保无论从哪里运行都正确
BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_DIR, "nana_note_config.json")
LOCK_FILE = os.path.join(BASE_DIR, "note.lock")


# --- 便签应用类 ---
class NoteApp:
    def __init__(self, root):
        self.root = root
        self.is_transparent_mode = False
        self.drag_start_x = None
        self.drag_start_y = None

        # --- 配色方案 ---
        self.BG_TRANSPARENT_KEY = "#2E2E2E"
        self.BG_ROOT = self.BG_TRANSPARENT_KEY
        self.FG_TEXT = "yellow"
        self.BG_TEXT_AREA = self.BG_TRANSPARENT_KEY
        self.CURSOR_COLOR_NORMAL = "white"
        self.CURSOR_COLOR_TRANSPARENT = self.BG_TRANSPARENT_KEY

        self._setup_window()
        self._setup_widgets()
        self._bind_events()
        self._load_initial_state()

        # 启动周期性检查
        self.check_for_updates()

    def _setup_window(self):
        """配置窗口基础属性"""
        self.root.title("Nana酱的便签")
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.configure(bg=self.BG_ROOT)
        self.root.geometry("400x300+50+50")  # 初始大小和位置

    def _setup_widgets(self):
        """创建文本框等组件"""
        self.text_area = tk.Text(
            self.root, wrap=tk.WORD, font=("微软雅黑", 16),
            bg=self.BG_TEXT_AREA, fg=self.FG_TEXT, bd=0, padx=10, pady=10,
            insertbackground=self.CURSOR_COLOR_NORMAL, highlightthickness=0,
            selectbackground="#555555"
        )
        self.text_area.pack(expand=True, fill='both')

    def _bind_events(self):
        """绑定所有事件"""
        self.root.bind('<Shift-Escape>', self.on_close)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.text_area.bind("<MouseWheel>", self._on_mouse_wheel)
        keyboard.add_hotkey('ctrl+h', self.toggle_mode_callback)

    def _on_mouse_wheel(self, event):
        """处理鼠标滚轮事件"""
        self.text_area.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def _save_config(self, config_data):
        """保存配置文件"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
        except IOError:
            pass

    def _load_initial_state(self):
        """加载初始内容和状态"""
        config = self._load_config()
        content = config.get('note_content', '欢迎使用Nana酱的便签！\n\n- 按 Ctrl+H 切换模式\n- 按 Shift+Esc 关闭')
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", content)

        if config.get('force_transparent', False):
            self.root.geometry(f"400x300+0+0")  # 移动到左上角
            self.set_transparent_mode(True)
            config['force_transparent'] = False
            self._save_config(config)
        else:
            initial_mode = config.get('is_transparent_mode', False)
            self.set_transparent_mode(initial_mode, save_state=False)

    def set_transparent_mode(self, is_transparent, save_state=True):
        """设置或取消透明模式"""
        self.is_transparent_mode = is_transparent
        if is_transparent:
            self.root.wm_attributes('-transparentcolor', self.BG_TRANSPARENT_KEY)
            self.text_area.config(state=tk.DISABLED, insertbackground=self.CURSOR_COLOR_TRANSPARENT)
            self.root.unbind("<Button-1>")
            self.root.unbind("<B1-Motion>")
        else:
            self.root.wm_attributes('-transparentcolor', '')
            self.text_area.config(state=tk.NORMAL, insertbackground=self.CURSOR_COLOR_NORMAL)
            self.text_area.focus_set()
            self.root.bind("<Button-1>", self._start_drag)
            self.root.bind("<B1-Motion>", self._on_drag)

        if save_state:
            config = self._load_config()
            config['is_transparent_mode'] = is_transparent
            self._save_config(config)

    def toggle_mode_callback(self):
        """切换模式的回调"""
        self.set_transparent_mode(not self.is_transparent_mode)

    def _start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def _on_drag(self, event):
        if self.drag_start_x is not None:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            x = self.root.winfo_x() + dx
            y = self.root.winfo_y() + dy
            self.root.geometry(f"+{x}+{y}")

    def on_close(self, event=None):
        """关闭窗口时的清理工作"""
        current_content = self.text_area.get("1.0", tk.END).strip()
        config = self._load_config()
        config['note_content'] = current_content
        config['is_transparent_mode'] = self.is_transparent_mode
        config.pop('force_refresh', None)  # 清理刷新标志
        config.pop('force_transparent', None)
        self._save_config(config)

        keyboard.unhook_all()
        # 删除锁文件
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        self.root.destroy()
        sys.exit()

    def check_for_updates(self):
        """周期性检查配置文件是否有刷新请求"""
        config = self._load_config()
        if config.get('force_refresh', False):
            # 获取当前滚动条位置
            scroll_pos_before = self.text_area.yview()

            # 更新内容
            new_content = config.get('note_content', '')
            self.text_area.config(state=tk.NORMAL)  # 临时启用以修改内容
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_content)

            # 恢复滚动条位置
            self.text_area.yview_moveto(scroll_pos_before[0])

            # 如果要求强制透明，则执行
            if config.get('force_transparent', False):
                self.root.geometry(f"400x300+0+0")  # 移动到左上角
                self.set_transparent_mode(True)

            # 重置标志并保存
            config['force_refresh'] = False
            config['force_transparent'] = False
            self._save_config(config)

        # 安排下一次检查
        self.root.after(1000, self.check_for_updates)  # 每1000毫秒（1秒）检查一次


def main():
    """主函数，处理应用启动逻辑"""
    if os.path.exists(LOCK_FILE):
        # 如果锁文件存在，说明已有实例在运行，直接退出
        # 指令已经由 __init__.py 发出并保存在 config.json 中，运行中的实例会捕捉到
        return

    # 如果没有实例在运行，则创建锁文件并启动应用
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

        root = tk.Tk()
        app = NoteApp(root)
        root.mainloop()
    finally:
        # 确保在任何情况下退出时都删除锁文件
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)


if __name__ == "__main__":
    main()