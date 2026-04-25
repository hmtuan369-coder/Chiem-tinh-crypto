import streamlit as st
import ephem
import datetime
import pytz

# Cài đặt múi giờ Việt Nam
tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.datetime.now(tz)

st.set_page_config(page_title="Chiêm Tinh Crypto", page_icon="🌙")
st.title("🔮 Bảng Điểm Chiêm Tinh Cá Nhân")
st.write(f"**Ngày cập nhật:** {now.strftime('%d/%m/%Y - %H:%M')} (GMT+7)")

st.divider()

# Quy tắc thanh khoản cuối tuần
day_of_week = now.weekday()
if day_of_week >= 5: 
    st.warning("⚠️ **LƯU Ý:** Hôm nay là cuối tuần. Thanh khoản kém, giá thường khó chạy hoặc quét râu hai đầu. \n\n**Khuyến nghị:** Dành thời gian dắt Bố đi dạo thay vì ngồi canh chart!")
else:
    st.info("✅ Thị trường đang trong tuần, thanh khoản duy trì ở mức bình thường.")

# Tính năng lượng (Vạch Xanh/Đỏ)
observer = ephem.Observer()
observer.date = now.astimezone(pytz.utc)

sun = ephem.Sun(observer)
moon = ephem.Moon(observer)

separation = abs(float(ephem.separation(sun, moon))) * (180 / ephem.pi)

score = 0
status_text = ""

if 85 <= separation <= 95 or 175 <= separation <= 185:
    score = -10
    status_text = "🔴 Lực cản mạnh (2 Vạch Đỏ) - Dễ xảy ra kill Long/Short. Không gồng lệnh."
elif 115 <= separation <= 125 or 55 <= separation <= 65:
    score = 10
    status_text = "🟢 Năng lượng thuận (Vạch Xanh) - Dư địa tăng tốt."
else:
    score = -5
    status_text = "🔴 Năng lượng bất ổn nhẹ (1 Vạch Đỏ) - Đánh volume nhỏ, ăn ngắn rút nhanh."

st.subheader("📊 Điểm Năng Lượng Hôm Nay")
st.metric(label="Chỉ số", value=f"{score} điểm")
if score > 0:
    st.success(status_text)
else:
    st.error(status_text)

st.divider()

st.subheader("🌊 Khung Giờ Sóng Mạnh")
col1, col2 = st.columns(2)
with col1:
    st.info("🌅 **Sáng:** 04h00 - 12h00")
with col2:
    st.info("🌃 **Tối:** 18h00 - 21h00")
