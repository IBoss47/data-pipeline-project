with listen_events as (
    select * from {{ref('stg_streamify__listen_events')}}
)

select
    -- users
    user_id,
    concat(first_name, ' ', last_name) as full_name,
    gender,
    city,
    state,
    zip,
    lat,
    lon,

    -- song and artist
    hex(MD5(concat(artist, '-', song))) as song_id,
    song,
    artist,

    -- events
    hex(MD5(concat(toString(user_id), '-', toString(time_stamp)))) as event_id,
    time_stamp,
    day,
    month,
    year,
    duration / 60 as duration_minutes,
    case 
        when duration >= 30 then 1
        else 0
    end as is_valid_play

from listen_events 
where artist is not null and song is not null