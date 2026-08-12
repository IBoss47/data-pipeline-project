# Streamify Business Questions & Data Modeling

## 1. Fact_Listen (ข้อมูลพฤติกรรมการฟังเพลง)
**ข้อมูลหลัก:** `listen_events.csv`
- **Fact Table:** `fact_listen_events` *(เก็บข้อมูลระดับ 1 row = 1 song played)*
- **Dimensions:** `dim_date`, `dim_users`, `dim_content`, `dim_state`

### Business Question 1
> *"ในแต่ละเดือน ผู้ใช้งานกลุ่ม Paid และ Free มีระยะเวลาการฟังเพลงรวม (Total Listening Hours) และจำนวนครั้งที่ฟังเพลง (Total Play Counts) ของแต่ละศิลปิน (Artist) แตกต่างกันอย่างไร?"*

### Business Question 1.1 (มุมมอง CEO ด้านคุณภาพคอนเทนต์และการลงทุน)
> *"ศิลปิน (Artist) หรือเพลง (Song) ใดที่มีสัดส่วนการฟังเพลง (Duration Rate) สูงที่สุด และมีการกดข้ามเพลง (Skip Rate) ต่ำที่สุด? ข้อมูลนี้จะช่วยในการตัดสินใจซื้อลิขสิทธิ์เพลงหรือการโปรโมตศิลปิน"*

### Business Question 1.2 (มุมมอง CEO ด้านพฤติกรรมผู้ใช้งานและโครงสร้างพื้นฐาน)
> *"วันใดในสัปดาห์ที่มีปริมาณการฟังเพลงสูงสุดในแต่ละภูมิภาค (Location)? เพื่อใช้วางแผนการตลาดและปรับปรุงการรองรับของระบบ (Server Scale)"*

### Business Question 1.3 (มุมมอง CEO ด้านกลยุทธ์ผลิตภัณฑ์)
> *"ผู้ใช้งานกลุ่มที่เปลี่ยนมาเป็นแบบจ่ายเงิน (Paid) มีพฤติกรรมการฟังเพลงที่หลากหลายขึ้นหรือไม่ (เช่น ฟังศิลปินหรือแนวเพลงใหม่ๆ มากขึ้น) เมื่อเทียบกับตอนใช้ฟรี? เพื่อนำไปพัฒนาฟีเจอร์ แนะนำเพลง (Personalized Recommendation) ที่กระตุ้นยอด Subscription"*


