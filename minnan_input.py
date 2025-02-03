import pandas as pd

# 讀取 Excel 文件
file_path = "D100_彙集雅俗通十五音字典.xlsx"
df_dict = pd.read_excel(file_path, sheet_name="彙集雅俗通字典")

def search_hanzi(yunmu: str, diao: str, siann: str, df=df_dict):
    """ 檢索符合條件的漢字 """
    results = df[(df["韻"] == yunmu) & (df["調"].astype(str) == diao) & (df["聲"] == siann)]
    return results[["漢字", "十五音標音"]].head(5)

def input_method_cli():
    """ 閩南話輸入法 CLI 版本 """
    print("=== 閩南話輸入法 (河洛白話) ===")
    print("輸入 'exit' 以退出。\n")

    while True:
        yunmu = input("請輸入【韻母】: ").strip()
        if yunmu.lower() == "exit":
            break

        diao = input("請輸入【聲調】: ").strip()
        if diao.lower() == "exit":
            break

        siann = input("請輸入【聲母】: ").strip()
        if siann.lower() == "exit":
            break

        results = search_hanzi(yunmu, diao, siann)

        if results.empty:
            print("❌ 找不到符合條件的漢字，請重新輸入。\n")
        else:
            print("\n✅ 候選字：")
            for index, row in results.iterrows():
                print(f"  {index + 1}. {row['漢字']} ({row['十五音標音']})")
            print("\n")

    print("輸入法已退出。")

if __name__ == "__main__":
    input_method_cli()
