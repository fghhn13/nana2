# clear_logs.py
import os
import sys

# --- 配置 ---
# 我们统一日志文件名称为 nana.log，文件位于与本脚本相同的目录
LOG_FILE_NAME = "nana.log"

def clear_log_file():
    """
    一个安全的小程序，用于清空指定的日志文件。
    在执行前会请求用户确认。
    """
    # 获取脚本所在的目录，从而定位项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(project_root, LOG_FILE_NAME)

    print("="*50)
    print(" Nana 日志清理程序 ".center(50, "~"))
    print("="*50)
    print(f"准备清理日志文件: {log_file_path}\n")

    # 1. 检查文件是否存在
    if not os.path.exists(log_file_path):
        print(f"❌ 错误：找不到日志文件 '{LOG_FILE_NAME}'。")
        print("请确保本程序和日志文件都在项目根目录下。")
        sys.exit(1) # 退出程序

    # 2. 请求用户确认
    try:
        # raw_input in python 2, input in python 3
        confirm = input("⚠️ 你确定要清空所有日志记录吗？这个操作无法撤销！(输入 y 确认, 其他任意键取消): ")
    except KeyboardInterrupt:
        print("\n\n操作已取消。")
        sys.exit(0)

    # 3. 执行清空操作
    if confirm.lower() == 'y':
        try:
            # 使用 'w' 模式打开文件会直接清空文件内容
            with open(log_file_path, 'w') as f:
                pass # 不需要做任何事，文件已经被清空
            print("\n✨ 操作成功！日志文件已被清空。")
        except Exception as e:
            print(f"\n❌ 执行清理时发生错误: {e}")
            sys.exit(1)
    else:
        print("\n操作已取消。日志文件保持原样。")

if __name__ == "__main__":
    clear_log_file()