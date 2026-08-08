with rename as (
    select 
        ts as time_stamp,
        cast(sessionId as UInt64) as session_id,
        lower(trim(page)) as page,
        lower(trim(auth)) as auth,
        lower(trim(method)) as method,
        status,
        lower(trim(level)) as level,
        itemInSession as items_in_session,
        lower(trim(city)) as city,
        cast(zip as Nullable(String)) as zip,
        lower(trim(state)) as state,
        lower(trim(userAgent)) as user_agent,
        lon,
        lat,
        userId as user_id,
        lower(trim(lastName)) as last_name,
        lower(trim(firstName)) as first_name,
        case
            when lower(trim(gender)) = 'f' then 'female'
            when lower(trim(gender)) = 'm' then 'male'
        end as gender,
        cast(registration as Nullable(String)) as registration,
        lower(trim(artist)) as artist,
        lower(trim(song)) as song,
        duration,
        year,
        month,
        hour,
        day
    from {{source('stg_streamify', 'raw_page_view_events')}}
)

select 
    time_stamp,
    session_id,
    nullif(page, '') as page,
    nullif(auth, '') as auth,
    nullif(method, '') as method,
    status,
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
    nullif(artist, '') as artist,
    nullif(song, '') as song,
    duration,
    year,
    month,
    hour,
    day
from rename













