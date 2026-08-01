import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026年8月 Honda 銷售條件試算",
    page_icon="🚗",
    layout="centered"
)

st.markdown("""
<style>
.stApp { background-color: #f7f7f7; }
.honda-header {
    background: linear-gradient(135deg, #cc0000 0%, #990000 100%);
    color: white;
    padding: 20px 28px 16px 28px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.honda-header h1 { color: white; font-size: 22px; font-weight: 700; margin: 0 0 4px 0; }
.honda-header p  { color: rgba(255,255,255,0.8); font-size: 12px; margin: 0; }
.metric-row { display: flex; gap: 12px; margin: 16px 0; }
.metric-card {
    flex: 1;
    background: white;
    border-radius: 12px;
    padding: 14px 16px;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-card .m-label { font-size: 11px; color: #999; margin-bottom: 6px; }
.metric-card .m-value { font-size: 22px; font-weight: 700; color: #cc0000; }
.metric-card .m-sub   { font-size: 11px; color: #aaa; margin-top: 3px; }
.metric-card.best { border-color: #cc0000; background: #fff8f8; }
.section-label {
    font-size: 13px;
    font-weight: 700;
    color: #333;
    margin: 16px 0 8px 0;
    padding-left: 10px;
    border-left: 3px solid #cc0000;
}
.warn-box {
    background: #fff8e1;
    border: 1px solid #ffcc02;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0 4px 0;
    font-size: 13px;
    color: #7a5400;
}
.danger-box {
    background: #fff0f0;
    border: 1px solid #ffb3b3;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0 4px 0;
    font-size: 13px;
    color: #990000;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年8月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵（103期）＋ 備註1車險獎勵　｜　領牌期間 2026/08/01–08/31</p>
</div>
""", unsafe_allow_html=True)

# ── 篩選器
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        ["1～2 台", "3 台以上"],
        horizontal=True,
        index=1
    )
    period = st.radio(
        "② 領牌時段（HTW 103期）",
        ["8/3～8/14", "8/17～8/31"],
        horizontal=True
    )

with col2:
    total_sales = st.radio(
        "③ TTL領牌台數（HTW，不含PRELUDE）",
        ["1台", "2台", "3台以上"],
        horizontal=True,
        index=2
    )
    note1_option = st.radio(
        "④ 上月首年車體續保率（備註1）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無母數（一年以下）→ +5,000", "無母數（一年以上）→ +3,000"]
    )

# ── 備註等級
note_level = st.radio(
    "⑤ 備註等級（8/14前現訂交達成台數）",
    ["無", "備2：達2台（HR-V +2k｜CR-V e:HEV +3k）", "備3：達3台（HR-V +3k｜CR-V e:HEV +6k）",
     "備4：達4台（HR-V +3k｜CR-V e:HEV +10k）", "備5：達5台（HR-V +3k｜CR-V e:HEV +10k）"],
    horizontal=False
)

# ── 警告訊息
if period == "8/17～8/31":
    st.markdown('<div class="danger-box">⚠️ 8/17～8/31 領牌期間 HTW 無獎勵金（103期規定）</div>', unsafe_allow_html=True)

st.markdown('<div class="warn-box">⚠️ CR-V e:HEV P 限8月前庫存，需8/31前領牌</div>', unsafe_allow_html=True)

# ── 計算邏輯
HTW_TABLE = {
    "8/3～8/14":  {"1台": 4000, "2台": 5000, "3台以上": 6000},
    "8/17～8/31": {"1台": 0,    "2台": 0,    "3台以上": 0},
}
htw = HTW_TABLE[period][total_sales]

note1_map = {
    "60% 以上 → +7,000":         7000,
    "低於 60% → +3,000":         3000,
    "無母數（一年以下）→ +5,000": 5000,
    "無母數（一年以上）→ +3,000": 3000,
}
note1 = note1_map[note1_option]
is_high = (tier == "3 台以上")

HRV_BONUS = {"無": 0, "備2：達2台（HR-V +2k｜CR-V e:HEV +3k）": 2000,
             "備3：達3台（HR-V +3k｜CR-V e:HEV +6k）": 3000,
             "備4：達4台（HR-V +3k｜CR-V e:HEV +10k）": 3000,
             "備5：達5台（HR-V +3k｜CR-V e:HEV +10k）": 3000}
CRV_BONUS = {"無": 0, "備2：達2台（HR-V +2k｜CR-V e:HEV +3k）": 3000,
             "備3：達3台（HR-V +3k｜CR-V e:HEV +6k）": 6000,
             "備4：達4台（HR-V +3k｜CR-V e:HEV +10k）": 10000,
             "備5：達5台（HR-V +3k｜CR-V e:HEV +10k）": 10000}

hrv_bonus = HRV_BONUS[note_level]
crv_bonus = CRV_BONUS[note_level]

# car_data: no_htw=True → CR-V不計HTW；hrv=True → 適用HR-V備註加成；crv=True → 適用CR-V備註加成；crv_p=True → 限庫存標示
car_data = [
    {"section": "CIVIC", "model": "e:HEV 26'式樣",   "nL": 31000, "nH": 39000, "sp": 0,     "sp_note": "無現金",    "no_htw": False, "hrv": False, "crv": False, "crv_p": False},
    {"section": "HR-V",  "model": "S",               "nL": 19000, "nH": 22000, "sp": 14000, "sp_note": "G案",      "no_htw": False, "hrv": True,  "crv": False, "crv_p": False},
    {"section": "HR-V",  "model": "e:HEV S",         "nL": 23000, "nH": 26000, "sp": 19000, "sp_note": "G案",      "no_htw": False, "hrv": True,  "crv": False, "crv_p": False},
    {"section": "HR-V",  "model": "e:HEV P",         "nL": 25000, "nH": 28000, "sp": 19000, "sp_note": "G案",      "no_htw": False, "hrv": True,  "crv": False, "crv_p": False},
    {"section": "FIT",   "model": "Home",            "nL": 39000, "nH": 39000, "sp": 9000,  "sp_note": "D案",      "no_htw": False, "hrv": False, "crv": False, "crv_p": False},
    {"section": "FIT",   "model": "e:HEV",           "nL": 43000, "nH": 43000, "sp": 19000, "sp_note": "D案",      "no_htw": False, "hrv": False, "crv": False, "crv_p": False},
    {"section": "CR-V",  "model": "e:HEV S",         "nL": 12000, "nH": 15000, "sp": 0,     "sp_note": "延長保固", "no_htw": True,  "hrv": False, "crv": True,  "crv_p": False},
    {"section": "CR-V",  "model": "VTi-S / S",       "nL": 12000, "nH": 15000, "sp": 0,     "sp_note": "延長保固", "no_htw": True,  "hrv": False, "crv": False, "crv_p": False},
    {"section": "CR-V",  "model": "e:HEV P ⚠️限庫存", "nL": 12000, "nH": 15000, "sp": 0,     "sp_note": "延長保固", "no_htw": True,  "hrv": False, "crv": True,  "crv_p": True},
]

totals, rows = [], []
show_bonus = note_level != "無"

for car in car_data:
    neicu_base = car["nH"] if is_high else car["nL"]
    htw_val    = 0 if car["no_htw"] else htw
    hb_val     = hrv_bonus if car["hrv"] else 0
    cb_val     = crv_bonus if car["crv"] else 0
    bonus_val  = hb_val + cb_val
    total      = neicu_base + car["sp"] + htw_val + note1 + bonus_val
    totals.append(total)

    sp_display    = f"${car['sp']:,}（{car['sp_note']}）" if car["sp"] > 0 else f"$0（{car['sp_note']}）"
    htw_display   = "—（不計）" if car["no_htw"] else f"${htw_val:,}"
    bonus_display = f"+${bonus_val:,}" if bonus_val > 0 else "—"

    row_dict = {
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            f"${neicu_base:,}",
        "SP最高現金":      sp_display,
        "HTW獎勵":         htw_display,
        "備註1":           f"+${note1:,}",
        "每台合計（最高）": f"${total:,}",
        "_total":          total,
    }
    if show_bonus:
        row_dict["備註加成"] = bonus_display
    rows.append(row_dict)

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片
htw_sub = "8/3~8/14" if period == "8/3～8/14" else "8/17後無獎勵"
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">HTW 每台單獎</div>
    <div class="m-value">${htw:,}</div>
    <div class="m-sub">{htw_sub} × {total_sales}</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{'60%以上' if note1==7000 else '低於60%' if note1==3000 and '低於' in note1_option else '無母數一年以下' if '一年以下' in note1_option else '無母數一年以上'}</div>
  </div>
  <div class="metric-card best">
    <div class="m-label">🏆 本月最高獎金車型</div>
    <div class="m-value">${max_total:,}</div>
    <div class="m-sub">{max_car['section']} {max_car['model']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 明細表格
st.markdown('<div class="section-label">各車型每台獎金明細</div>', unsafe_allow_html=True)

col_order = ["車系", "車型", "內促", "SP最高現金", "HTW獎勵", "備註1"]
if show_bonus:
    col_order.append("備註加成")
col_order.append("每台合計（最高）")

df = pd.DataFrame(rows)[col_order]

def style_table(df_in):
    def row_style(row):
        total_str = row["每台合計（最高）"].replace("$", "").replace(",", "")
        if int(total_str) == max_total:
            return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        return [""] * len(row)
    return df_in.style.apply(row_style, axis=1)

st.dataframe(
    style_table(df),
    use_container_width=True,
    hide_index=True,
    height=330
)

# ── 計算式展開
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu_base = car["nH"] if is_high else car["nL"]
        htw_val    = 0 if car["no_htw"] else htw
        htw_str    = "HTW不計" if car["no_htw"] else f"HTW ${htw_val:,}"
        hb_val     = hrv_bonus if car["hrv"] else 0
        cb_val     = crv_bonus if car["crv"] else 0
        bonus_val  = hb_val + cb_val
        color = "#cc0000" if total == max_total else "#333"
        bold  = "700" if total == max_total else "400"
        bonus_str = f" ＋ 備註加成 ${bonus_val:,}" if bonus_val > 0 else ""
        formula = (
            f"內促 ${neicu_base:,} ＋ SP ${car['sp']:,} ＋ {htw_str} ＋ 備1 ${note1:,}{bonus_str}"
        )
        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　{formula} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金選項（G案最高：HR-V S=$14k，HR-V e:HEV=$19k，FIT Home=$9k，FIT e:HEV=$19k）。")
st.caption("※ CIVIC SP本月無現金。CR-V SP為延長保固（無現金）。")
st.caption("※ CR-V 不計入TTL台數，CR-V單台不發放HTW獎勵。PRELUDE不計入TTL台數。")
st.caption("※ 備2～5加成疊加於基礎內促之上；備4與備5 CR-V e:HEV加成相同（+10k）。")
st.caption("※ CR-V e:HEV P 限8月前庫存，需8/31前領牌。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
