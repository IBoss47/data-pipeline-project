# Datasets Configuration

ไฟล์ในโฟลเดอร์นี้ (`config/datasets`) ใช้สำหรับกำหนดโครงสร้างและรายละเอียดของข้อมูล (datasets) แต่ละชุด เพื่อใช้ใน Data Pipeline (เช่น การส่งผ่านข้อมูลด้วย Airflow, การทำ Schema mapping สำหรับ ClickHouse หรือการนำเข้าข้อมูลสู่ MinIO)

โครงสร้างของไฟล์อยู่ในรูปแบบ YAML (`.yml`) โดยมีรายละเอียดที่ต้องกำหนดดังต่อไปนี้:

## โครงสร้าง YAML (Schema)

| ฟิลด์ (Field) | ประเภท (Type) | คำอธิบาย (Description) |
|---|---|---|
| `name` | String | ชื่อของ dataset เช่น `customers`, `orders` |
| `source` | Object | การตั้งค่าเกี่ยวกับข้อมูลต้นทาง (Source Data) |
| ├── `type` | String | ประเภทของไฟล์ต้นทาง เช่น `csv` |
| ├── `path` | String | ที่อยู่ (Path) ของไฟล์ข้อมูลดิบ เช่น `/opt/data/raw/raw_ecom/customers.csv` |
| `target` | Object | การตั้งค่าข้อมูลปลายทางสำหรับ Data Warehouse (ClickHouse) |
| ├── `database` | String | ชื่อ Database ปลายทางใน ClickHouse เช่น `ecom_analytics` |
| ├── `table` | String | ชื่อ Table ใน ClickHouse เช่น `raw_customers` |
| ├── `engine` | String | Database Engine ที่ใช้งาน เช่น `MergeTree` |
| ├── `order_by` | List[String] | คอลัมน์ที่ใช้ในการเรียงลำดับข้อมูลใน Table เช่น `[customer_id]` |
| ├── `partition_by` | String / Null | เงื่อนไขการแบ่งพาร์ทิชัน (Partitioning) เช่น ฟิลด์วันที่ หรือ `null` หากไม่ต้องการแบ่ง |
| `storage` | Object | การตั้งค่าพื้นที่จัดเก็บข้อมูลบน Object Storage (Data Lake / MinIO) |
| ├── `provider` | String | ผู้ให้บริการ Object Storage เช่น `minio` |
| ├── `bucket` | String | ชื่อ Bucket เช่น `ecom` |
| ├── `layer` | String | ชั้นของข้อมูล (Data Layer) เช่น `raw`, `staging`, `serving` |
| ├── `folder` | String | ชื่อโฟลเดอร์ย่อย (Prefix) สำหรับเก็บข้อมูลชุดนี้ เช่น `customer` |
| ├── `format` | String | รูปแบบไฟล์ที่ต้องการจัดเก็บ เช่น `csv`, `parquet` |
| `column_types` | Key-Value | การกำหนดประเภทข้อมูล (Data Type) สำหรับแต่ละคอลัมน์ โดยระบุรูปแบบ `<column_name>: <clickhouse_type>` (เช่น `customer_id: UInt32`, `created_at: DateTime`) |
| `nullable` | Key-Value | ระบุว่าคอลัมน์ไหนยอมรับค่าว่าง (NULL) ได้ โดยระบุ `<column_name>: true` หากคอลัมน์ไหนห้ามเป็นค่าว่างไม่จำเป็นต้องใส่ หรือปล่อยว่างไว้ |
| `primary_key` | List[String] | รายชื่อคอลัมน์ที่ใช้เป็น Primary Key ในระบบจัดเก็บข้อมูล (มักจะสอดคล้องกับ `order_by` ใน ClickHouse) |

## ตัวอย่างการตั้งค่า (Example: `customers.yml`)

```yaml
name: customers

source:
  type: csv
  path: /opt/data/raw/raw_ecom/customers.csv

target:
  database: ecom_analytics
  table: raw_customers
  engine: MergeTree
  order_by:
    - customer_id
  partition_by: null

storage:
  provider: minio
  bucket: ecom
  layer: raw
  folder: customer
  format: csv

column_types:
  customer_id: UInt32
  customer_name: String
  email: String
  sub_tier: String
  created_at: DateTime

nullable:
  customer_name: true
  email: true

primary_key:
  - customer_id
```
