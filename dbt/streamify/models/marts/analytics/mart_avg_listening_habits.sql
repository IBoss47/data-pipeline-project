with listen_events as (
    select * from {{ref('int_streamify__listen_events')}}
),
paid_users as (
    select distinct user_id
    from listen_events
    where level_on_event = 'paid'
),
songs_per_user as (
    select 
        l.level_on_event as type,
        l.user_id,
        count(*) as song_count
    from listen_events l
    inner join paid_users p on l.user_id = p.user_id
    where l.level_on_event in ('free', 'paid')
    group by l.level_on_event, l.user_id
)
select 
    type,
    round(avg(song_count), 2) as avg_song
from songs_per_user
group by type
order by type desc;