with listen_events as (
    select * from {{ref('stg_streamify__listen_events')}}
),
rank_users as (
    select 
        user_id,
        first_name,
        last_name,
        gender,
        city,
        state,
        zip,
        lat,
        lon,
        level,
        row_number() over(
            partition by user_id 
            order by time_stamp desc
        ) as rn
    from {{ref('stg_streamify__listen_events')}}
    where user_id is not null
     
),
users as (
    select 
        *
    from rank_users
    where rn = 1
)

select
    -- users
    l.user_id as user_id,
    concat(l.first_name, ' ', l.last_name) as full_name,
    l.gender as gender,
    l.level as level,
    l.city as city,
    l.state as state,
    l.zip as zip,
    l.lat as lat,
    l.lon as lon, 

    -- song and artist
    hex(MD5(concat(l.artist, '-', l.song))) as song_id,
    l.song as song,
    l.artist as artist,

    -- events
    hex(MD5(concat(coalesce(toString(l.user_id), 'guest'), '-', toString(l.time_stamp)))) as event_id,
    l.time_stamp as time_stamp,
    l.day as day,
    l.month as month,
    l.year as year,
    l.duration / 60 as duration_minutes,
    case 
        when l.duration >= 30 then 1
        else 0
    end as is_valid_play

from listen_events l
left join users u
using (user_id)
where artist is not null 
    and song is not null