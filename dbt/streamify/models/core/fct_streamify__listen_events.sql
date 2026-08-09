with listen_events as (
    select * from {{ ref('int_streamify__listen_events') }}
)

select 
    user_id,
    event_id,
    song_id,
    duration_minutes,
    time_stamp,
    day,
    month,
    year,
    is_valid_play
from listen_events
