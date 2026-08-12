select 
    1 
from {{ref('mart_total_duration_play_count_for_each_user_type')}} 
where total_listen_hour < 0