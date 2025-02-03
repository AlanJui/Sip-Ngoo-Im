import json

# 加載韻書數據
with open('韻書.json', 'r', encoding='utf-8') as f:
    un_ceh_data = json.load(f)

def find_characters_by_rhyme(un_bu):
    for entry in un_ceh_data['韻母']:
        if entry['韻'] == un_bu:
            return entry['字']
    return []

# 示例：查找韻母為 "a" 的字
un_bu = "a"
characters = find_characters_by_rhyme(un_bu)
print(f"韻母為 {un_bu} 的字有：{characters}")