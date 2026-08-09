# Streamify Business Questions & Data Modeling

## 1. Fact_Listen (ข้อมูลพฤติกรรมการฟังเพลง)
**ข้อมูลหลัก:** `listen_events.csv`

### Business Question 1
> *"ในแต่ละเดือน ผู้ใช้งานกลุ่ม Paid และ Free มีระยะเวลาการฟังเพลงรวม (Total Listening Hours) และจำนวนครั้งที่ฟังเพลง (Total Play Counts) ของแต่ละศิลปิน (Artist) แตกต่างกันอย่างไร?"*

- **Fact Table:** `fact_listen_events` *(เก็บข้อมูลระดับ 1 row = 1 song played)*
- **Dimensions:** `dim_date`, `dim_users`, `dim_content`