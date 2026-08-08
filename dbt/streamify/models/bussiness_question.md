# Streamify Business Questions & Data Modeling

## 1. Fact_Listen (ข้อมูลพฤติกรรมการฟังเพลง)
**ข้อมูลหลัก:** `listen_events.csv`

### Business Question 1
> *"ในแต่ละเดือน ผู้ใช้งานกลุ่ม Paid และ Free มีระยะเวลาการฟังเพลงรวม (Total Listening Hours) และจำนวนครั้งที่ฟังเพลง (Total Play Counts) ของแต่ละศิลปิน (Artist) แตกต่างกันอย่างไร?"*

- **Fact Table:** `Fact_Listen` *(เก็บข้อมูลระดับ 1 row = 1 song played)*
- **Measures (Facts):** `sum(duration)`, `count(song_plays)`
- **Dimensions:** `Dim_Date` (Year, Month), `Dim_User_Tier` (Level), `Dim_Content` (Artist, Song)

### Business Question 2
> *"พื้นที่ใด (City/State) ที่มียอดการสตรีมเพลงสูงที่สุดในช่วงวันหยุดสุดสัปดาห์ (Weekends) แบ่งตามเพศของผู้ใช้งาน?"*

- **Fact Table:** `Fact_Listen`
- **Measures (Facts):** `count(song_plays)`
- **Dimensions:** `Dim_Geography` (City, State), `Dim_Date` (Day of Week, Is_Weekend), `Dim_User` (Gender)

---

## 2. Fact_Page_View (ข้อมูลการใช้งานแพลตฟอร์ม/เว็บไซต์)
**ข้อมูลหลัก:** `page_view_events.csv`

### Business Question 3
> *"ในแต่ละวัน แพลตฟอร์มเกิดข้อผิดพลาด (HTTP Status ที่ไม่ใช่ 200) จำนวนกี่ครั้ง และข้อผิดพลาดเหล่านั้นมักเกิดขึ้นในหน้าเพจ (Page) ใดมากที่สุด?"*

- **Fact Table:** `Fact_Page_View` *(เก็บข้อมูลระดับ 1 row = 1 page view event)*
- **Measures (Facts):** `count(error_events)` หรือ `count(page_views)`
- **Dimensions:** `Dim_Date`, `Dim_Page` (Page Name), `Dim_Status_Code`

### Business Question 4
> *"มีจำนวนผู้ใช้งานกี่รายที่เข้าชมหน้า 'Upgrade' หรือหน้า 'Cancel' (หากมี) โดยแยกตามประเภทอุปกรณ์/เบราว์เซอร์ (User Agent) ที่ใช้?"*

- **Fact Table:** `Fact_Page_View`
- **Measures (Facts):** `count(distinct user_id)`, `count(page_views)`
- **Dimensions:** `Dim_Page`, `Dim_Device` *(สกัดข้อมูล OS/Browser จาก userAgent)*

---

## 3. Fact_User_Session (ตารางสรุประดับเซสชัน - Aggregated Fact)
**ข้อมูลหลัก:** รวบรวมจาก `auth_events.csv`, `listen_events.csv`, `page_view_events.csv`

### Business Question 5
> *"โดยเฉลี่ยแล้ว ผู้ใช้งาน 1 เซสชัน (Session) มีการเปิดหน้าเพจกี่หน้า (Pages per Session) และฟังเพลงกี่เพลง (Songs per Session) เปรียบเทียบระหว่างผู้ใช้ Paid และ Free?"*

- **Fact Table:** `Fact_User_Session` *(เก็บข้อมูลระดับ 1 row = 1 Session ID)*
- **Measures (Facts):** `count(pages_viewed)`, `count(songs_played)`, `avg(session_duration)`
- **Dimensions:** `Dim_User_Tier` (Level), `Dim_Date` (Session Start Date)

---

## 4. Fact_Auth (ข้อมูลการยืนยันตัวตนและความปลอดภัย)
**ข้อมูลหลัก:** `auth_events.csv`

### Business Question 6
> *"อัตราความสำเร็จในการเข้าสู่ระบบ (Login Success Rate) ในแต่ละชั่วโมงของวันเป็นเท่าใด และมีผู้ใช้งาน (Daily Active Users) ที่เข้าสู่ระบบสำเร็จจากแต่ละรัฐ (State) จำนวนเท่าใด?"*

- **Fact Table:** `Fact_Auth` *(เก็บข้อมูลระดับ 1 row = 1 login attempt)*
- **Measures (Facts):** `count(total_logins)`, `count(successful_logins)`, `count(distinct user_id)`
- **Dimensions:** `Dim_Time` (Hour), `Dim_Date`, `Dim_Geography` (State)