with listen_events as (
    select * from {{ ref('int_streamify__listen_events') }}
)

select distinct
    song_id,
    song as song_name,
    artist as artist_name
from listen_events
where song_id is not null