import tkinter as tk
from tkinter import ttk

import pandas as pd

# 韻母對照表（不區分舒聲、促聲）
un_mu_dict = {
    "un": "君", "ut": "君", "ian": "堅", "iat": "堅", "im": "金", "ip": "金",
    "ui": "規", "ee": "嘉", "eeh": "嘉", "an": "干", "at": "干", "ong": "公",
    "ok": "公", "uai": "乖", "uaih": "乖", "ing": "經", "ik": "經", "uan": "觀",
    "uat": "觀", "oo": "沽", "iau": "嬌", "iauh": "嬌", "ei": "稽", "iong": "恭",
    "iok": "恭", "o": "高", "oh": "高", "ai": "皆", "in": "巾", "it": "巾",
    "iang": "姜", "iak": "姜", "am": "甘", "ap": "甘", "ua": "瓜", "uah": "瓜",
    "ang": "江", "ak": "江", "iam": "兼", "iap": "兼", "au": "交", "auh": "交",
    "ia": "迦", "iah": "迦", "ue": "檜", "ueh": "檜", "ann": "監", "ahnn": "監",
    "u": "艍", "uh": "艍", "a": "膠", "ah": "膠", "i": "居", "ih": "居",
    "iu": "丩", "enn": "更", "ehnn": "更", "uinn": "褌", "io": "茄", "ioh": "茄",
    "inn": "梔", "ihnn": "梔", "ionn": "薑", "iann": "驚", "uann": "官", "ng": "鋼",
    "e": "伽", "eh": "伽", "ainn": "閒", "oonn": "姑", "m": "姆", "uang": "光",
    "uak": "光", "uainn": "閂", "uaihnn": "閂", "uenn": "糜", "iaunn": "嘄",
    "iauhnn": "嘄", "om": "箴", "op": "箴", "aunn": "爻", "onn": "扛", "ohnn": "扛",
    "iunn": "牛"
}

# 韻母的傳統排序
traditional_order = [
    "君", "堅", "金", "規", "嘉", "干", "公", "乖", "經", "觀",
    "沽", "嬌", "稽", "恭", "高", "皆", "巾", "姜", "甘", "瓜",
    "江", "兼", "交", "迦", "檜", "監", "艍", "膠", "居", "丩",
    "更", "褌", "茄", "梔", "薑", "驚", "官", "鋼", "伽", "閒",
    "姑", "姆", "光", "閂", "糜", "嘄", "箴", "爻", "扛", "牛"
]

# 只顯示獨特的韻母名稱，並按照傳統排序
un_mu_list = sorted(set(un_mu_dict.values()), key=lambda x: traditional_order.index(x))

# 聲調對照表
tiau_dict = {
    "1": "一（陰平）", "2": "二（上声）", "3": "三（陰去）", "4": "四（陰入）",
    "5": "五（陽平）", "6": "六（上声）", "7": "七（陽去）", "8": "八（陽入）",
}

# 聲母對照表
siann_dict = {
    "l": "柳", "n": "耐", "p": "邊", "k": "求", "kh": "去", "t": "地",
    "ph": "頗", "th": "他", "z": "曾", "j": "入", "s": "時", "q": "英",
    "b": "門", "m": "毛", "g": "語", "ng": "雅", "c": "出", "h": "喜"
}
siann_list = list(siann_dict.values())

# 讀取 Excel 字典
file_path = "D100_彙集雅俗通十五音字典.xlsx"
df_dict = pd.read_excel(file_path, sheet_name="彙集雅俗通字典")

class SipNgooIm:
    def __init__(self, root):
        self.root = root
        self.root.title("閩南話輸入法 (河洛白話)")
        self.root.geometry("600x500")

        font_style = ("Helvetica", 18)

        # 韻母
        tk.Label(root, text="韻母:", font=font_style).grid(row=0, column=0, padx=5, pady=5)
        self.un_var = tk.StringVar()
        self.combo_un_mu = ttk.Combobox(root, textvariable=self.un_var, font=font_style, state="normal")
        self.combo_un_mu['values'] = un_mu_list
        self.combo_un_mu.grid(row=0, column=1, padx=5, pady=5)

        # 聲調
        tk.Label(root, text="聲調:", font=font_style).grid(row=1, column=0, padx=5, pady=5)
        self.tiau_var = tk.StringVar()
        self.combo_tiau = ttk.Combobox(root, textvariable=self.tiau_var, font=font_style, state="normal")
        self.combo_tiau['values'] = list(tiau_dict.values())
        self.combo_tiau.grid(row=1, column=1, padx=5, pady=5)

        # 聲母
        tk.Label(root, text="聲母:", font=font_style).grid(row=2, column=0, padx=5, pady=5)
        self.siann_var = tk.StringVar()
        self.combo_siann = ttk.Combobox(root, textvariable=self.siann_var, font=font_style, state="normal")
        self.combo_siann['values'] = siann_list
        self.combo_siann.grid(row=2, column=1, padx=5, pady=5)

        # 搜尋按鈕
        tk.Button(root, text="搜尋", font=font_style, command=self.search_han_ji).grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # 候選字列表
        self.result_frame = ttk.Frame(root)
        self.result_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        self.result_list = tk.Listbox(self.result_frame, height=5, width=30, font=font_style)
        self.result_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.result_list.yview)

    def search_han_ji(self):
        """ 檢索符合條件的漢字 """
        un = self.un_var.get().strip()
        tiau = self.tiau_var.get().strip()
        siann = self.siann_var.get().strip()
        results = df_dict[
            (df_dict["韻"] == un) &
            (df_dict["調"].astype(str) == tiau) &
            (df_dict["聲"] == siann)
        ]
        self.result_list.delete(0, tk.END)
        if results.empty:
            self.result_list.insert(tk.END, "❌ 找不到符合條件的漢字")
        else:
            for _, row in results.iterrows():
                self.result_list.insert(tk.END, f"{row['漢字']} ({row['十五音標音']})")

if __name__ == "__main__":
    root = tk.Tk()
    app = SipNgooIm(root)
    root.mainloop()
