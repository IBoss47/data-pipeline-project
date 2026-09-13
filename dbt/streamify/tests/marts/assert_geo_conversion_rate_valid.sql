select
    1
from {{ ref('mart_geo_user_distribution') }}
where conversion_rate_pct < 0 or conversion_rate_pct > 100
