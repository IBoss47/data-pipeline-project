with fct_listen_events as (
    select * from {{ref('int_streamify__listen_events')}}
),
dim_date as (
    select * from {{ref('dim_streamify__date')}}
),
dim_state as (
    select * from {{ref('dim_streamify__state')}}
),
base_grid as (
    select distinct
        ds.region as region,
        dd.day_of_week as day_of_week
    from dim_state ds
    cross join dim_date dd
    where region is not null
),
daily_listen as (
    select
        ds.region as region,
        dd.day_of_week as day,
        sum(fl.duration_minutes) / 60 as total_listen_hour
    from fct_listen_events fl
    left join dim_state ds on fl.state = ds.state_id
    left join dim_date dd on toDate(fl.time_stamp) = dd.date_day
    group by region, day
)

select 
    bg.region,
    bg.day_of_week as day_of_week,
    dl.total_listen_hour as total_hours,
    rank() over(partition by bg.region order by total_hours desc) as ranking
from base_grid bg
left join daily_listen dl on bg.day_of_week = dl.day and bg.region = dl.region


