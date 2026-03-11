# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案定位

本專案為**十五音輸入法（Sip-Ngoo-Im）**，以 RIME 中州韻輸入法引擎為平台，提供閩南語（台語）漢字輸入支援。支援三種輸入體系：
- **拼音輸入法**：台語音標（TLPA）羅馬拼音
- **注音輸入法**：台灣方音符號（BPMF 變體）
- **反切輸入法**：十五音聲韻母體系

## 部署指令

```powershell
# 部署至 RIME 使用者目錄並重啟 (Windows Weasel)
powershell -File .\redeploy_rime.ps1

# 僅重啟 RIME 服務
.\tools\restart_rime_service.bat

# 清除 RIME 快取
.\tools\clear_rime_cache.bat
```

RIME 使用者目錄（Windows）：`%APPDATA%\Rime`

修改方案後必須執行部署腳本並重啟 RIME 服務才能驗證。

## 核心架構

```
*.schema.yaml          # RIME 輸入方案（主要配置入口）
*.dict.yaml            # 漢字字典（拼音對映漢字）
lib_*.yaml             # 共用 YAML 模組（被 schema 引用）
keymap_piau_tian.yaml  # 標點符號鍵盤映射
rime.lua               # Lua 擴充主入口
lua/                   # Lua 擴充模組
tools/                 # 字典轉換與輔助 Python 工具
src/                   # 音標轉換腳本（TLPA→BP/MPS2 等）
```

### 主要方案檔

| 檔案 | 說明 |
|------|------|
| `sgi_ping_im.schema.yaml` | 拼音輸入法（TLPA 羅馬字） |
| `sgi_zu_im.schema.yaml` | 注音輸入法（方音符號） |
| `kb_hong_im.schema.yaml` | 方音符號鍵盤配置 |
| `kb_ipa.schema.yaml` | IPA 鍵盤配置 |

### 字典檔

- `tl_han_ji_khoo.dict.yaml`：主字庫（大型，勿直接手動編輯）
- `tl_ji_khoo_ciann_ji.dict.yaml`：正字字庫
- `tl_ji_khoo_kah_kut_bun.dict.yaml`：甲骨文字庫
- `tl_ji_khoo_zu_ting.dict.yaml`：注頂字庫

### lib_*.yaml 模組

各 `lib_` 模組定義共用規則，供 schema 以 `__append` 方式引用：
- `lib_sip_ngoo_im.yaml`：十五音聲韻母轉換規則、聲調鍵映射、preedit 顯示格式
- `lib_phing_im.yaml`：拼音規則
- `lib_zu_im.yaml`：方音符號規則
- `lib_hau_suan_ji_tuann.yaml`：候選字詞處理

### Lua 模組

`rime.lua` 為主入口，`lua/` 下各模組提供動態邏輯（如 `sip_ngoo_im.lua`、`piau_im.lua`、`lian_sua_pa_ji.lua` 等），修改時需考慮 Windows/macOS/Linux 跨平台相容性。

## 字典維護規則

修改字典前，先檢查 `tools/` 是否有對應的 Python 腳本：

```powershell
# 字典轉換工具範例
python tools/convert_tlpa_to_mps2_for_rime_dict.py
python tools/convert_tlpa_to_bp_for_rime_dict.py
```

優先修改 Excel 資料源（`tools/tlpa_ji_khoo.xlsx`）或執行轉換腳本，而非直接編輯 `.dict.yaml`。

## 開發規範

1. **YAML 縮排**：Rime 的 YAML 對縮排極為敏感，必須保持原有風格（2 空格）。
2. **檔案編碼**：所有 `.yaml`、`.dict.yaml`、`.lua` 必須使用 **UTF-8（無 BOM）**。
3. **註解保留**：嚴禁刪除或簡化原有註解，其中包含 Rime 特性記錄、已知坑洞及版本相容性說明。
4. **版本控制**：不得提交 `build/` 目錄或 Rime 部署產生的二進位快取（`*.bin`）。
5. **封存目錄**：未經確認不得修改 `_archived/` 內的任何檔案。
