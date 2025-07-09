# Gui/handle/event_handlers.py
from core.log.logger_config import logger
from tkinter import END


class EventHandler:
    def __init__(self, main_view, controller):

        self.view = main_view
        self.controller = controller
        self.placeholder_text = self.view.gui_config.INPUT_PLACEHOLDER

    def on_send_click(self, event=None):
        """
        处理“发送”按钮的点击事件 或 输入框的回车事件。
        """
        user_text = self.view.user_input_entry.get().strip()

        # 如果输入为空或者是占位符，则不执行任何操作
        if not user_text or user_text == self.placeholder_text:
            return "break"  # 阻止事件继续传播

        logger.info(f"捕获到用户输入: {user_text}")

        # 清空输入框
        self.view.user_input_entry.delete(0, END)

        # 通过控制器将用户输入发送到后端逻辑
        self.controller.process_user_input(user_text)

        return "break"  # 阻止回车键的默认换行行为


    def bind_events(self):
        """集中绑定所有事件。"""
        # 绑定发送按钮的鼠标事件
        if self.view.img_send_normal:  # 确保图片按钮存在
            self.view.send_button.bind("<Enter>", self.on_button_enter)
            self.view.send_button.bind("<Leave>", self.on_button_leave)
            self.view.send_button.bind("<Button-1>", self.on_button_press)
            self.view.send_button.bind("<ButtonRelease-1>", self.on_button_release)

        # 绑定输入框的回车键事件
        self.view.user_input_entry.bind("<Return>", self.on_input_enter)

        # 为聊天显示框绑定滚轮
        self.view.chat_display.bind("<MouseWheel>", self.on_chat_scroll)
        # 兼容Linux系统的滚轮事件
        self.view.chat_display.bind("<Button-4>", self.on_chat_scroll)
        self.view.chat_display.bind("<Button-5>", self.on_chat_scroll)
        self.view.user_input_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.view.user_input_entry.bind("<FocusOut>", self.on_entry_focus_out)

    def on_button_enter(self, event):
        """鼠标进入按钮"""
        if self.view.img_send_hover:
            self.view.send_button.config(image=self.view.img_send_hover)

    def on_button_leave(self, event):
        """鼠标离开按钮"""
        if self.view.img_send_normal:
            self.view.send_button.config(image=self.view.img_send_normal)

    def on_button_press(self, event):
        """鼠标按下按钮"""
        if self.view.img_send_press:
            self.view.send_button.config(image=self.view.img_send_press)

    def on_button_release(self, event):
        """鼠标释放（恢复到悬停状态）"""
        # 检查鼠标当前是否还在按钮上
        x, y = event.x, event.y
        if 0 <= x < self.view.send_button.winfo_width() and 0 <= y < self.view.send_button.winfo_height():
            if self.view.img_send_hover:
                self.view.send_button.config(image=self.view.img_send_hover)
        else:
            if self.view.img_send_normal:
                self.view.send_button.config(image=self.view.img_send_normal)

    def on_input_enter(self, event):

        return self.on_send_click(event)

    def on_listbox_scroll(self, event):
        """处理笔记列表的鼠标滚轮事件。"""
        # event.delta 在Windows上通常是120的倍数（上滚为正，下滚为负）
        # 在Linux上，我们通过event.num来判断，4是上滚，5是下滚
        if event.num == 4 or event.delta > 0:
            self.view.note_listbox.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.view.note_listbox.yview_scroll(1, "units")

    def on_chat_scroll(self, event):
        """处理聊天显示框的鼠标滚轮事件。"""
        # 原理同上
        if event.num == 4 or event.delta > 0:
            self.view.chat_display.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.view.chat_display.yview_scroll(1, "units")

    def add_placeholder(self):
        """添加占位提示文本"""
        self.view.user_input_entry.insert(0, self.placeholder_text)
        self.view.user_input_entry.config(fg='grey')

    def remove_placeholder(self):
        """移除占位提示文本"""
        self.view.user_input_entry.delete(0, 'end')
        self.view.user_input_entry.config(fg=self.view.gui_config.FG_TEXT)  # 恢复正常的文字颜色

    def on_entry_focus_in(self, event):
        """当输入框获得焦点时触发"""
        # 如果当前显示的是提示文本，就清空它
        if self.view.user_input_entry.get() == self.placeholder_text:
            self.remove_placeholder()

    def on_entry_focus_out(self, event):
        """当输入框失去焦点时触发"""
        # 如果输入框里什么都没有，就重新显示提示文本
        if not self.view.user_input_entry.get():
            self.add_placeholder()