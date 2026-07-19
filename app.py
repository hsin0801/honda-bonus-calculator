import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="2026年7月 Honda 銷售條件試算",
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
.note2-box {
    background: #fff8e1;
    border: 1px solid #ffcc02;
    border-radius: 10px;
    padding: 12px 16px;
    margin: 8px 0 4px 0;
    font-size: 13px;
    color: #7a5400;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題 ─────────────────────────────────────────────
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年7月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵 ＋ 備註1車險獎勵　｜　領牌期間 2026/07/01–07/31</p>
</div>
""", unsafe_allow_html=True)

# ── 篩選器 ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        ["1～3 台", "4 台以上"],
        horizontal=True,
        index=1
    )
    hrv_option = st.radio(
        "③ 本月有無販售 HR-V（HTW）",
        ["有 HR-V", "無 HR-V"],
        horizontal=True
    )

with col2:
    total_sales = st.radio(
        "② 本月全車系總銷售台數（HTW，不含CR-V）",
        ["1台", "2台", "3台", "4台以上"],
        horizontal=True,
        index=3
    )
    note1_option = st.radio(
        "④ 上月首年車體續保率（備註1）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無續保（一年以下）→ +5,000"]
    )

# ── 備註2 ────────────────────────────────────────────────
note2_on = st.toggle(
    "⑤ 備註2：本月現訂交 2 台 CR-V（HR-V 內促改以 3.5% 牌價 ＋ 備註1 計算）",
    value=False
)

if note2_on:
    st.markdown('<div class="note2-box">⚠️ 備註2 啟動：HR-V 內促將改為 <strong>3.5% × 牌價（無條件刪去到百位數）＋ 備註1</strong>，請輸入各 HR-V 車型當月成交牌價（新台幣）</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        price_s     = st.number_input("HR-V S 牌價", min_value=0, value=899000, step=1000, format="%d")
    with pc2:
        price_hev_s = st.number_input("HR-V e:HEV S 牌價", min_value=0, value=1009000, step=1000, format="%d")
    with pc3:
        price_hev_p = st.number_input("HR-V e:HEV P 牌價", min_value=0, value=1069000, step=1000, format="%d")
else:
    price_s = price_hev_s = price_hev_p = 0

# ── 計算邏輯 ─────────────────────────────────────────────
htw_table = {
    "有 HR-V":  {"1台":5000,"2台":6000,"3台":7000,"4台以上":8000},
    "無 HR-V":  {"1台":3000,"2台":4000,"3台":5000,"4台以上":6000},
}
htw = htw_table[hrv_option][total_sales]

note1_map = {
    "60% 以上 → +7,000": 7000,
    "低於 60% → +3,000": 3000,
    "無續保（一年以下）→ +5,000": 5000,
}
note1 = note1_map[note1_option]
is_high = (tier == "4 台以上")

def floor100(val):
    """無條件刪去到百位數"""
    return math.floor(val / 100) * 100

# HR-V 備註2 內促含備注1合計
hrv_note2_amounts = {
    "S":       (floor100(price_s     * 0.035) + note1) if note2_on else None,
    "e:HEV S": (floor100(price_hev_s * 0.035) + note1) if note2_on else None,
    "e:HEV P": (floor100(price_hev_p * 0.035) + note1) if note2_on else None,
}

# car_data：no_htw=True 表示不計入HTW且不發HTW獎勵（CR-V）
car_data = [
    {"section":"CIVIC", "model":"e:HEV 26'式樣", "nL":31000,"nH":39000,"sp":0,    "sp_note":"無現金",           "no_htw":False,"hrv":False},
    {"section":"HR-V",  "model":"S",              "nL":17000,"nH":20000,"sp":16000,"sp_note":"E案",             "no_htw":False,"hrv":True},
    {"section":"HR-V",  "model":"e:HEV S",        "nL":20000,"nH":23000,"sp":21000,"sp_note":"E案",             "no_htw":False,"hrv":True},
    {"section":"HR-V",  "model":"e:HEV P",        "nL":22000,"nH":25000,"sp":21000,"sp_note":"E案",             "no_htw":False,"hrv":True},
    {"section":"FIT",   "model":"Home",            "nL":39000,"nH":39000,"sp":11000,"sp_note":"D案",             "no_htw":False,"hrv":False},
    {"section":"FIT",   "model":"e:HEV",           "nL":43000,"nH":43000,"sp":21000,"sp_note":"D案",             "no_htw":False,"hrv":False},
    {"section":"CR-V",  "model":"ALL（各車型）",   "nL":12000,"nH":15000,"sp":0,    "sp_note":"延長保固（無現金）","no_htw":True, "hrv":False},
]

totals, rows = [], []
for car in car_data:
    neicu_base = car["nH"] if is_high else car["nL"]
    sp         = car["sp"]
    htw_val    = 0 if car["no_htw"] else htw

    is_hrv       = car.get("hrv", False)
    note2_amount = hrv_note2_amounts.get(car["model"]) if is_hrv else None

    if note2_on and is_hrv and note2_amount is not None:
        # 備注2：HR-V 內促已含備注1，不再另加
        note1_val    = 0
        neicu_label  = f"${note2_amount:,}（3.5%+備1）"
        note1_label  = "（含於內促）"
        total        = note2_amount + sp + htw_val
    else:
        note1_val    = note1
        neicu_label  = f"${neicu_base:,}"
        note1_label  = f"+${note1:,}"
        total        = neicu_base + sp + htw_val + note1

    totals.append(total)

    sp_display  = f"${sp:,}（{car['sp_note']}）" if sp > 0 else f"$0（{car['sp_note']}）"
    htw_display = "—（不計）" if car["no_htw"] else f"${htw_val:,}"

    rows.append({
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            neicu_label,
        "SP最高現金":      sp_display,
        "HTW獎勵":         htw_display,
        "備註1":           note1_label,
        "每台合計（最高）": f"${total:,}",
        "_total":          total,
    })

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片 ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">HTW 每台單獎</div>
    <div class="m-value">${htw:,}</div>
    <div class="m-sub">{total_sales} × {hrv_option}</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{'60%以上' if note1==7000 else '低於60%' if note1==3000 else '無續保'}</div>
  </div>
  <div class="metric-card best">
    <div class="m-label">🏆 本月最高獎金車型</div>
    <div class="m-value">${max_total:,}</div>
    <div class="m-sub">{max_car['section']} {max_car['model']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 明細表格 ─────────────────────────────────────────────
st.markdown('<div class="section-label">各車型每台獎金明細</div>', unsafe_allow_html=True)

df = pd.DataFrame(rows).drop(columns=["_total"])

def style_table(df_in):
    def row_style(row):
        total_str = row["每台合計（最高）"].replace("$","").replace(",","")
        if int(total_str) == max_total:
            return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        return [""] * len(row)
    return df_in.style.apply(row_style, axis=1)

st.dataframe(
    style_table(df),
    use_container_width=True,
    hide_index=True,
    height=300
)

# ── 計算式展開 ────────────────────────────────────────────
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu_base = car["nH"] if is_high else car["nL"]
        htw_val    = 0 if car["no_htw"] else htw
        htw_str    = "HTW不計" if car["no_htw"] else f"HTW ${htw_val:,}"
        color      = "#cc0000" if total == max_total else "#333"
        bold       = "700" if total == max_total else "400"

        is_hrv       = car.get("hrv", False)
        note2_amount = hrv_note2_amounts.get(car["model"]) if is_hrv else None

        if note2_on and is_hrv and note2_amount is not None:
            formula = (
                f"內促(3.5%+備1) ${note2_amount:,} "
                f"[牌價×3.5%↓百位 ＋ 備1 ${note1:,}] "
                f"＋ SP ${car['sp']:,} ＋ {htw_str}"
            )
        else:
            formula = (
                f"內促 ${neicu_base:,} ＋ SP ${car['sp']:,} ＋ {htw_str} ＋ 備註1 ${note1:,}"
            )

        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　"
            f"{formula} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金選項（E案/D案）。CIVIC SP本月無現金。CR-V SP為延長保固（無現金）。")
st.caption("※ CR-V 不計入HTW銷售台數，CR-V單台不發放HTW獎勵。")
st.caption("※ 備註1為新車投保乙式＋代步金險之獎勵，每台適用（取2026年6月成績）。")
st.caption("※ 備註2：本月現訂交2台CR-V達成，HR-V 內促改以 3.5% 牌價（無條件刪去到百位數）＋ 備註1 計算。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
