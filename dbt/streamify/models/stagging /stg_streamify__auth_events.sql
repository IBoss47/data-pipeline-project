with rename as (
    select 
        ts as time_stamp,
        cast(sessionId as UInt64) as session_id,
        lower(trim(level)) as level,
        itemInSession as items_in_session,
        lower(trim(city)) as city,
        cast(zip as Nullable(String)) as zip,
        lower(trim(state)) as state,
        lower(trim(userAgent)) as user_agent,
        lon,
        lat,
        cast(userId as Nullable(UInt64)) as user_id,
        lower(trim(lastName)) as last_name,
        lower(trim(firstName)) as first_name,
        case
            when lower(trim(gender)) = 'f' then 'female'
            when lower(trim(gender)) = 'm' then 'male'
        end as gender,
        cast(registration as Nullable(String)) as registration,
        success,
        year,
        month,
        hour,
        day
    from {{source('stg_streamify', 'raw_auth_events')}}
)

select 
    time_stamp,
    session_id,
    nullif(level, '') as level,
    items_in_session,
    nullif(city, '') as city,
    nullif(lower(trim(zip)), '') as zip,
    nullif(state, '') as state,
    nullif(user_agent, '') as user_agent,
    lon,
    lat,
    user_id,
    nullif(first_name, '') as first_name,
    nullif(last_name, '') as last_name,
    nullif(gender, '') as gender,
    nullif(registration, '') as registration,
    success,
    year,
    month,
    hour,
    day
from rename













