select
    1
from {{ ref('mart_avg_listening_habits') }}
where avg_song < 0
