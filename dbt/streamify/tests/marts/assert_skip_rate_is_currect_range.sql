select 
    1
from {{ref('mart_content_performance_metrics')}}
where skip_rate_pct < 0
    or skip_rate_pct > 100