# Streamify Business Questions & Data Modeling

## 1. Fact_Listen (ข้อมูลพฤติกรรมการฟังเพลง)
**ข้อมูลหลัก:** `listen_events.csv`
- **Fact Table:** `fact_listen_events` *(เก็บข้อมูลระดับ 1 row = 1 song played)*
- **Dimensions:** `dim_date`, `dim_users`, `dim_content`, `dim_state`

### Business Question 1
> *"ในแต่ละเดือน ผู้ใช้งานกลุ่ม Paid และ Free มีระยะเวลาการฟังเพลงรวม (Total Listening Hours) และจำนวนครั้งที่ฟังเพลง (Total Play Counts)*

### Business Question 2 (มุมมอง CEO ด้านพฤติกรรมผู้ใช้งานและโครงสร้างพื้นฐาน)
> *"ในแต่ละภูมิภาคมีอัตราการเข้าใช้ระบบเท่าใด? เพื่อใช้วางแผนการตลาดและปรับปรุงการรองรับของระบบ (Server Scale)"*

### Business Question 1.3 (มุมมอง CEO ด้านกลยุทธ์ผลิตภัณฑ์)
> *"ผู้ใช้งานกลุ่มที่เปลี่ยนมาเป็นแบบจ่ายเงิน (Paid) มีพฤติกรรมการฟังเพลงที่หลากหลายขึ้นหรือไม่ (เช่น ฟังศิลปินหรือแนวเพลงใหม่ๆ มากขึ้น) เมื่อเทียบกับตอนใช้ฟรี? เพื่อนำไปพัฒนาฟีเจอร์ แนะนำเพลง (Personalized Recommendation) ที่กระตุ้นยอด Subscription"*


