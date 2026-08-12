select 
    1
from {{ref('mart_level_listening_volume')}}
where count_after_paid < 0 
    or count_before_paid < 0