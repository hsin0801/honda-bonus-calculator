import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026年5月 Honda 銷售條件試算",
    page_icon="🚗",
    layout="centered"
)

st.markdown("""
<style>
/* 整體背景 */
.stApp { background-color: #f7f7f7; }

/* 頂部 Honda 色條 */
.honda-header {
    background: linear-gradient(135deg, #cc0000 0%, #990000 100%);
    color: white;
    padding: 20px 28px 16px 28px;
    border-radius: 14px;
    margin-bottom: 20px;
}
.honda-header h1 { color: white; font-size: 22px; font-weight: 700; margin: 0 0 4px 0; }
.honda-header p  { color: rgba(255,255,255,0.8); font-size: 12px; margin: 0; }

/* 篩選器卡片 */
.filter-card {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.filter-title {
    font-size: 11px;
    font-weight: 600;
    color: #999;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* 指標卡片 */
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
.metric-card.best .m-value { color: #cc0000; }

/* 表格容器 */
.table-wrap {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    margin-top: 4px;
}

/* Streamlit radio 標籤 */
div[data-testid="stRadio"] label { font-size: 13px !important; }
div[data-testid="stRadio"] > div { gap: 6px; }

/* 分隔線 */
hr { border: none; border-top: 1px solid #ebebeb; margin: 16px 0; }

/* section 標題 */
.section-label {
    font-size: 13px;
    font-weight: 700;
    color: #333;
    margin: 16px 0 8px 0;
    padding-left: 10px;
    border-left: 3px solid #cc0000;
}

/* 隱藏 Streamlit 預設元素 */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題 ─────────────────────────────────────────────
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年5月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ DM銷售顧問獎勵 ＋ 備註1車險獎勵　｜　領牌期間 2026/05/01–05/31</p>
</div>
""", unsafe_allow_html=True)

# ── 篩選器 ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        ["1～2 台", "3 台以上"],
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
        "② 本月全車系總銷售台數（HTW）",
        ["1台", "2台", "3台", "4台以上"],
        horizontal=True,
        index=3
    )
    note1_option = st.radio(
        "④ 上月首年車體續保率（備註1）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無續保（一年以下）→ +5,000"]
    )

# ── 計算邏輯 ─────────────────────────────────────────────
dm_table = {
    "有 HR-V":  {"1台":5000,"2台":6000,"3台":7000,"4台以上":8000},
    "無 HR-V":  {"1台":3000,"2台":4000,"3台":5000,"4台以上":6000},
}
dm = dm_table[hrv_option][total_sales]

note1_map = {
    "60% 以上 → +7,000": 7000,
    "低於 60% → +3,000": 3000,
    "無續保（一年以下）→ +5,000": 5000,
}
note1 = note1_map[note1_option]
is_high = (tier == "3 台以上")

car_data = [
    {"section":"CIVIC", "model":"e:HEV 26'式樣", "nL":31000,"nH":39000,"sp":0,    "sp_note":"延長保固（無現金）"},
    {"section":"HR-V",  "model":"S",              "nL":12000,"nH":15000,"sp":25000,"sp_note":""},
    {"section":"HR-V",  "model":"e:HEV S",        "nL":14000,"nH":17000,"sp":30000,"sp_note":""},
    {"section":"HR-V",  "model":"e:HEV P",        "nL":16000,"nH":19000,"sp":30000,"sp_note":""},
    {"section":"FIT",   "model":"Home",            "nL":38000,"nH":38000,"sp":20000,"sp_note":""},
    {"section":"FIT",   "model":"e:HEV",           "nL":42000,"nH":42000,"sp":30000,"sp_note":""},
]

totals, rows = [], []
for car in car_data:
    neicu = car["nH"] if is_high else car["nL"]
    sp    = car["sp"]
    total = neicu + sp + dm + note1
    totals.append(total)
    sp_display = f"${sp:,}" if sp > 0 else f"$0（{car['sp_note']}）"
    rows.append({
        "車系": car["section"],
        "車型": car["model"],
        "內促": f"${neicu:,}",
        "SP最高現金": sp_display,
        "HTW獎勵": f"${dm:,}",
        "備註1": f"+${note1:,}",
        "每台合計（最高）": f"${total:,}",
        "_total": total,
    })

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片 ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">HTW 每台單獎</div>
    <div class="m-value">${dm:,}</div>
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

def style_table(df):
    def row_style(row):
        total_str = row["每台合計（最高）"].replace("$","").replace(",","")
        if int(total_str) == max_total:
            return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        if row["車系"] != (df["車系"].shift(1).iloc[df.index.get_loc(row.name)] if row.name > 0 else ""):
            return ["background-color:#fafafa"] * len(row)
        return [""] * len(row)
    return df.style.apply(row_style, axis=1)

st.dataframe(
    style_table(df),
    use_container_width=True,
    hide_index=True,
    height=280
)

# ── 計算式展開 ────────────────────────────────────────────
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu = car["nH"] if is_high else car["nL"]
        color = "#cc0000" if total == max_total else "#333"
        st.markdown(
            f"<span style='color:{color};font-weight:{'700' if total==max_total else '400'}'>"
            f"**{car['section']} {car['model']}**　"
            f"內促 ${neicu:,} ＋ SP ${car['sp']:,} ＋ HTW ${dm:,} ＋ 備註1 ${note1:,} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金選項（E/D案）。CIVIC SP僅延長保固（無現金支援金）。")
st.caption("※ 備註1為新車投保乙式＋代步金險之獎勵，每台適用。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
