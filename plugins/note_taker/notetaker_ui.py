import tkinter as tk
from tkinter import scrolledtext, messagebox
from .notetaker_handle import get_note_path, get_note_content
from Gui.config import gui_config
from .note_config import EDITOR_WIDTH, EDITOR_HEIGHT


def open_note_editor(note_name: str, content: str = "", master_window=None):
    editor_window = tk.Toplevel(master_window)
    editor_window.title(f"{gui_config.NOTE_EDITOR_TITLE_PREFIX}{note_name}")
    editor_window.config(bg=gui_config.BG_MAIN)

    text_area = scrolledtext.ScrolledText(
        editor_window,
        wrap=tk.WORD,
        width=EDITOR_WIDTH,
        height=EDITOR_HEIGHT,
        font=(gui_config.GENERAL_FONT_FAMILY, gui_config.GENERAL_FONT_SIZE),
        bg=gui_config.BG_INPUT,
        fg=gui_config.FG_TEXT,
        insertbackground=gui_config.CURSOR_COLOR,
        bd=0,
    )
    text_area.insert(tk.END, content)
    text_area.pack(padx=10, pady=10, fill="both", expand=True)

    def save_note():
        current_content = text_area.get(1.0, tk.END).strip()
        try:
            with open(get_note_path(note_name), "w", encoding="utf-8") as f:
                f.write(current_content)
            messagebox.showinfo(
                gui_config.CONFIRM_SAVE_TITLE,
                gui_config.CONFIRM_SAVE_MESSAGE.format(note_name=note_name),
                parent=editor_window,
            )
        except Exception as e:
            messagebox.showerror(
                gui_config.ERROR_SAVE_TITLE,
                gui_config.ERROR_SAVE_MESSAGE.format(e=e),
                parent=editor_window,
            )

    def on_close():
        save_note()
        editor_window.destroy()

    editor_window.protocol("WM_DELETE_WINDOW", on_close)


def open_notes_window(notes: list[str], master_window=None):
    win = tk.Toplevel(master_window)
    win.title(gui_config.NOTES_WINDOW_TITLE)
    win.config(bg=gui_config.BG_MAIN)

    listbox = tk.Listbox(
        win,
        bg=gui_config.BG_LISTBOX,
        fg=gui_config.FG_LISTBOX,
        selectbackground=gui_config.SELECT_BG_LISTBOX,
        selectforeground=gui_config.SELECT_FG_LISTBOX,
    )
    for n in notes:
        listbox.insert(tk.END, n)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)

    def on_open(event=None):
        selection = listbox.curselection()
        if selection:
            note_name = listbox.get(selection[0])
            content = get_note_content(note_name) or ""
            open_note_editor(note_name, content, master_window)

    listbox.bind("<Double-1>", on_open)


def confirm_delete(note_name: str, master_window=None) -> bool:
    """显示确认删除对话框，用户选择是或否"""
    return messagebox.askyesno(
        gui_config.CONFIRM_DELETE_TITLE,
        gui_config.CONFIRM_DELETE_MESSAGE.format(note_name=note_name),
        parent=master_window,
    )
