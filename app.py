import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="2026年9月 Honda 銷售條件試算",
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
  <h1>🚗 2026年9月 Honda 銷售條件試算</h1>
  <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵（103期）＋ 備註1車險獎勵　｜　領牌期間 2026/09/01–09/30</p>
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
    has_crv_hev = st.radio(
        "② 本月有無販售 CR-V e:HEV（HTW）",
        ["有 CR-V e:HEV", "無 CR-V e:HEV"],
        horizontal=True,
        index=0
    )

with col2:
    total_sales = st.radio(
        "③ TTL領牌台數（HTW，不含PRELUDE）",
        ["1台", "2台", "3台", "4台以上"],
        horizontal=True,
        index=3
    )
    note1_option = st.radio(
        "④ 8月首年車體續保率（備註1）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無母數（一年以下）→ +5,000", "無母數（一年以上）→ +3,000"],
        index=0
    )

# ── 備2 / 備4
col_n1, col_n2 = st.columns(2)
with col_n1:
    note2_on = st.toggle(
        "⑤ 備2：9/18前完成 ZR-V 或 CR-V e:HEV S 預接單 1 台",
        value=True,
        help="CR-V e:HEV 訂單車型內促每台直接以第4台內促計算（CR-V e:HEV 及 ZR-V 需9/30前領牌）"
    )
with col_n2:
    note4_option = st.radio(
        "⑥ 備4：9月現訂交達5台（直販不計）",
        ["未達成", "達5台 → 每台 +1,000", "達5台＋法人達成率南區第一 → 每台 +3,000"],
        index=2
    )

if note2_on:
    st.markdown('<div class="warn-box">⚠️ 備2達成：CR-V e:HEV S 及 e:HEV P(Prestige) 內促直接套用第4台 $22,000</div>', unsafe_allow_html=True)

# ── 計算邏輯
HTW_TABLE = {
    "有 CR-V e:HEV": {"1台": 5000, "2台": 6000, "3台": 7000, "4台以上": 8000},
    "無 CR-V e:HEV": {"1台": 2000, "2台": 3000, "3台": 4000, "4台以上": 5000},
}
htw = HTW_TABLE[has_crv_hev][total_sales]

note1_map = {
    "60% 以上 → +7,000":         7000,
    "低於 60% → +3,000":         3000,
    "無母數（一年以下）→ +5,000": 5000,
    "無母數（一年以上）→ +3,000": 3000,
}
note1 = note1_map[note1_option]

NOTE4_MAP = {
    "未達成": 0,
    "達5台 → 每台 +1,000": 1000,
    "達5台＋法人達成率南區第一 → 每台 +3,000": 3000,
}
note4_base = NOTE4_MAP[note4_option]
show_note4 = note4_base > 0

tier_idx = {"1～2 台": 0, "3 台": 1, "4 台以上": 2}[tier]

# car_data:
#   nL/nM/nH = 1~2台 / 3台 / 4台以上 內促
#   sp       = SP最高現金（負數=DLR負擔）
#   crv_hev  = True → 備2達成時內促直接套第4台
#   n4x      = 備4紅包倍數（CR-V e:HEV S ×2）
car_data = [
    {"section": "HR-V", "model": "S",                  "nL": 19000, "nM": 21000, "nH": 23000, "sp": 14000, "sp_note": "G案",              "crv_hev": False, "n4x": 1},
    {"section": "HR-V", "model": "e:HEV S",            "nL": 23000, "nM": 25000, "nH": 27000, "sp": 19000, "sp_note": "G案",              "crv_hev": False, "n4x": 1},
    {"section": "HR-V", "model": "e:HEV P",            "nL": 25000, "nM": 27000, "nH": 29000, "sp": 19000, "sp_note": "G案",              "crv_hev": False, "n4x": 1},
    {"section": "FIT",  "model": "Home",               "nL": 39000, "nM": 39000, "nH": 39000, "sp": 9000,  "sp_note": "D案",              "crv_hev": False, "n4x": 1},
    {"section": "FIT",  "model": "e:HEV",              "nL": 43000, "nM": 43000, "nH": 43000, "sp": 19000, "sp_note": "D案",              "crv_hev": False, "n4x": 1},
    {"section": "CR-V", "model": "e:HEV S",            "nL": 18000, "nM": 20000, "nH": 22000, "sp": 11000, "sp_note": "B案",              "crv_hev": True,  "n4x": 2},
    {"section": "CR-V", "model": "e:HEV P (Prestige)", "nL": 18000, "nM": 20000, "nH": 22000, "sp": 0,     "sp_note": "A案（無現金）",     "crv_hev": True,  "n4x": 1},
    {"section": "CR-V", "model": "VTi-S / S",          "nL": 13000, "nM": 15000, "nH": 15000, "sp": -3000, "sp_note": "A案DLR負擔-3,000", "crv_hev": False, "n4x": 1},
]

def neicu(car):
    if car["crv_hev"] and note2_on:
        return car["nH"]
    return [car["nL"], car["nM"], car["nH"]][tier_idx]

def sp_text(car):
    if car["sp"] > 0:
        return f"${car['sp']:,}（{car['sp_note']}）"
    if car["sp"] < 0:
        return f"-${-car['sp']:,}（{car['sp_note']}）"
    return f"$0（{car['sp_note']}）"

totals, rows = [], []
for car in car_data:
    neicu_val = neicu(car)
    n4_val    = note4_base * car["n4x"]
    total     = neicu_val + car["sp"] + htw + note1 + n4_val
    totals.append(total)

    neicu_label = f"${neicu_val:,}"
    if car["crv_hev"] and note2_on and tier_idx < 2:
        neicu_label += "（備2套第4台）"

    row = {
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            neicu_label,
        "SP最高現金":      sp_text(car),
        "HTW獎勵":         f"${htw:,}",
        "備註1":           f"+${note1:,}",
        "每台合計（最高）": f"${total:,}",
    }
    if show_note4:
        row["備4紅包"] = f"+${n4_val:,}" + ("（×2）" if car["n4x"] == 2 else "")
    rows.append(row)

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片
htw_label = "有CR-V e:HEV" if has_crv_hev == "有 CR-V e:HEV" else "無CR-V e:HEV"
note1_sub = ("60%以上" if "60% 以上" in note1_option else "低於60%" if "低於" in note1_option
             else "無母數一年以下" if "一年以下" in note1_option else "無母數一年以上")
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="m-label">HTW 每台單獎</div>
    <div class="m-value">${htw:,}</div>
    <div class="m-sub">{total_sales} × {htw_label}</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{note1_sub}</div>
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
if show_note4:
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

st.dataframe(style_table(df), use_container_width=True, hide_index=True, height=320)

# ── 計算式展開
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu_val = neicu(car)
        n4_val    = note4_base * car["n4x"]
        color = "#cc0000" if total == max_total else "#333"
        bold  = "700" if total == max_total else "400"
        n2_str = "（備2套第4台）" if car["crv_hev"] and note2_on and tier_idx < 2 else ""
        n4_str = f" ＋ 備4 ${n4_val:,}" + ("（×2）" if car["n4x"] == 2 else "") if n4_val else ""
        sp_str = f"-${-car['sp']:,}" if car["sp"] < 0 else f"${car['sp']:,}"
        formula = f"內促 ${neicu_val:,}{n2_str} ＋ SP {sp_str} ＋ HTW ${htw:,} ＋ 備1 ${note1:,}{n4_str}"
        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　{formula} ＝ **${total:,}**"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ SP取各方案最高現金：CR-V e:HEV S B案$11k；HR-V G案（S $14k／e:HEV $19k）；FIT D案（Home $9k／e:HEV $19k）。")
st.caption("※ CR-V VTi-S/S A案延長保固 DLR負擔$3,000，計入合計-$3,000。CR-V e:HEV P(Prestige) A案延長保固無現金。")
st.caption("※ HTW：有CR-V e:HEV $5k~$8k；無CR-V e:HEV $2k~$5k。PRELUDE不計TTL台數。ZR-V內促上市發佈，未列入。")
st.caption("※ 備2：9/18前完成 ZR-V 或 CR-V e:HEV S 預接單1台，CR-V e:HEV 內促每台以第4台計（CR-V e:HEV 及 ZR-V 需9/30前領牌）。")
st.caption("※ 備4：9月現訂交達5台每台+1,000紅包（直販不計）；法人達成率南區第一加碼至每台3,000；CR-V e:HEV S 獎勵×2。")
st.caption("※ 備5（未列入每台計算）：9月售1台CR-V e:HEV＋ZR-V/HR-V/FIT e:HEV三選二現訂交，紅包+10,000。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
