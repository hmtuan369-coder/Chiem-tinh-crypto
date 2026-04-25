import streamlit as st
import ephem
import datetime
import pytz
import pandas as pd
import random

# Cài đặt múi giờ
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.datetime.now(tz)

st.set_page_config(page_title="Chiêm Tinh Crypto", page_icon="🌙", layout="centered")
st.title("🔮 Bảng Điểm & Biểu Đồ Chiêm Tinh")
st.write(f"**Cập nhật lúc:** {now.strftime('%d/%m/%Y - %H:%M')} (GMT+7)")

st.divider()

# 1. CẢNH BÁO CUỐI TUẦN
day_of_week = now.weekday()
if day_of_week >= 5: 
    st.warning("⚠️ **LƯU Ý:** Hôm nay là cuối tuần. Thanh khoản kém, giá thường khó chạy hoặc quét râu hai đầu. \n\n**Khuyến nghị:** Tranh thủ thời gian này dắt Bố đi dạo thay vì ngồi canh chart!")
else:
    st.info("✅ Thị trường đang trong tuần, thanh khoản duy trì ở mức bình thường.")

# 2. TÍNH ĐIỂM NĂNG LƯỢNG (VẠCH)
observer = ephem.Observer()
observer.date = now.astimezone(pytz.utc)

sun = ephem.Sun(observer)
moon = ephem.Moon(observer)

separation = abs(float(ephem.separation(sun, moon))) * (180 / ephem.pi)

score = 0
status_text = ""

if 85 <= separation <= 95 or 175 <= separation <= 185:
    score = -10
    status_text = "🔴 2 VẠCH ĐỎ (Rủi ro cao) - Dễ kill Long/Short."
elif 115 <= separation <= 125 or 55 <= separation <= 65:
    score = 10
    status_text = "🟢 VẠCH XANH (Thuận lợi) - Dư địa tăng tốt."
else:
    score = -5
    status_text = "🔴 1 VẠCH ĐỎ (Bất ổn nhẹ) - Đánh volume nhỏ, rút nhanh."

st.subheader("📊 Năng Lượng Hôm Nay")
st.metric(label="Chỉ số Vạch", value=f"{score} điểm")
if score > 0:
    st.success(status_text)
else:
    st.error(status_text)

st.divider()

# 3. BIỂU ĐỒ SÓNG THEO GIỜ
st.subheader("📈 Biểu Đồ Sóng Năng Lượng (24h)")

# Tạo dữ liệu giả lập sóng khớp với khung giờ bạn quan sát
hours = []
wave_values = []

for h in range(24):
    hours.append(f"{h:02d}:00")
    # Sóng sáng: 4h - 12h (Đỉnh lúc 12h)
    if 4 <= h <= 12:
        wave = (h - 3) * 10
    # Sóng tối: 18h - 21h (Đỉnh lúc 21h)
    elif 18 <= h <= 21:
        wave = (h - 17) * 25
    # Giờ nhiễu/đi ngang
    else:
        wave = random.randint(5, 15)
    wave_values.append(wave)

# Vẽ biểu đồ
df_wave = pd.DataFrame({
    "Giờ": hours,
    "Sóng": wave_values
})

# Hiển thị biểu đồ dạng mảng (Area Chart) màu tím/xanh
st.area_chart(df_wave.set_index("Giờ"), color="#8884d8")

st.caption("💡 Đỉnh sóng cao nhất rơi vào 12h00 trưa và 21h00 tối. Hãy kết hợp với vùng Cầu/Cung trên chart để tìm Entry.")
