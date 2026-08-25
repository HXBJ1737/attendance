import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import sys
import threading

CONFIG_FILE = 'config.json'

def resource_path(relative_path):
    """获取资源文件路径，兼容PyInstaller打包"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

def app_dir():
    """exe（或脚本）所在目录，用于存放需要持久化的文件"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def load_config():
    # 优先读 exe 所在目录（用户保存的配置）
    path = os.path.join(app_dir(), CONFIG_FILE)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    # 回退：读打包内置的默认配置
    bundled = resource_path(CONFIG_FILE)
    if os.path.exists(bundled):
        with open(bundled, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'username': '', 'password': '',
        'start_date': '', 'end_date': '',
        'work_end_time': '17:20',
        'unchecked_days': '0',
        'login_url': ''
    }

def save_config(cfg):
    path = os.path.join(app_dir(), CONFIG_FILE)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title('考勤打卡记录爬取工具(已考虑调休工作日和周末)')
        self.root.geometry('480x380')
        self.root.resizable(False, False)

        self.config = load_config()
        self.build_ui()

    def build_ui(self):
        frame = ttk.LabelFrame(self.root, text='配置信息', padding=10)
        frame.pack(padx=15, pady=10, fill='x')

        labels = ['工号:', '密码:', '起始日期:', '终止日期:', '加班起算时间:', '未打卡工作日天数(居家等):']
        keys = ['username', 'password', 'start_date', 'end_date', 'work_end_time', 'unchecked_days']
        self.entries = {}

        for i, (label, key) in enumerate(zip(labels, keys)):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=4)
            entry = ttk.Entry(frame, width=30, show='*' if key == 'password' else '')
            entry.insert(0, str(self.config.get(key, '')))
            entry.grid(row=i, column=1, padx=5, pady=4)
            self.entries[key] = entry

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)

        self.run_btn = ttk.Button(btn_frame, text='开始爬取', command=self.run)
        self.run_btn.pack(side='left', padx=10)

        ttk.Button(btn_frame, text='保存配置', command=self.save).pack(side='left', padx=10)

        self.status_var = tk.StringVar(value='就绪')
        ttk.Label(self.root, textvariable=self.status_var, foreground='gray').pack(pady=5)

    def save(self):
        for key, entry in self.entries.items():
            self.config[key] = entry.get().strip()
        try:
            save_config(self.config)
            messagebox.showinfo('提示', '配置已保存到程序目录')
        except Exception as e:
            messagebox.showerror('错误', f'保存配置失败：{e}')

    def run(self):
        for key, entry in self.entries.items():
            self.config[key] = entry.get().strip()

        if not self.config['username'] or not self.config['password']:
            messagebox.showerror('错误', '请输入工号和密码')
            return
        if not self.config['start_date'] or not self.config['end_date']:
            messagebox.showerror('错误', '请输入起止日期')
            return

        ud = self.config.get('unchecked_days', '').strip()
        if ud and (not ud.isdigit()):
            messagebox.showerror('错误', '未打卡工作日天数需为非负整数')
            return

        self.run_btn.config(state='disabled')
        self.status_var.set('正在运行，请勿关闭浏览器...')
        threading.Thread(target=self.do_scrape, daemon=True).start()

    def do_scrape(self):
        def progress(msg):
            self.root.after(0, lambda: self.status_var.set(msg))

        try:
            from scraper import run_scrape
            result = run_scrape(self.config, progress)
            self.root.after(0, lambda: self.on_done(result))
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))

    def on_done(self, result):
        self.run_btn.config(state='normal')
        self.status_var.set('完成')
        messagebox.showinfo('完成', result)

    def on_error(self, msg):
        self.run_btn.config(state='normal')
        self.status_var.set('出错')
        messagebox.showerror('错误', msg)

if __name__ == '__main__':
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
