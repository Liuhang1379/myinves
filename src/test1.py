import os
import subprocess
import time
import schedule
from plyer import notification
import tkinter as tk
from tkinter import messagebox
import json
import sys

# 用于存储需要用户确认的待处理通知
pending_notifications = []

def load_config():
    """读取配置文件以获取通知内容和脚本路径。"""
    with open(r'D:\_Develop\programmierung\python\investment\config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def confirm_notification():
    """显示待处理通知的确认对话框。"""
    global pending_notifications
    if pending_notifications:
        notification_message = pending_notifications.pop(0)
        print(f"显示确认对话框: {notification_message}")
        
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        result = messagebox.askyesno("确认通知", notification_message)
        root.destroy()
        
        if result:
            print("用户确认了通知。")
        else:
            print("用户未确认，重新调度通知。")
            pending_notifications.append(notification_message)

def send_notification_and_run_script(config):
    """发送桌面通知并运行外部 Python 脚本。"""
    message = config['notification_message_017093']
    print(f"发送通知: {message}")
    notification.notify(
        title="重要通知",
        message=message,
        app_name="RyanBo_Invesment",
        timeout=600
    )
    
    # 将通知消息加入待处理列表
    pending_notifications.append(message)

    script_path = config['script_path']
    print(f"尝试启动脚本: {script_path}")
    try:
        subprocess.Popen(["python", script_path])
        print(f"脚本已启动: {script_path}")
    except Exception as e:
        print(f"运行脚本时发生错误: {e}")

def schedule_notifications(config):
    """调度任务以在指定时间发送通知和运行脚本。"""
    for schedule_time in config["schedule_time_017093"]:
        schedule.every().day.at(schedule_time).do(send_notification_and_run_script, config)
        print(f"已设置通知调度时间: {schedule_time}")

    print("通知调度已设置。按 Ctrl+C 退出。")

if __name__ == "__main__":
    # 加载配置
    config = load_config()
    
    script_path = os.path.abspath(__file__)  
    print(f"当前脚本绝对路径: {script_path}")

    # 设置开机启动
    startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_path, 'ScheduledNotification.lnk')

    if not os.path.exists(shortcut_path):
        import winshell
        from win32com.client import Dispatch
        
        print("创建开机启动快捷方式...")
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = f'"{script_path}"'
        shortcut.IconLocation = sys.executable
        shortcut.save()
        print("已创建开机启动快捷方式。")
    else:
        print("开机启动快捷方式已存在，跳过创建。")

    # 调度通知
    schedule_notifications(config)

    try:
        while True:
            schedule.run_pending()
            confirm_notification()
            time.sleep(1)

            if os.path.exists('exit.txt'):
                print("程序已终止。")
                break
    except KeyboardInterrupt:
        print("程序已终止。")
