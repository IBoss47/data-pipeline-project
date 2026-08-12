with listen_events as (
    select * from {{ref('int_streamify__listen_events')}}
),
paid_users as (
    select 
        user_id,
        count(distinct song_id) as count_song
    from listen_events
    where count_level > 1
        and current_level = 'paid'
    group by user_id
),
before_paid as (
    select 
        user_id,
        count(distinct song_id) as count_song
    from listen_events 
    where user_id in (select user_id from paid_users)
        and level_on_event = 'free'
    group by user_id
)

select
    user_id,
    be.count_song as count_before_paid,
    pu.count_song as count_after_paid,
    pu.count_song - be.count_song as growth_volume,
    avg(growth_volume) over() as avg_growth_volume
from before_paid be
inner join paid_users pu using(user_id)
order by user_id