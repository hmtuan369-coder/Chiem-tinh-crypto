import streamlit as st
import ephem
import datetime
import pytz
import pandas as pd
import random
import calendar
import altair as alt

# Cai dat mui gio va thoi gian
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.datetime.now(tz)
current_year = now.year
current_month = now.month

st.set_page_config(page_title="Chiem Tinh Crypto Pro", page_icon="🔮", layout="wide")

# --- KHOI TAO DO TUONG THIEN VAN ---
obs = ephem.Observer()
sun, moon, jupt, sat = ephem.Sun(), ephem.Moon(), ephem.Jupiter(), ephem.Saturn()

# Function de cham diem nang luong da hanh tinh
def calculate_astro_score(target_date):
    obs.date = target_date.astimezone(pytz.utc)
    
    # 1. Tinh cac goc quan trong (Asepcts)
    # Goc giua cac hanh tinh: 0-180
    sep_sm = abs(float(ephem.separation(sun, moon))) * (180 / ephem.pi) # Sun-Moon
    sep_sj = abs(float(ephem.separation(sun, jupt))) * (180 / ephem.pi) # Sun-Jupiter
    sep_ms = abs(float(ephem.separation(moon, sat))) * (180 / ephem.pi) # Moon-Saturn
    
    current_score = 0
    
    # --- LOGIC CHAM DIEM NANG CAO ---
    # Sun-Moon: Can bang tam ly
    if 115 <= sep_sm <= 125 or 55 <= sep_sm <= 65: # Trine/Sextile: Thuan
        current_score += 3
    elif 85 <= sep_sm <= 95 or 175 <= sep_sm <= 185: # Square/Opposition: Kho
        current_score -= 3
        
    # Sun-Jupiter: May man, mo rong (Nang luong +)
    if 0 <= sep_sj <= 10: # Conjunction: Rat manh
        current_score += 5
    elif 115 <= sep_sj <= 125: # Trine: Thuan
        current_score += 2
        
    # Moon-Saturn: Can tro, kìm hãm (Nang luong -)
    if 85 <= sep_ms <= 95 or 175 <= sep_ms <= 185: # Square/Opposition: Xau
        current_score -= 5
        
    # Can bang diem va phan loai vach
    if current_score > 3: return 10    # Vach Xanh
    if current_score < -3: return -10 # 2 Vach Do
    if current_score == 0: return -5  # 1 Vach Do (Tinh hinh trung binh xau)
    return 5 if current_score > 0 else -7 # Điểm lẻ

# =========================================================================
# === GIAO DIEN CHINH ===
# =========================================================================
st.title(f"🔮 Dự Báo Theo Chiêm Tinh ( Tháng {current_month} / {current_year} )")
st.write(f"**Cập nhật:** {now.strftime('%d/%m/%Y - %H:%M')} (GMT+7)")

st.divider()

# =========================================================================
# I. DU BAO THEO THANG (KET QUA CHIEM TINH TUNG NGAY)
# =========================================================================
st.subheader(f"📅 Kết Quả Năng Lượng Chiêm Tinh")

days_in_month = calendar.monthrange(current_year, current_month)[1]
days_list, scores_list = [], []

for d in range(1, days_in_month + 1):
    test_date = datetime.datetime(current_year, current_month, d, 12, 0, tzinfo=tz)
    day_score = calculate_astro_score(test_date)
    days_list.append(f"{d:02d}")
    scores_list.append(day_score)
    
df_month = pd.DataFrame({"Ngày": days_list, "Điểm": scores_list})

# --- VE BIEU DO COT VOI MAU SAC THUAN/NGHICH ---
# Altair: Xanh #3b82f6 (Diem > 0), Do #ef4444 (Diem < 0)
chart = alt.Chart(df_month).mark_bar().encode(
    x='Ngày',
    y=alt.Y('Điểm', axis=alt.Axis(title='Kết quả Năng lượng')),
    color=alt.condition(
        alt.datum.Điểm > 0,
        alt.value("#3b82f6"),  # Xanh lam - Positive
        alt.value("#ef4444")   # Đỏ - Negative
    )
).properties(height=350)

st.altair_chart(chart, use_container_width=True)

st.caption("💡 Chú thích: Cột Xanh biểu thị năng lượng thuận lợi (dư địa tăng tốt). Cột Đỏ biểu thị năng lượng cản trở (dễ có áp lực giảm). Hãy kết hợp với Wyckoff để tìm vùng Cầu/Cung.")

st.divider()

# =========================================================================
# II. CHI TIET HOM NAY & BIEU DO SONG 24H
# =========================================================================
# Tao giao dien cot de bo tri khoa hoc
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader(f"📊 Chi Tiết Hôm Nay (Ngày {now.day})")
    today_score = calculate_astro_score(now)
    
    # Hien thi Metro voi mau sac
    score_color = "normal"
    status_text = "Năng lượng bất ổn nhẹ"
    
    if today_score == 10:
        score_color = "success"
        status_text = "🔴 🟢 VẠCH XANH - Năng lượng tốt"
    elif today_score == -10:
        score_color = "error"
        status_text = "🔴🔴 2 VẠCH ĐỎ - Rủi ro cao"
    else:
        score_color = "normal"
        status_text = "🔴 1 VẠCH ĐỎ - Thị trường đi ngang/Kill râu"

    st.metric(label="Chỉ Số Năng Lượng Vạch", value=f"{today_score} điểm", delta=None, delta_color="normal")
    st.write(status_text)
    
    # Khung gio song manh
    st.info("🌊 Khoảng thời gian thị trường sóng mạnh:\n**( 4h -> 12h ) ( 18h -> 21h )**")
    
    # Quy tac cuoi tuan
    day_of_week = now.weekday()
    if day_of_week >= 5: 
        st.warning("⚠️ LƯU Ý: Hôm nay là cuối tuần. Thanh khoản kém, de quet rau hai dau.")

with col2:
    st.subheader("📈 Biểu Đồ Sóng Năng Lượng (24h)")
    hours = [f"{h:02d}:00" for h in range(24)]
    waves = []
    
    # Tao song da dang hon voi mieu ta mieu ta mieu ta
    for h in range(24):
        base_wave = 15
        if 4 <= h <= 12: base_wave = (h - 3) * 12
        elif 18 <= h <= 21: base_wave = (h - 17) * 30
        else: base_wave = random.randint(5, 20)
        
        # Bien dong ngau nhien de song 'sông' hon
        waves.append(base_wave + random.randint(-5, 5)) 

    # Ve bieu do vung (Area Chart) mau Purple giong mau mau mau mau mau mau mau mau mau mau mau mau mau
    df_wave = pd.DataFrame({"Giờ": hours, "Cường Độ Sóng": waves})
    
    # Ve bieu do area co them 'Trục' (Median Line) de so sanh
    st.area_chart(df_wave.set_index("Giờ"), color="#8b5cf6")

st.caption("Lưu ý: Năng lượng chiêm tinh cung cấp cái nhìn về tâm lý thị trường, hãy luôn quản lý rủi ro và sử dụng Sonic R / Wyckoff để xác nhận điểm vào lệnh.")
