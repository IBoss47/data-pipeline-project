with fct_listen_events as (
    select * from {{ref('int_streamify__listen_events')}}
),
dim_users as (
    select * from {{ref('dim_streamify__users')}}
),
dim_contents as (
    select * from {{ref('dim_streamify__contents')}}
)

select top 10
    fl.song_id as song_id,
    concat(
        dc.song_name, ' (', dc.artist_name, ')'
    ) as content,
    avg(fl.duration_minutes) as avg_duration,
    ((count(user_id) - sum(fl.is_valid_play)) * 100.0 / count(fl.song_id)) as skip_rate_pct
from fct_listen_events fl 
left join dim_contents dc 
using (song_id)
group by song_id, content
having count(user_id) > 1000
order by avg_duration desc, skip_rate_pct asc

