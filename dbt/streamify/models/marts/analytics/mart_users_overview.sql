with fct_listen_events as (
    select * from {{ref('fct_streamify__listen_events')}}
),
dim_users as (
    select * from {{ref('dim_streamify__users')}}
)

select 
    fl.date_day as date_day,
    count(distinct fl.user_id) as total_users_by_month,
    
    count(
        distinct 
        case 
            when du.current_level = 'free' then user_id
        end
    ) as total_free_users_by_month,

    count(
        distinct 
        case 
            when du.current_level = 'paid' then user_id
        end
    ) as total_paid_users_by_month,

    round(total_paid_users / total_users, 2) as conversion_rate_pct,

    sum(total_users_by_month) over() as total_users,
    sum(total_paid_users_by_month) over() as total_paid_users,
    sum(total_free_users_by_month) over() as total_free_users

from fct_listen_events fl 
inner join dim_users du using(user_id)
group by date_day
order by date_day


