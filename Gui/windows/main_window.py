# Gui/windows/main_window.py

import tkinter as tk
import queue
from tkinter import messagebox, DISABLED, NORMAL, END
from ..config import gui_config
from ..handle import event_handlers
from global_config import settings

class MainWindow:
    def __init__(self, master: tk.Tk, app_controller):
        """
        主窗口的构造函数
        :param master: tk.Tk() 的根实例
        :param app_controller: 主应用程序的控制器实例，用于通信
        """
        self.settings = settings
        self.master = master
        self.controller = app_controller  # 外部逻辑通信的桥梁
        self.gui_config = gui_config  # 加载UI配置
        self.note_listbox = None
        try:
            # 使用 gui_config 中的路径
            self.img_send_normal = tk.PhotoImage(file=self.gui_config.IMG_SEND_NORMAL)
            self.img_send_hover = tk.PhotoImage(file=self.gui_config.IMG_SEND_HOVER)
            self.img_send_press = tk.PhotoImage(file=self.gui_config.IMG_SEND_PRESS)
        except FileNotFoundError as e:
            messagebox.showerror("资源错误", f"找不到按钮图片文件！\n{e}")
            self.img_send_normal = None
        # --- 1. 基础窗口设置 ---
        self.master.title(self.gui_config.APP_TITLE)
        self.master.geometry(self.gui_config.MAIN_WINDOW_SIZE)
        self.master.config(bg=self.gui_config.BG_MAIN)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- 2. 状态与通信 ---
        # 这个队列是线程安全的，用于从任何地方向GUI发送更新任务
        self.ui_queue = queue.Queue()

        # --- 3. 创建界面和绑定事件 ---
        self.handler = event_handlers.EventHandler(self, self.controller)
        self._create_widgets()
        self.handler.bind_events()
        self.handler.add_placeholder()  # 设置初始输入框提示

        # --- 4. 启动UI更新循环 ---
        # 这个循环会定期检查队列里有没有新任务，并执行它们
        self.master.after(100, self.process_ui_queue)

        # --- 5. 初始化完成 ---
        self.user_input_entry.focus_set()


    def _create_widgets(self):


        chat_frame = tk.Frame(self.master, bg=self.gui_config.BG_MAIN)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        chat_frame.rowconfigure(0, weight=1)
        chat_frame.columnconfigure(0, weight=1)
        self.chat_display = tk.Text(
            chat_frame, wrap=tk.WORD, state=DISABLED,
            font=(self.gui_config.GENERAL_FONT_FAMILY, self.gui_config.GENERAL_FONT_SIZE),
            bg=self.gui_config.BG_INPUT, fg=self.gui_config.FG_TEXT, insertbackground=self.gui_config.CURSOR_COLOR, bd=0
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", pady=(0, 24))
        self.chat_display.tag_config("user_sender", foreground="#81C784",
                                     font=(self.gui_config.GENERAL_FONT_FAMILY, self.gui_config.GENERAL_FONT_SIZE, "bold"))
        self.chat_display.tag_config("nana_sender", foreground="#82AAFF",
                                     font=(self.gui_config.GENERAL_FONT_FAMILY, self.gui_config.GENERAL_FONT_SIZE, "bold"))
        self.chat_display.tag_config("error_sender", foreground="#FF5370",
                                     font=(self.gui_config.GENERAL_FONT_FAMILY, self.gui_config.GENERAL_FONT_SIZE, "bold"))

        input_frame = tk.Frame(chat_frame, bg=self.gui_config.BG_MAIN)
        input_frame.grid(row=1, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.user_input_entry = tk.Entry(
            input_frame,
            font=(self.gui_config.GENERAL_FONT_FAMILY, self.gui_config.GENERAL_FONT_SIZE),
            bg=self.gui_config.BG_INPUT,
            fg=self.gui_config.FG_TEXT,
            disabledbackground=self.gui_config.BG_INPUT_DISABLED,
            disabledforeground=self.gui_config.FG_TEXT_DISABLED,
            insertbackground=self.gui_config.CURSOR_COLOR,
            bd=0,
            relief=tk.FLAT
        )
        self.user_input_entry.grid(row=0, column=0, sticky="ew", ipady=16, padx=(0, 10))

        if self.img_send_normal:
            self.send_button = tk.Button(
                input_frame, image=self.img_send_normal, command=self.handler.on_send_click, bg=self.gui_config.BG_MAIN,
                activebackground=self.gui_config.BG_MAIN, relief=tk.FLAT, bd=0, cursor="hand2"
            )
        else:
            self.send_button = tk.Button(input_frame, text="发送", command=self.handler.on_send_click)
        self.send_button.grid(row=0, column=1, ipady=4)

    def append_message(self, sender, message, sender_tag):   # ... (这部分函数内容不变)
        self.chat_display.config(state=NORMAL)
        self.chat_display.insert(END, f"{sender}: ", (sender_tag,))
        self.chat_display.insert(END, f"{message}\n\n")
        self.chat_display.config(state=DISABLED)
        self.chat_display.see(END)

    def set_ui_state(self, state: str):
        """
        设置UI的交互状态，'enabled' 或 'disabled'。
        """
        tk_state = NORMAL if state == 'enabled' else DISABLED
        self.user_input_entry.config(state=tk_state)
        self.send_button.config(state=tk_state)

    def process_ui_queue(self):
        """
        处理消息队列，在主线程中安全地更新UI。
        """
        try:
            while not self.ui_queue.empty():
                msg_type, data = self.ui_queue.get_nowait()

                # 在这里根据消息类型，调用不同的UI更新方法
                if msg_type == "APPEND_MESSAGE":
                    sender, message, tag = data
                    self.append_message(sender, message, tag)
                elif msg_type == "SET_STATE":
                    self.set_ui_state(data)
                elif msg_type == "RUN_FUNC":
                    func = data
                    func()
                # elif msg_type == "SHOW_ERROR":
                #     messagebox.showerror("错误", data)
                # ... 在这里可以定义和处理更多类型的UI更新消息 ...
        finally:
            self.master.after(100, self.process_ui_queue)

    def on_closing(self):

        self.is_running = False
        self.controller.on_app_exit()  # 通知控制器应用要退出了
        self.master.destroy()