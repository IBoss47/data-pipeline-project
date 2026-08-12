with listen_events as (
    select 
        * 
    from {{ ref('int_streamify__listen_events') }}
    where user_id is not null
),
dedup as (
    select 
        user_id,
        current_level,
        full_name,
        gender,
        city,
        state,
        lat,
        lon,
        row_number() over(
            partition by user_id 
            order by time_stamp desc
        ) as rn
    from listen_events
)

select distinct
    user_id,
    current_level,
    full_name,
    gender,
    city,
    state,
    lat,
    lon
from dedup
where user_id is not null 
    and rn = 1