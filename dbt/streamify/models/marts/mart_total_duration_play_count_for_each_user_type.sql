with fct_listen_events as (
    select * from {{ref('fct_streamify__listen_events')}}
),
dim_users as (
    select * from {{ref('dim_streamify__users')}}
),

select 
    du.current_level as current_level,
    sum(fl.duration_minutes) / 60 as total_listen_hour,
    count(fl.is_valid_play) as total_play
from fct_listen_events fl
left join dim_users du 
using (user_id)
where fl.is_valid_play = 1
group by du.current_level
order by total_listen_hour, total_play