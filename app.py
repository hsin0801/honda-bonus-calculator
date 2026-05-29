import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026年6月 Honda 銷售條件試算",
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
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題 ─────────────────────────────────────────────
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年6月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵 ＋ 備註1車險獎勵　｜　領牌期間 2026/06/01–06/30</p>
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

note3_on = st.radio(
    "⑤ 本月現訂交台數（備註3：達4台以上，各車型加給獎勵）",
    ["達4台以上（加給）", "未達4台（不加給）"],
    horizontal=True
)

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
note3_active = (note3_on == "達4台以上（加給）")

# no_htw=True 表示該車型不計入HTW（CR-V）
# note3: 備註3各車型換算金額
car_data = [
    {"section":"CIVIC", "model":"e:HEV 26'式樣", "nL":31000,"nH":39000,"sp":0,    "sp_note":"無（A案）/ 延長保固（B案）","no_htw":False,"note3":5000},
    {"section":"HR-V",  "model":"S",              "nL":13000,"nH":15000,"sp":17000,"sp_note":"","no_htw":False,"note3":2000},
    {"section":"HR-V",  "model":"e:HEV S",        "nL":15000,"nH":18000,"sp":22000,"sp_note":"","no_htw":False,"note3":2000},
    {"section":"HR-V",  "model":"e:HEV P",        "nL":17000,"nH":20000,"sp":22000,"sp_note":"","no_htw":False,"note3":2000},
    {"section":"FIT",   "model":"Home",            "nL":39000,"nH":39000,"sp":12000,"sp_note":"","no_htw":False,"note3":2000},
    {"section":"FIT",   "model":"e:HEV",           "nL":43000,"nH":43000,"sp":22000,"sp_note":"","no_htw":False,"note3":2000},
    {"section":"CR-V",  "model":"ALL（各車型）",   "nL":12000,"nH":15000,"sp":0,    "sp_note":"延長保固（無現金）","no_htw":True,"note3":1000},
]

totals, rows = [], []
for car in car_data:
    neicu   = car["nH"] if is_high else car["nL"]
    sp      = car["sp"]
    htw_val = 0 if car["no_htw"] else htw
    n3_val  = car["note3"] if note3_active else 0
    total   = neicu + sp + htw_val + note1 + n3_val

    totals.append(total)
    sp_display  = f"${sp:,}" if sp > 0 else f"$0（{car['sp_note']}）"
    htw_display = "—（不計）" if car["no_htw"] else f"${htw_val:,}"
    n3_display  = f"+${n3_val:,}" if note3_active else "—"

    rows.append({
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            f"${neicu:,}",
        "SP最高現金":      sp_display,
        "HTW獎勵":         htw_display,
        "備註1":           f"+${note1:,}",
        "備註3":           n3_display,
        "每台合計（最高）": f"${total:,}",
        "_total":          total,
    })

# 最高獎金（排除CR-V計算HTW為0的影響，找真正最高的）
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
        neicu   = car["nH"] if is_high else car["nL"]
        htw_val = 0 if car["no_htw"] else htw
        htw_str = "HTW不計" if car["no_htw"] else f"HTW ${htw_val:,}"
        color   = "#cc0000" if total == max_total else "#333"
        bold    = "700" if total == max_total else "400"
        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　"
            f"內促 ${neicu:,} ＋ SP ${car['sp']:,} ＋ {htw_str} ＋ 備註1 ${note1:,} ＋ 備註3 ${car['note3'] if note3_active else 0:,} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金選項（D案）。CIVIC SP本月無現金。CR-V SP為延長保固（無現金）。")
st.caption("※ CR-V 不計入HTW銷售台數，CR-V單台不發放HTW獎勵。")
st.caption("※ 備註1為新車投保乙式＋代步金險之獎勵，每台適用。")
st.caption("※ 備註2：6/1-6/14銷售各機型以第4台內促計算。")
st.caption("※ 備註3：現訂交4台以上發放，CR-V $1,000／HR-V $2,000／FIT $2,000／CIVIC $5,000 每台。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
