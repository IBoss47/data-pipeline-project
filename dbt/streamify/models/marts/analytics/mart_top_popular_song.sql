with fct_listen_events as (
    select * from {{ref('fct_streamify__listen_events')}}
),
dim_contents as (
    select * from {{ref('dim_streamify__contents')}}
)

select
    dc.song_name,
    count(distinct fl.user_id)
from fct_listen_events fl
inner join dim_contents dc using(song_id)
group by dc.song_name
order by count(distinct fl.user_id) desc
limit 10