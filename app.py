import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="2026年11月 Honda 銷售條件試算",
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
    display: flex;
    align-items: center;
    gap: 18px;
}
.honda-logo { height: 56px; width: auto; flex-shrink: 0; }
@media (max-width: 540px) { .honda-logo { height: 42px; } .honda-header { gap: 12px; padding: 16px 18px; } }
.honda-header h1 { color: white; font-size: 22px; font-weight: 700; margin: 0 0 4px 0; }
.honda-header p  { color: rgba(255,255,255,0.8); font-size: 12px; margin: 0; }
.metric-row { display: flex; gap: 10px; margin: 14px 0; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 130px;
    background: white;
    border-radius: 12px;
    padding: 12px 14px;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-card .m-label { font-size: 10px; color: #999; margin-bottom: 5px; }
.metric-card .m-value { font-size: 20px; font-weight: 700; color: #cc0000; }
.metric-card .m-sub   { font-size: 10px; color: #aaa; margin-top: 3px; }
.metric-card.best { border-color: #cc0000; background: #fff8f8; }
.metric-card.htw  { border-color: #2196f3; background: #f0f7ff; }
.metric-card.htw .m-value { color: #1565c0; }
.section-label {
    font-size: 13px; font-weight: 700; color: #333;
    margin: 14px 0 8px 0; padding-left: 10px;
    border-left: 3px solid #cc0000;
}
.htw-box {
    background: #e3f2fd;
    border: 1px solid #90caf9;
    border-radius: 10px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 12px;
    color: #1565c0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── 頂部標題 ─────────────────────────────────────────────
LOGO_B64 = "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"

st.markdown(f"""
<div class="honda-header">
  <img class="honda-logo" src="data:image/png;base64,{LOGO_B64}" alt="Honda">
  <div>
    <h1>2026年11月 Honda 銷售條件試算</h1>
    <p>內促 ＋ SP銷售支援金 ＋ HTW銷售顧問獎勵（累點制）＋ 備註1車險獎勵　｜　領牌期間 2026/11/01–11/30</p>
  </div>
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
    note1_option = st.radio(
        "③ 上月首年車體續保率（備註1，取9月成績）",
        ["60% 以上 → +7,000", "低於 60% → +3,000", "無母數（一年以下）→ +5,000", "無母數（一年以上）→ +3,000"]
    )

with col2:
    htw_tier = st.radio(
        "② HTW 累計點數級距",
        ["累9點以上（$5,500/點）", "累7~8點（$4,500/點）", "累5~6點（$3,500/點）", "累3~4點（$2,500/點）", "未達3點（不發放）"],
        index=0
    )

# ── HTW 累點計算（每台 = 該車型點數 × 每點金額）─────────────
htw_rate = {"累9點以上（$5,500/點）":5500, "累7~8點（$4,500/點）":4500, "累5~6點（$3,500/點）":3500,
            "累3~4點（$2,500/點）":2500, "未達3點（不發放）":0}[htw_tier]
st.markdown(f'<div class="htw-box">📊 HTW 每點 <strong>${htw_rate:,}</strong>　｜　國產 e:HEV（HR-V e:HEV、FIT e:HEV、CR-V e:HEV）2點 = <strong>${htw_rate*2:,}</strong>/台　｜　進口（ZR-V、CIVIC）＆國產汽油（CR-V VTi-S/S、HR-V S、FIT Home）1點 = <strong>${htw_rate:,}</strong>/台　｜　PRELUDE 不計</div>', unsafe_allow_html=True)

# ── 備註1 ────────────────────────────────────────────────
note1_map = {
    "60% 以上 → +7,000":        7000,
    "低於 60% → +3,000":        3000,
    "無母數（一年以下）→ +5,000": 5000,
    "無母數（一年以上）→ +3,000": 3000,
}
note1 = note1_map[note1_option]

# ── 備註2 & 備註3 ─────────────────────────────────────────
tg1, tg2 = st.columns(2)
with tg1:
    note2_on = st.toggle(
        "④ 備註2：現訂交庫存車（每台 +2,000）",
        value=True,
        help="11月底清空11月前庫存，CR-V庫存車再+3,000"
    )
with tg2:
    note2_crv_extra = st.toggle(
        "　 備註2 CR-V 清空庫存（CR-V 再 +3,000）",
        value=True,
        help="清空11月前CR-V庫存，每台CR-V額外+3,000"
    ) if note2_on else False

note3_option = st.select_slider(
    "⑤ 備註3：本月現訂交台數（CR-V e:HEV S/P 加給）",
    options=["未達5台（無加給）", "5台（+2,000/台）", "6台（+5,000/台）", "7台以上（+8,000/台）"],
    value="7台以上（+8,000/台）"
)
note3_crv_p_map = {
    "未達5台（無加給）": 0,
    "5台（+2,000/台）": 2000,
    "6台（+5,000/台）": 5000,
    "7台以上（+8,000/台）": 8000,
}
note3_crv_p = note3_crv_p_map[note3_option]

is_high  = (tier == "4 台以上")
n2_base  = 2000 if note2_on else 0

# ── 車型資料 ─────────────────────────────────────────────
# is_crv=True   → 備注2 CR-V加給適用
# is_prelude=True → HTW不計（PRELUDE不計）
# note5=True    → CIVIC備注5預接獎勵+5,000
# crv_p=True    → 備注3 CR-V e:HEV P加給適用
car_data = [
    {"section":"PRELUDE","model":"e:HEV 26'年",    "nL":10000,"nH":10000,"sp":0,    "sp_note":"無",              "is_prelude":True, "is_crv":False,"crv_p":False,"pts":0,"note5":False},
    {"section":"CIVIC",  "model":"e:HEV 26'年",    "nL":0,    "nH":0,   "sp":0,    "sp_note":"無（上市發佈）",   "is_prelude":False,"is_crv":False,"crv_p":False,"pts":1,"note5":True},
    {"section":"ZR-V",   "model":"e:HEV 26'年",    "nL":10000,"nH":15000,"sp":6000,"sp_note":"B案",             "is_prelude":False,"is_crv":False,"crv_p":False,"pts":1,"note5":False},
    {"section":"HR-V",   "model":"S",              "nL":19000,"nH":21000,"sp":15000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"pts":1,"note5":False},
    {"section":"HR-V",   "model":"e:HEV S",        "nL":23000,"nH":25000,"sp":22000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"pts":2,"note5":False},
    {"section":"HR-V",   "model":"e:HEV P",        "nL":25000,"nH":27000,"sp":32000,"sp_note":"F案",            "is_prelude":False,"is_crv":False,"crv_p":False,"pts":2,"note5":False},
    {"section":"FIT",    "model":"Home",            "nL":37000,"nH":37000,"sp":10000,"sp_note":"D案",            "is_prelude":False,"is_crv":False,"crv_p":False,"pts":1,"note5":False},
    {"section":"FIT",    "model":"e:HEV",           "nL":41000,"nH":41000,"sp":25000,"sp_note":"D案",            "is_prelude":False,"is_crv":False,"crv_p":False,"pts":2,"note5":False},
    {"section":"CR-V",   "model":"e:HEV S",        "nL":22000,"nH":24000,"sp":27000,"sp_note":"D案",            "is_prelude":False,"is_crv":True, "crv_p":True,"pts":2,"note5":False},
    {"section":"CR-V",   "model":"e:HEV P",        "nL":22000,"nH":24000,"sp":19000,"sp_note":"C案",            "is_prelude":False,"is_crv":True, "crv_p":True, "pts":2,"note5":False},
    {"section":"CR-V",   "model":"VTi-S / S",      "nL":15000,"nH":15000,"sp":5000, "sp_note":"A案",            "is_prelude":False,"is_crv":True, "crv_p":False,"pts":1,"note5":False},
]

# ── 計算 ─────────────────────────────────────────────────
totals, rows = [], []
for car in car_data:
    neicu     = car["nH"] if is_high else car["nL"]
    sp        = car["sp"]
    htw_val   = car["pts"] * htw_rate
    n1        = note1
    n2        = n2_base + (3000 if (note2_on and note2_crv_extra and car["is_crv"]) else 0)
    n3        = note3_crv_p if car["crv_p"] else 0
    n5        = 5000 if car["note5"] else 0

    # CIVIC 內促TBD
    if car["note5"]:
        neicu_label = "待公佈"
        total = sp + htw_val + n1 + n2 + n5
    else:
        neicu_label = f"${neicu:,}"
        total = neicu + sp + htw_val + n1 + n2 + n3

    totals.append(total)

    sp_display  = f"${sp:,}（{car['sp_note']}）" if sp > 0 else f"$0（{car['sp_note']}）"
    htw_display = "—（PRELUDE不計）" if car["is_prelude"] else f"${htw_val:,}（{car['pts']}點）"
    n2_display  = f"+${n2:,}" if n2 > 0 else "—"
    n3_display  = f"+${n3:,}" if n3 > 0 else ""
    n5_display  = "+$5,000（備5）" if n5 > 0 else ""

    rows.append({
        "車系":            car["section"],
        "車型":            car["model"],
        "內促":            neicu_label,
        "SP最高現金":      sp_display,
        "HTW":         htw_display,
        "備註1":           f"+${n1:,}",
        "備註2":           n2_display,
        "每台合計（最高）": ("待公佈+" if car["note5"] else "") + f"${total:,}",
        "_total":          total,
    })

max_total = max(totals)
max_car   = car_data[totals.index(max_total)]

# ── 指標卡片 ─────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card htw">
    <div class="m-label">HTW e:HEV（2點）</div>
    <div class="m-value">${htw_rate*2:,}</div>
    <div class="m-sub">每點 ${htw_rate:,}</div>
  </div>
  <div class="metric-card htw">
    <div class="m-label">HTW 汽油/進口（1點）</div>
    <div class="m-value">${htw_rate:,}</div>
    <div class="m-sub">每點 ${htw_rate:,}</div>
  </div>
  <div class="metric-card">
    <div class="m-label">備註1 每台加給</div>
    <div class="m-value">+${note1:,}</div>
    <div class="m-sub">{'60%以上' if note1==7000 else '低於60%' if '低於' in note1_option else '無母數一年以下' if '一年以下' in note1_option else '無母數一年以上'}</div>
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
        total_str = row["每台合計（最高）"].replace("待公佈+","").replace("$","").replace(",","")
        try:
            if int(total_str) == max_total:
                return ["background-color:#fff0f0; font-weight:bold; color:#cc0000"] * len(row)
        except:
            pass
        return [""] * len(row)
    return df_in.style.apply(row_style, axis=1)

st.dataframe(
    style_table(df),
    width="stretch",
    hide_index=True,
    height=430
)

# ── 計算式展開 ────────────────────────────────────────────
with st.expander("📋 查看各車型詳細計算式"):
    for car, total in zip(car_data, totals):
        neicu   = car["nH"] if is_high else car["nL"]
        htw_val = car["pts"] * htw_rate
        n2      = n2_base + (3000 if (note2_on and note2_crv_extra and car["is_crv"]) else 0)
        n3      = note3_crv_p if car["crv_p"] else 0
        n5      = 5000 if car["note5"] else 0
        color   = "#cc0000" if total == max_total else "#333"
        bold    = "700" if total == max_total else "400"

        if car["note5"]:
            formula = f"內促 待公佈 ＋ SP ${car['sp']:,} ＋ HTW ${htw_val:,} ＋ 備1 ${note1:,} ＋ 備2 ${n2:,} ＋ 備5 $5,000 ＝ 待公佈+${total:,}"
        else:
            parts = [f"內促 ${neicu:,}", f"SP ${car['sp']:,}", f"HTW ${htw_val:,}", f"備1 ${note1:,}"]
            if n2: parts.append(f"備2 ${n2:,}")
            if n3: parts.append(f"備3 ${n3:,}")
            formula = " ＋ ".join(parts) + f" ＝ ${total:,}"

        st.markdown(
            f"<span style='color:{color};font-weight:{bold}'>"
            f"**{car['section']} {car['model']}**　{formula}"
            f"</span>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("※ HTW 累點制：國產 e:HEV（HR-V e:HEV S/P、FIT e:HEV、CR-V e:HEV S/P）2點；進口（ZR-V、CIVIC）及國產汽油（CR-V VTi-S/S、HR-V S、FIT Home）1點；PRELUDE 不計。（11/4 更新）累3-4點 $2,500/點、累5-6點 $3,500/點、累7-8點 $4,500/點、累9點以上 $5,500/點。")
st.caption("※ SP 取各方案最高現金選項。CIVIC/PRELUDE SP本月無現金（延保為加價購）。CR-V VTi-S/S A案需加選延長保固。")
st.caption("※ 備註1 取2026年9月成績。ZR-V 另有乙式保險+$3,000獎勵（未含於本表）。")
st.caption("※ 備註2：現訂交庫存車每台+2,000；11月底清空11月前庫存 → CR-V 再+3,000。")
st.caption("※ 備註3：現訂交5台+→CR-V e:HEV S/P每台+2,000；6台+→+5,000；7台+→+8,000（取最高適用）。")
st.caption("※ 備註5：CIVIC 上市前準備預接獎勵每台+5,000（需12/31前領牌），內促待上市公佈。")
st.caption("※ 本試算表僅供參考，實際獎金依 Honda Taiwan 官方公告為準。")
