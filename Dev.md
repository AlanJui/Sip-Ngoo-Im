# 開發作業指引

## 啟用 Claude AI

啟動 Windows Terminal，切換到專案資料夾，輸入 `claude` 指令：

```bash
cd C:\work\Sip-Ngoo-Im
claude
```

Claude Code 會自動讀取 CLAUDE.md，直接進入專案情境。

後續可直接使用中文下達指令，例如：

- 檢視 sgi_zu_im.schema.yaml 的結構，說明目前的輸入方案設計
- 幫我在 tl_han_ji_khoo.dict.yaml 新增詞條
- 執行 redeploy_rime.ps1 並告訴我部署結果

## 要求 AI 理解專案情境

在 Clau在 CLI 的互動介面中，輸入以下指令：

```

請閱讀並分析本專案的輸入方案設計，說明：
1. 目前有哪些輸入方案（schema），各自的用途為何？
2. 字典（dict）的結構與內容概述
3. lib 模組的功能分工
4. Lua 擴充的主要功能
請用繁體中文回覆。
```

## 實用的起手式建議

進入 Claude Code 後，可以先說：

```
請閱讀 CLAUDE.md 與各 schema 檔案，告訴我目前輸入方案的設計邏輯，並建議可改善之處。

```

## 其它 AI 作業常用指令

- 進一步解讀設計邏輯
- 找出可改善之處
- 規劃後續開發方向

## Claude 所理解的專案情境

---

輸入方案設計分析

## 1. 輸入方案（Schema）

本專案目前有 4 個 Schema：

### sgi_ping_im（十五音輸入法【TLPA】）

拼音輸入法，使用者以台語音標（TLPA）羅馬字母輸入，輸入法在 preedit
列將按鍵即時轉換為十五音聲母（如 t → 地、k → 求）與韻母（如 ong →
公）。候選字視窗同時顯示【十五音反切】與【方音符號】兩欄標音。

聲調鍵位：

┌───────────┬──────┐
│ 調 │ 按鍵 │
├───────────┼──────┤
│ 1（陰平） │ ; │
├───────────┼──────┤
│ 7（陽去） │ - │
├───────────┼──────┤
│ 3（陰去） │ \_ │
├───────────┼──────┤
│ 2（上聲） │ \ │
├───────────┼──────┤
│ 5（陽平） │ / │
├───────────┼──────┤
│ 4（陰入） │ [ │
├───────────┼──────┤
│ 8（陽入） │ ] │
└───────────┴──────┘

### sgi_zu_im（十五音輸入法【注音反切】）

注音輸入法，使用者以方音符號按鍵輸入，內部透過極複雜的 algebra
規則（一對一鍵盤映射 xlit 共 60+
個符號）將按鍵轉換為台羅拼音編碼，再查字典。preedit 列顯示方音符號，候選字同時
呈現十五音反切。支援鼻化韻母多種輸入方式（重複輸入、前綴識別 N、縮寫符號 \*）。

### kb_hong_im（按鍵練習【方音符號】）

工具型方案，不具備漢字輸入能力，Engine 只掛 punctuator +
selector。用途是讓使用者透過按鍵輸出方音符號字元，供練習或測試用。

### kb_ipa（IPA 鍵盤）

類似 kb_hong_im，用於輸入 IPA 國際音標字元，同為工具/練習用途，不含字典翻譯。

---

## 2. 字典（Dict）結構

所有字典使用 TLPA 台羅拼音作為 code（音標），格式為：

漢字 <tab> 拼音 <tab> 常用度(weight) <tab> 用法 <tab> 建立時間

共有 4 個字典檔，形成階層引用關係：

tl_han_ji_khoo.dict.yaml ← 主字庫入口（import_tables 方式聚合）
└── tl_ji_khoo_peh_ue ← 河洛白話音（透過 import_tables 引入各子庫）
├── tl_ji_khoo_ciann_ji.dict.yaml ← 正字詞彙（含多音節詞、常用語）
├── tl_ji_khoo_kah_kut_bun.dict.yaml ← 甲骨文字庫
└── tl_ji_khoo_zu_ting.dict.yaml ← 注頂字庫（特殊漢字）

- weight 欄位控制候選字排序，值愈高愈優先（常見字 0.1，罕見字 0.01）
- sort: by_weight 依常用度排序候選字
- 主字庫禁止直接手動編輯，應透過 tools/ 的 Python 腳本從 Excel 產生

---

## 3. lib 模組的功能分工

各 lib\_\*.yaml 模組提供可被 schema 以 \_\_append 方式引用的共用規則區塊：

### 模組: lib_sip_ngoo_im.yaml

提供的區塊（key）:
phing_im_tng_ji_be、abbreviation、ji_be_tng_jih_kian、phah_ji_tng_uann
主要功能: 十五音核心：TLPA→十五音聲韻母對映、聲調按鍵對映、preedit
顯示轉換（漢字聲韻母）、縮寫規則
────────────────────────────────────────

### 模組: lib_phing_im.yaml

提供的區塊（key）: phing_im_tng_ji_be、abbreviation、ji_be_tng_jih_kian、Phing
\_Im_Iong_Tiau_Ho/Hu、jih_kian_tng_uann
主要功能: 拼音輸入通用：聲調鍵映射、preedit 以 TLPA 調號（數字）或調符（á â
ā）顯示、地方腔相容（漳州/泉州/廈門腔）
────────────────────────────────────────

### 模組: lib_zu_im.yaml

提供的區塊（key）: zu_im_hu_ho_pinn_be
主要功能: 注音輸入通用：台羅拼音→注音符號編碼的 algebra
規則、鼻化韻母多種格式處理
────────────────────────────────────────

### 模組: lib_hau_suan_ji_tuann.yaml

提供的區塊（key）: hau_suan_tuann
主要功能: 候選字清單格式化：雙欄顯示（左
TLPA、右方音符號），含連續輸入的音節拆解邏輯（零聲母自動補「英」、以
〔〕【】
框住標音）

---

## 4. Lua 擴充的主要功能

rime.lua 為主入口，定義了 5 個主要全域函式，各自對應 schema 中
lua_processor@、lua_filter@ 的掛載點：

### jump_select（lua_processor）

截攔 Ctrl+/、Ctrl+.、Ctrl+, 快捷鍵，讓使用者能快速將候選游標移到候選清單的第 1
/ 第 3 / 第 5 個選項；Ctrl+1~5 則直接選定並上屏。內部邏輯是先發 Page_Up
重置到頁首，再補送對應次數的 Down 鍵。

### aux_commit（lua_processor）

擴充 Enter 系列按鍵的輸出模式，允許將候選字以多種形式上屏：

- Space → 漢字
- Enter → TLPA 羅馬拼音字母（如 hu5）
- Ctrl+Enter → 方音符號（如 ㄏㄨˊ）
- Shift+Enter → 上標格式拼音（如 hu⁵）
- Ctrl+Shift+Enter → 完整雙欄格式（如 〔hu5〕【ㄏㄨˊ】）

### reformat_comment_filter（lua_filter）

過濾器，重新格式化候選字的
comment（標注欄），實現候選字視窗的雙欄標音顯示（左欄
TLPA、右欄方音符號），並依 dict_mode / tiau_mark 等 switch
狀態動態切換顯示格式。

### convert_15_to_roman（內部工具函式）

將「韻母漢字 + 聲調漢字 + 聲母漢字」（十五音反切格式，如「公七求」）解析並反查
sheng_mu_dict / yun_mu_dict 字典，還原成 TLPA 羅馬拼音字母（如 kong7）。

### apply_poj_tone_mark（內部工具函式）

將數字調號（如 hu5）轉換成 POJ/台羅調符（如 hû），依 a > e/oo/ee > e > o >
iu/ui > i > u > m > ng 的規則決定調符加在哪個元音上。
