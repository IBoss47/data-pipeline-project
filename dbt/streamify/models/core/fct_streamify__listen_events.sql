with listen_events as (
    select * from {{ ref('int_streamify__listen_events') }}
)

select 
    user_id,
    event_id,
    song_id,
    state,
    duration_minutes,
    time_stamp,
    date_day,
    day,
    month,
    year,
    is_valid_play
from listen_events
