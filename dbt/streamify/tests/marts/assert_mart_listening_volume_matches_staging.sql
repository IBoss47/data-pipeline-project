with staging_events as (
    select 
        e.duration,
        s.region
    from {{ ref('stg_streamify__listen_events') }} e
    left join {{ ref('dim_streamify__state') }} s
        on e.state = s.state_id
    where e.artist is not null 
      and e.song is not null
      and s.region is not null 
),
staging_total as (
    select 
        sum(duration) / 3600 as total_hours_stg
    from staging_events
),
mart_total as (
    select 
        sum(total_hours) as total_hours_mart
    from {{ ref('mart_listening_volume_by_region_and_day') }}
)

select 
    1
from staging_total stg
cross join mart_total m
where abs(stg.total_hours_stg - coalesce(m.total_hours_mart, 0)) > 0.01
