import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026年10月 Honda 銷售條件試算",
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
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題
st.markdown("""
<div class="honda-header">
  <h1>🚗 2026年10月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵（103期）＋ 備註獎勵　｜　領牌期間 2026/10/01–10/31</p>
</div>
""", unsafe_allow_html=True)

# ── 篩選器
col1, col2 = st.columns(2)

with col1:
    tier = st.radio(
        "① 各車型銷售台數（內促門檻）",
        ["1～2 台", "3 台", "4 台以上"],
        horizontal=True,
        index=2
    )
    crv_hev_cnt = st.radio(
        "② 本月 CR-V e:HEV 領牌台數（HTW）",
        ["無", "1台", "2台以上"],
        horizontal=True,
        index=2
    )

with col2:
    total_sales = st.radio(
        "③ TTL領牌台數（HTW，不含PRELUDE）",
        ["1台", "2台", "3台", "4台以上"],
        horizontal=True,
        index=3
    )
    note1_option = st.radio(
        "④ 9月首年車體續保率（備註1）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無母數（一年以下）→ +5,000", "無母數（一年以上）→ +3,000"],
        index=0
    )

# ── 備2 / 備3 / 備4
note2_on = st.toggle(
    "⑤ 備2：10/11前完成2台訂單（10/31前領牌）→ 全車型內促直接以第4台計算",
    value=True
)
note3_on = st.toggle(
    "⑥ 備3：10月 ZR-V＋CR-V e:HEV 現訂交達3台 → ZR-V／CR-V e:HEV S +3,000、Prestige +4,000",
    value=True
)
note4_on = st.toggle(
    "⑦ 備4：10月現訂交達5台（不限機型，直販不計）→ 每台 +1,000，CR-V e:HEV ×2",
    value=True
)

# ── 計算邏輯
HTW_TABLE = {
    "無":     {"1台": 2000, "2台": 3000, "3台": 4000, "4台以上": 5000},
    "1台":    {"1台": 5000, "2台": 6000, "3台": 7000, "4台以上": 8000},
    "2台以上": {"1台": None, "2台": 8000, "3台": 9000, "4台以上": 10000},
}
htw = HTW_TABLE[crv_hev_cnt][total_sales]
if htw is None:
    st.markdown('<div class="warn-box">⚠️ CR-V e:HEV 2台以上時 TTL 至少2台，HTW 以2台（$8,000）計算</div>', unsafe_allow_html=True)
    htw = 8000

note1_map = {
    "60% 以上 → +7,000":         7000,
    "低於 60% → +3,000":         3000,
    "無母數（一年以下）→ +5,000": 5000,
    "無母數（一年以上）→ +3,000": 3000,
}
note1 = note1_map[note1_option]

tier_idx = 2 if note2_on else {"1～2 台": 0, "3 台": 1, "4 台以上": 2}[tier]

# car_data:
#   nL/nM/nH = 1~2台 / 3台 / 4台以上 內促
#   sp       = SP最高現金
#   n1_fix   = 備1固定金額（ZR-V 乙式 +3,000），None=依續保率
#   n3       = 備3每台加給
#   n4x      = 備4紅包倍數（CR-V e:HEV ×2）
car_data = [
    {"section": "ZR-V", "model": "e:HEV 26'式樣",      "nL": 10000, "nM": 10000, "nH": 15000, "sp": 0,     "sp_note": "視為0",       "n1_fix": 3000, "n3": 3000, "n4x": 1},
    {"section": "HR-V", "model": "S",                  "nL": 19000, "nM": 21000, "nH": 23000, "sp": 14000, "sp_note": "G案",         "n1_fix": None, "n3": 0,    "n4x": 1},
    {"section": "HR-V", "model": "e:HEV S",            "nL": 23000, "nM": 25000, "nH": 27000, "sp": 16000, "sp_note": "G案",         "n1_fix": None, "n3": 0,    "n4x": 1},
    {"section": "HR-V", "model": "e:HEV P",            "nL": 25000, "nM": 27000, "nH": 29000, "sp": 26000, "sp_note": "G案",         "n1_fix": None, "n3": 0,    "n4x": 1},
    {"section": "FIT",  "model": "Home",               "nL": 39000, "nM": 39000, "nH": 39000, "sp": 9000,  "sp_note": "C案",         "n1_fix": None, "n3": 0,    "n4x": 1},
    {"section": "FIT",  "model": "e:HEV",              "nL": 43000, "nM": 43000, "nH": 43000, "sp": 19000, "sp_note": "C案",         "n1_fix": None, "n3": 0,    "n4x": 1},
    {"section": "CR-V", "model": "e:HEV S",            "nL": 20000, "nM": 22000, "nH": 24000, "sp": 26000, "sp_note": "B案",         "n1_fix": None, "n3": 3000, "n4x": 2},
    {"section": "CR-V", "model": "e:HEV P (Prestige)", "nL": 20000, "nM": 22000, "nH": 24000, "sp": 18000, "sp_note": "B案",         "n1_fix": None, "n3": 4000, "n4x": 2},
    {"section": "CR-V", "model": "VTi-S / S",          "nL": 13000, "nM": 15000, "nH": 15000, "sp": 0,     "sp_note": "視為0", "n1_fix": None, "n3": 0, "n4x": 1},
]

def neicu(car):
    return [car["nL"], car["nM"], car["nH"]][tier_idx]

totals, rows = [], []
for car in car_data:
    neicu_val = neicu(car)
    n1_val    = car["n1_fix"] if car["n1_fix"] is not None else note1
    n3_val    = car["n3"] if note3_on else 0
    n4_val    = 1000 * car["n4x"] if note4_on else 0
    total     = neicu_val + car["sp"] + htw + n1_val + n3_val + n4_val
    totals.append(total)

    row = {
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            f"${neicu_val:,}" + ("（備2第4台）" if note2_on else ""),
        "SP最高現金":      f"${car['sp']:,}（{car['sp_note']}）",
        "HTW獎勵":         f"${htw:,}",
        "備註1":           f"+${n1_val:,}" + ("（ZR-V乙式）" if car["n1_fix"] is not None else ""),
        "每台合計（最高）": f"${total:,}",
    }
    if note3_on:
        row["備3"] = f"+${n3_val:,}" if n3_val else "—"
    if note4_on:
        row["備4紅包"] = f"+${n4_val:,}" + ("（×2）" if car["n4x"] == 2 else "")
    rows.append(row)

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片
note1_sub = ("60%以上" if "60% 以上" in note1_option else "低於60%" if "低於" in note1_option
             else "無母數一年以下" if "一年以下" in note1_option else "無母數一年以上")
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">HTW 每台單獎</div>
    <div class="m-value">${htw:,}</div>
    <div class="m-sub">TTL {total_sales} × CR-V e:HEV {crv_hev_cnt}</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{note1_sub}（ZR-V固定+3,000）</div>
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
if note3_on:
    col_order.append("備3")
if note4_on:
    col_order.append("備4紅包")
col_order.append("每台合計（最高）")
df = pd.DataFrame(rows)[col_order]

def style_table(df_in):
    def row_style(row):
        v = int(row["每台合計（最高）"].replace("$", "").replace(",", ""))
        if v == max_total:
            return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        return [""] * len(row)
    return df_in.style.apply(row_style, axis=1)

st.dataframe(style_table(df), use_container_width=True, hide_index=True, height=360)

# ── 計算式展開
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu_val = neicu(car)
        n1_val    = car["n1_fix"] if car["n1_fix"] is not None else note1
        n3_val    = car["n3"] if note3_on else 0
        n4_val    = 1000 * car["n4x"] if note4_on else 0
        color = "#cc0000" if total == max_total else "#333"
        bold  = "700" if total == max_total else "400"
        formula = (
            f"內促 ${neicu_val:,} ＋ SP ${car['sp']:,} ＋ HTW ${htw:,} ＋ 備1 ${n1_val:,}"
            + (f" ＋ 備3 ${n3_val:,}" if n3_val else "")
            + (f" ＋ 備4 ${n4_val:,}" if n4_val else "")
        )
        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　{formula} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金：CR-V e:HEV S B案$26k、Prestige B案$18k；HR-V G案（S $14k／e:HEV S $16k／e:HEV P $26k）；FIT C案（Home $9k／e:HEV $19k）。ZR-V、CR-V VTi-S/S SP視為0。")
st.caption("※ HTW：無CR-V e:HEV $2k~$5k；CR-V e:HEV 1台 $5k~$8k；CR-V e:HEV 2台 $8k~$10k。PRELUDE不計TTL台數。")
st.caption("※ 備1：ZR-V 乙式 +3,000。備2：10/11前完成2台訂單且10/31前領牌，本月促案直接以第4台計算。")
st.caption("※ 備3：10月ZR-V＋CR-V e:HEV現訂交達3台，ZR-V及CR-V e:HEV S每台+3,000、CR-V e:HEV Prestige每台+4,000。")
st.caption("※ 備4：10月現訂交達5台每台+1,000紅包（直販不計），CR-V e:HEV ×2。")
st.caption("※ 備5（未列入每台計算）：10月CIVIC預接單課目標2台完成，該課聚餐基金6,000元（領牌後發放）。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
