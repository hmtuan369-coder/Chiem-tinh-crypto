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

# Function de cham diem nang luong da hanh tinh (DA FIX LOI THIEN VAN)
def calculate_astro_score(target_date):
    obs = ephem.Observer()
    obs.date = target_date.astimezone(pytz.utc)
    
    # Phai cap nhat vi tri hanh tinh o ben TRONG ham cho tung ngay
    sun = ephem.Sun(obs)
    moon = ephem.Moon(obs)
    jupt = ephem.Jupiter(obs)
    sat = ephem.Saturn(obs)
    
    # 1. Tinh cac goc quan trong (Asepcts)
    sep_sm = abs(float(ephem.separation(sun, moon))) * (180 / ephem.pi)
    sep_sj = abs(float(ephem.separation(sun, jupt))) * (180 / ephem.pi)
    sep_ms = abs(float(ephem.separation(moon, sat))) * (180 / ephem.pi)
    
    current_score = 0
    
    # Sun-Moon: Can bang tam ly
    if 115 <= sep_sm <= 125 or 55 <= sep_sm <= 65:
        current_score += 3
    elif 85 <= sep_sm <= 95 or 175 <= sep_sm <= 185:
        current_score -= 3
        
    # Sun-Jupiter: May man, mo rong (Nang luong +)
    if 0 <= sep_sj <= 10:
        current_score += 5
    elif 115 <= sep_sj <= 125:
        current_score += 2
        
    # Moon-Saturn: Can tro, kìm hãm (Nang luong -)
    if 85 <= sep_ms <= 95 or 175 <= sep_ms <= 185:
        current_score -= 5
        
    # Can bang diem va phan loai vach
    if current_score > 3: return 10    # Vach Xanh
    if current_score < -3: return -10 # 2 Vach Do
    if current_score == 0: return -5  # 1 Vach Do
    return 5 if current_score > 0 else -7 

# =========================================================================
# === GIAO DIEN CHINH ===
# =========================================================================
st.title(f"🔮 Dự Báo Theo Chiêm Tinh ( Tháng {current_month} / {current_year} )")
st.write(f"**Cập nhật:** {now.strftime('%d/%m/%Y - %H:%M')} (GMT+7)")

st.divider()

# =========================================================================
# I. DU BAO THEO THANG
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

# Altair Chart (Tu dong Xanh/Do theo diem so)
chart = alt.Chart(df_month).mark_bar().encode(
    x='Ngày',
    y=alt.Y('Điểm', axis=alt.Axis(title='Kết quả Năng lượng')),
    color=alt.condition(
        alt.datum.Điểm > 0,
        alt.value("#3b82f6"),  # Xanh lam
        alt.value("#ef4444")   # Đỏ
    )
).properties(height=350)

st.altair_chart(chart, use_container_width=True)

st.caption("💡 Chú thích: Cột Xanh biểu thị năng lượng thuận lợi. Cột Đỏ biểu thị năng lượng cản trở.")

st.divider()

# =========================================================================
# II. CHI TIET HOM NAY & BIEU DO SONG 24H
# =========================================================================
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader(f"📊 Chi Tiết Hôm Nay (Ngày {now.day})")
    today_score = calculate_astro_score(now)
    
    if today_score == 10:
        status_text = "🟢 VẠCH XANH - Năng lượng thuận lợi"
    elif today_score == -10:
        status_text = "🔴🔴 2 VẠCH ĐỎ - Rủi ro cao, dễ kill râu"
    else:
        status_text = "🔴 1 VẠCH ĐỎ - Thị trường đi ngang/Bất ổn nhẹ"

    st.metric(label="Chỉ Số Năng Lượng", value=f"{today_score} điểm")
    st.write(status_text)
    
    st.info("🌊 Sóng mạnh:\n**( 4h -> 12h ) & ( 18h -> 21h )**")
    
    day_of_week = now.weekday()
    if day_of_week >= 5: 
        st.warning("⚠️ LƯU Ý CUỐI TUẦN: Thanh khoản kém. Nhớ dành thời gian nghỉ ngơi, chơi đùa với Bố nhé!")

with col2:
    st.subheader("📈 Biểu Đồ Sóng Năng Lượng (24h)")
    hours = [f"{h:02d}:00" for h in range(24)]
    waves = []
    
    for h in range(24):
        base_wave = 15
        if 4 <= h <= 12: base_wave = (h - 3) * 12
        elif 18 <= h <= 21: base_wave = (h - 17) * 30
        else: base_wave = random.randint(5, 20)
        
        waves.append(base_wave + random.randint(-5, 5)) 

    df_wave = pd.DataFrame({"Giờ": hours, "Cường Độ Sóng": waves})
    st.area_chart(df_wave.set_index("Giờ"), color="#8b5cf6")

st.caption("Lưu ý: Luôn quản lý rủi ro và sử dụng Sonic R / Wyckoff để xác nhận vùng Cung-Cầu trước khi vào lệnh.")
