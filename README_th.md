<div align="right">
  🌐 <strong><a href="README.md">🇬🇧 English</a></strong> | <strong><a href="README_th.md">🇹🇭 ภาษาไทย</a></strong>
</div>

# Streamify Data Pipeline Project

โปรเจคนี้เป็นระบบ Data Pipeline สำหรับวิเคราะห์ข้อมูลพฤติกรรมการฟังเพลงจากแพลตฟอร์มจำลอง (Streamify) โดยมีการประยุกต์ใช้ **Modern Data Stack** อย่าง `dbt`, `ClickHouse` และ `Airflow` ในการทำ Data Modeling และทำ Pipeline

> **หมายเหตุ:** 
> * โครงสร้างของ Project นี้ได้มีการ Clone มาจาก Github Repo ที่เป็น Structure ที่ผมได้เคยทำไว้ และนำมาปรับและต่อยอดจากของเดิม
> * ข้อมูลที่ใช้ใน Project นี้เป็นข้อมูลจาก **[Streamify](https://github.com/ankurchavda/ 
)** ซึ่งจะดึงข้อมูลจำลองมา ณ ช่วงเวลาใดเวลานึงเพียงเท่านั้น และจะถูกจัดเก็บใน `data/`

## System Architecture

![System Architecture](stack.png)

## Pipeline Workflow

```mermaid
flowchart LR
    Airflow[Airflow DAGs] --> Services[Python Services]
    
    subgraph dbt [dbt Transformation]
        direction LR
        STG[Staging] --> INT[Intermediate]
        INT --> CORE[Fact & Dim]
        CORE --> MARTS[Marts]
    end
    
    Services --> STG

    style Airflow fill:#e8f4f8,stroke:#017cee,stroke-width:2px,color:#000
    style Services fill:#f0f5f9,stroke:#306998,stroke-width:2px,color:#000
    style dbt fill:#fff0ed,stroke:#ff694b,stroke-width:2px,color:#000
```
---

## Project Structure (โครงสร้างโปรเจค)

### 1. `data/` (ข้อมูลดิบ)
โฟลเดอร์สำหรับจัดเก็บไฟล์ข้อมูลดิบ (Raw Data) ที่ถูกจำลองขึ้นมา
- **Note:** ไฟล์ข้อมูลขนาดใหญ่จะไม่ถูกนำขึ้น Git (ถูกกำหนดไว้ใน `.gitignore`) 
- จะมีเพียงไฟล์ `_sample.csv` ที่จำกัด **200 แถว** สำหรับใช้ทดสอบรันระบบเบื้องต้นเท่านั้น

### 2. `services/` (Python Data Ingestion)
ชุดคำสั่ง Python สำหรับนำเข้าและจัดการไฟล์ก่อนส่งเข้า Data Warehouse
- **`extractors/csv_extractor.py`**: ช่วยในการอ่านไฟล์ CSV 
- **`converters/parquet_converter.py`**: แปลงไฟล์จาก Raw CSV ให้เป็น Parquet Format 
- **`metadata/ddl_generator.py`**: ตัวช่วยแกะโครงสร้างข้อมูล (Schema) ออกมาเป็นคำสั่ง DDL เพื่อสร้างตารางใน ClickHouse

### 3. `dbt/streamify/` (Data Transformation)
การทำงานในส่วนนี้ถูกแบ่งออกเป็น 3 ชั้น (Layers) หลักๆ:

- **`models/staging/`** *(ชั้นทำความสะอาด)*
  - **Files:** `stg_streamify__listen_events`, `stg_streamify__auth_events`, `stg_streamify__page_view_events`

- **`models/intermediate/`** *(OBT)*
  - **Files:** `int_streamify__listen_events`

- **`models/core/`** *(Star Schema)*
  - **หน้าที่:** แตกตารางออกจาก Intermediate แยกเป็น **Dimension (ตารางมิติ)** เพื่ออธิบายข้อมูล และ **Fact (ตารางเหตุการณ์)** เพื่อเก็บตัวเลขการกระทำ
  - **ไฟล์สำคัญ:** 
    - `fct_streamify__listen_events` *(Fact การฟังเพลง)*
    - `dim_streamify__users`, `dim_streamify__contents`, `dim_streamify__date` *(Dimension ต่างๆ)*

### 4. `airflow/` (Data Orchestration)
โฟลเดอร์สำหรับจัดการ Workflow และตั้งเวลาการทำงาน (Scheduling) ของ Data Pipeline
- **`dags/`**: โฟลเดอร์สำหรับเก็บไฟล์ DAG (Directed Acyclic Graph) ซึ่งใช้กำหนดลำดับขั้นตอนการทำงานของ Pipeline เช่น สั่งรัน Python Script เพื่อนำเข้าข้อมูล แล้วตามด้วยการสั่ง `dbt run`
- **`config/datasets/`**: จัดเก็บไฟล์การตั้งค่า (Config/Metadata) ที่เกี่ยวข้องกับชุดข้อมูล เพื่อให้ Airflow สามารถอ้างอิงและจัดการข้อมูลได้อย่างเป็นระบบ

---

## การจำลองสถานการณ์ทางธุรกิจ (Business Scenario Simulation)

เนื่องจากโปรเจคนี้จัดทำขึ้นเพื่อฝึกฝนการสร้าง Data Pipeline และพัฒนาทักษะในสายงาน Data Engineer แต่ในโลกของการทำงานจริงนั้น Data Engineer จำเป็นต้องมีการสื่อสารและทำงานร่วมกับหลายฝ่าย เช่น Data Owner, Business Analyst (BA), Data Scientist และผู้บริหาร

ดังนั้น เพื่อให้เห็นภาพการทำงานที่ใกล้เคียงกับความเป็นจริงมากที่สุด ผมจึงได้ทำการ Prompt AI เพื่อจำลองบทบาท (Roles) ต่างๆ ที่เกี่ยวข้อง ดังนี้:
- **Data Source Owner**
- **Business Analyst (BA)**
- **CEO**

สามารถดูรายละเอียดคำถามทางธุรกิจ (Business Questions) ที่ได้จากการจำลองสถานการณ์นี้ได้ที่: <strong><a href="dbt/streamify/models/bussiness_question.md">Business Questions</a></strong>
