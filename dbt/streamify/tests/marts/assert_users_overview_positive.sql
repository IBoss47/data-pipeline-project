-- Total users by month should be greater than or equal to 0
select
    1
from {{ ref('mart_users_overview') }}
where total_users_by_month < 0
