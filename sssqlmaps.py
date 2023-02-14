
"""
============================
# -*- coding: utf-8 -*-
# @Time    : 2023/2/14 11:02
# @Author  : Denceun_siwei
# @FileName: sssqlmaps.py
# @Software: PyCharm
# @Blogs ：https://www.denceun.com/archives/author/1
===========================
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import subprocess
import threading


class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("sssqlmaps v1.0 - SQL注入批量检测工具 By.思维(www.denceun.com)")
        self.geometry("900x750")

        self.columns = ("URL", "Injection", "Payload")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.text_widget = tk.Text(self, height=20)
        self.text_widget.pack(fill="x")
        self.text_widget.tag_configure("bold_text", font=("TkDefaultFont", 20, "bold"))
        self.text_widget.tag_add("bold_text", "1.0", "end")

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill="x", pady=10)

        import_data_btn = tk.Button(buttons_frame, text="导入URL", command=self.import_data)
        import_data_btn.pack(side="left", padx=10)

        tk.Label(buttons_frame, text="sqlmap -u url --batch").pack(side="left")
        self.params_entry = tk.Entry(buttons_frame, width=50)
        self.params_entry.pack(side="left", padx=10)
        self.params_entry.insert(0, "--level 3")

        self.run_btn = tk.Button(buttons_frame, text="运行", command=self.run)
        self.run_btn.pack(side="left", padx=10)
        clear_btn = tk.Button(buttons_frame, text="清空", command=self.clear_content)
        clear_btn.pack(side="left", padx=10)

    def import_data(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.tree.delete(*self.tree.get_children())
            with open(file_path, "r") as file:
                for line in file:
                    line = line.strip().split(",")
                    self.tree.insert("", "end", values=line)

    def run(self):
        params = self.params_entry.get()
        # print(params)
        self.run_btn.config(text="正在运行", state="disabled")
        thread = threading.Thread(target=self._run_scan, args=(params,))
        thread.start()

    def _run_scan(self, params):
        for item in self.tree.get_children():
            url = self.tree.item(item)["values"][0]
            result = subprocess.run(['sqlmap', '-u', url] + params.split() + ['--batch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # result = subprocess.run(['python', 'sqlmap.py', '-u', url] + params.split() + ['--batch'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result_output = result.stdout.decode("utf-8") + result.stderr.decode("utf-8")
            self.text_widget.insert("end", result_output)
            self.text_widget.update()
            if "Parameter: " in result_output:
                self.tree.set(item, "Injection", "Yes")
                payload_start = result_output.index("Payload:") + len("Payload:")
                payload_end = result_output.index("\n", payload_start)
                self.tree.set(item, "Payload", result_output[payload_start:payload_end].strip())
            else:
                self.tree.set(item, "Injection", "No")
        self.run_btn.config(text="运行", state="normal")

    def clear_content(self):
        self.text_widget.delete("1.0", "end")
        for item in self.tree.get_children():
            self.tree.set(item, "URL", "")
            self.tree.set(item, "Injection", "")
            self.tree.set(item, "Payload", "")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
