with fct_listen_events as (
    select * from {{ref('fct_streamify__listen_events')}}
),
dim_state as (
    select * from {{ref('dim_streamify__state')}}
)

select 
    ds.state_name as state_name,
    count(distinct fl.user_id) as total_users,
    round(count(distinct user_id) * 100.0 / sum(count(distinct user_id)) over(), 2) as conversion_rate_pct
from fct_listen_events fl 
left join dim_state ds on ds.state_id = fl.state
group by state_name


