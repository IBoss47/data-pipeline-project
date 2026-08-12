select 
    1
from {{ref('mart_listening_volume_by_region_and_day')}}
where total_hours < 0