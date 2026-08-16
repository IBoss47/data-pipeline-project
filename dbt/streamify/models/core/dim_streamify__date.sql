with date_temp as (
    select 
        toDate('2025-01-01') + number as date_day
    from numbers(3650)
)

select 
    date_day,
    toYear(date_day) as year,
    toQuarter(date_day) as quarter,
    toMonth(date_day) as month_of_year,
    toDayOfMonth(date_day) as day_of_month,
    toDayOfWeek(date_day) as day_of_week,
    
    case
        when day_of_week in (6, 7) then TRUE
        else FALSE
    end as is_weekend
from date_temp
