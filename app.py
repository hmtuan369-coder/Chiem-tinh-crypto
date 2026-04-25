import streamlit as st
import ephem
import datetime
import pytz
import pandas as pd
import random
import calendar

# Cai dat mui gio
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.datetime.now(tz)
current_year = now.year
current_month = now.month

st.set_page_config(page_title="Chiem Tinh Crypto", page_icon="🌙")
st.title("🔮 Bang Diem & Bieu Do Chiem Tinh")
st.write(f"**Cap nhat:** {now.strftime('%d/%m/%Y - %H:%M')}")

st.divider()

# Quy tac cuoi tuan
day_of_week = now.weekday()
if day_of_week >= 5: 
    st.warning("⚠️ HOM NAY LA CUOI TUAN: Thanh khoan kem, de quet rau hai dau. Nen dac biet chu y quan sat khoi luong (Volume) theo Wyckoff hoac dung ngoai!")
else:
    st.info("✅ Thi truong dang trong tuan, thanh khoan binh thuong.")

# Tinh diem nang luong hom nay
observer = ephem.Observer()
observer.date = now.astimezone(pytz.utc)
sun, moon = ephem.Sun(observer), ephem.Moon(observer)
sep = abs(float(ephem.separation(sun, moon))) * (180 / ephem.pi)

score = -5
status = "🔴 1 VACH DO - Bien dong nhe, rut nhanh."
if 85 <= sep <= 95 or 175 <= sep <= 185:
    score, status = -10, "🔴 2 VACH DO - Rui ro cao, de kill Long/Short."
elif 115 <= sep <= 125 or 55 <= sep <= 65:
    score, status = 10, "🟢 VACH XANH - Thuan loi, du dia tang tot."

st.metric(label="Chi so Vach Hom Nay", value=f"{score} diem")
st.write(status)

st.divider()

# ---------------------------------------------------------
# BIEU DO THEO THANG (KET QUA CHIEM TINH TUNG NGAY)
# ---------------------------------------------------------
st.subheader(f"📅 Du Bao Chiem Tinh (Thang {current_month})")

days_in_month = calendar.monthrange(current_year, current_month)[1]
days_list = []
scores_list = []
colors_list = []

for d in range(1, days_in_month + 1):
    # Tinh toan nang luong cho tung ngay trong thang
    test_date = datetime.datetime(current_year, current_month, d, 12, 0, tzinfo=tz)
    obs_temp = ephem.Observer()
    obs_temp.date = test_date.astimezone(pytz.utc)
    s_temp, m_temp = ephem.Sun(obs_temp), ephem.Moon(obs_temp)
    sep_temp = abs(float(ephem.separation(s_temp, m_temp))) * (180 / ephem.pi)
    
    # Cham diem giong he thong mau
    if 85 <= sep_temp <= 95 or 175 <= sep_temp <= 185:
        day_score = -10
    elif 115 <= sep_temp <= 125 or 55 <= sep_temp <= 65:
        day_score = 10
    elif 45 <= sep_temp <= 54 or 135 <= sep_temp <= 145:
        day_score = 5
    else:
        day_score = -5
        
    days_list.append(f"{d:02d}")
    scores_list.append(day_score)
    # Phan loai mau: Xanh blue cho diem duong, Do cho diem am
    colors_list.append("#3b82f6" if day_score > 0 else "#ef4444") 

# Tao bang du lieu
df_month = pd.DataFrame({"Ngay": days_list, "KetQua": scores_list, "Color": colors_list})

# Ve bieu do cot
st.bar_chart(df_month, x="Ngay", y="KetQua", color="Color")

st.divider()

# ---------------------------------------------------------
# BIEU DO SONG THEO GIO (TRONG NGAY)
# ---------------------------------------------------------
st.subheader("📈 Bieu Do Song Nang Luong (24h Hom Nay)")
hours = [f"{h:02d}:00" for h in range(24)]
waves = []
for h in range(24):
    if 4 <= h <= 12: wave = (h - 3) * 10
    elif 18 <= h <= 21: wave = (h - 17) * 25
    else: wave = random.randint(5, 15)
    waves.append(wave)

df_wave = pd.DataFrame({"Gio": hours, "Song": waves})
st.area_chart(df_wave.set_index("Gio"), color="#8b5cf6")

st.caption("💡 Chon ngay co vach xanh/thanh khoan cao de danh, tranh cac ngay 2 vach do hoac cuoi tuan.")
