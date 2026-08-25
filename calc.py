import tkinter as tk
from tkinter import ttk
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class OvertimeCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title('加班时长百分比计算器')
        self.root.geometry('600x500')
        self.root.resizable(True, True)

        self.build_ui()

    def build_ui(self):
        # 输入区域
        input_frame = ttk.LabelFrame(self.root, text='参数设置', padding=10)
        input_frame.pack(padx=15, pady=10, fill='x')

        params = [
            ('p', 'p (已加班时长):', '52.73'),
            ('q', 'q (满加班时长):', '116'),
            ('y', 'y (连续加班天数):', '20'),
            ('h', 'h (每天加班小时):', '0'),
            ('weekend', 'weekend (周末加班总时长):', '0'),
            ('h步长', 'h步长 (每次递增):', '0.5'),
            ('循环次数', '循环次数:', '9'),
        ]

        self.entries = {}
        for i, (key, label, default) in enumerate(params):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=3)
            entry = ttk.Entry(input_frame, width=20)
            entry.insert(0, default)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entries[key] = entry

        # 按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text='计算', command=self.calculate).pack(side='left', padx=10)

        # 结果区域
        result_frame = ttk.LabelFrame(self.root, text='计算结果', padding=10)
        result_frame.pack(padx=15, pady=5, fill='both', expand=True)

        self.result_text = tk.Text(result_frame, height=15, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(result_frame, orient='vertical', command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def calculate(self):
        try:
            p = float(self.entries['p'].get())
            q = float(self.entries['q'].get())
            y = float(self.entries['y'].get())
            h = float(self.entries['h'].get())
            weekend = float(self.entries['weekend'].get())
            step = float(self.entries['h步长'].get())
            count = int(self.entries['循环次数'].get())
        except ValueError:
            from tkinter import messagebox
            messagebox.showerror('错误', '请输入有效的数字')
            return

        self.result_text.delete('1.0', tk.END)

        # 表头
        header = f'{"连续天数":>10} {"每天加班":>10} {"周末加班":>10} {"百分比":>10}'
        self.result_text.insert(tk.END, header + '\n')
        self.result_text.insert(tk.END, '-' * 50 + '\n')

        for i in range(count):
            if (q + y * h) != 0:
                x = (p + y * h + weekend) / (q + y * h) * 100
            else:
                x = 0
            line = f'{int(y):>10} {h:>10.1f} {weekend:>10.0f} {x:>10.2f}%'
            self.result_text.insert(tk.END, line + '\n')
            h += step

        # 汇总
        self.result_text.insert(tk.END, '-' * 50 + '\n')
        self.result_text.insert(tk.END, f'\n初始参数: p={p}, q={q}, y={int(y)}, weekend={weekend}\n')
        self.result_text.insert(tk.END, f'步长: h每次+{step}, 共{count}次\n')

if __name__ == '__main__':
    root = tk.Tk()
    app = OvertimeCalcApp(root)
    root.mainloop()
