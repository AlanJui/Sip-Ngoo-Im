import tkinter as tk
from tkinter import ttk

import pandas as pd

# 讀取 Excel 文件
file_path = "D100_彙集雅俗通十五音字典.xlsx"
df_dict = pd.read_excel(file_path, sheet_name="彙集雅俗通字典")

def search_hanzi(yunmu: str, diao: str, siann: str):
    """ 檢索符合條件的漢字 """
    results = df_dict[(df_dict["韻"] == yunmu) & (df_dict["調"].astype(str) == diao) & (df_dict["聲"] == siann)]
    return results[["漢字", "十五音標音"]].head(5)

class MinnanInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("閩南話輸入法 (河洛白話)")
        self.root.geometry("500x400")

        # 韻母輸入
        self.label_yunmu = tk.Label(root, text="韻母:")
        self.label_yunmu.grid(row=0, column=0, padx=5, pady=5)
        self.entry_yunmu = tk.Entry(root)
        self.entry_yunmu.grid(row=0, column=1, padx=5, pady=5)

        # 聲調輸入
        self.label_diao = tk.Label(root, text="聲調:")
        self.label_diao.grid(row=1, column=0, padx=5, pady=5)
        self.entry_diao = tk.Entry(root)
        self.entry_diao.grid(row=1, column=1, padx=5, pady=5)

        # 聲母輸入
        self.label_siann = tk.Label(root, text="聲母:")
        self.label_siann.grid(row=2, column=0, padx=5, pady=5)
        self.entry_siann = tk.Entry(root)
        self.entry_siann.grid(row=2, column=1, padx=5, pady=5)

        # 搜尋按鈕
        self.search_button = tk.Button(root, text="搜尋", command=self.search_hanzi)
        self.search_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # 候選字列表
        self.result_frame = ttk.Frame(root)
        self.result_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.result_list = tk.Listbox(self.result_frame, height=5, width=30)
        self.result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 捲動條
        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result_list.yview)

        # 空白鍵輸出選擇的漢字
        self.root.bind("<space>", self.select_hanzi)
        # Enter 鍵輸出羅馬拼音
        self.root.bind("<Return>", self.output_pinyin)
        # Shift+Enter 鍵輸出十五音標音
        self.root.bind("<Shift-Return>", self.output_taiwanese_phonetic)

    def search_hanzi(self):
        yunmu = self.entry_yunmu.get().strip()
        diao = self.entry_diao.get().strip()
        siann = self.entry_siann.get().strip()

        results = search_hanzi(yunmu, diao, siann)

        self.result_list.delete(0, tk.END)
        if results.empty:
            self.result_list.insert(tk.END, "❌ 找不到符合條件的漢字")
        else:
            for index, row in results.iterrows():
                self.result_list.insert(tk.END, f"{row['漢字']} ({row['十五音標音']})")

    def select_hanzi(self, event):
        try:
            selected_index = self.result_list.curselection()[0]
            selected_text = self.result_list.get(selected_index)
            selected_hanzi = selected_text.split()[0]
            print(f"輸出漢字: {selected_hanzi}")
        except IndexError:
            pass

    def output_pinyin(self, event):
        try:
            selected_index = self.result_list.curselection()[0]
            selected_text = self.result_list.get(selected_index)
            selected_hanzi = selected_text.split()[0]
            print(f"輸出羅馬拼音: {selected_hanzi}")
        except IndexError:
            pass

    def output_taiwanese_phonetic(self, event):
        try:
            selected_index = self.result_list.curselection()[0]
            selected_text = self.result_list.get(selected_index)
            selected_hanzi = selected_text.split()[0]
            print(f"輸出十五音標音: {selected_hanzi}")
        except IndexError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MinnanInputGUI(root)
    root.mainloop()
