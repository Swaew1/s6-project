CREATE TABLE VT2610287BD414__DWH.l_user_group_activity (
    hk_l_user_group_activity int PRIMARY KEY,
    hk_user_id int NOT NULL CONSTRAINT fk_user_group_activity_user REFERENCES VT2610287BD414__DWH.h_users(hk_user_id),
    hk_group_id int NOT NULL CONSTRAINT fk_user_group_activity_group REFERENCES VT2610287BD414__DWH.h_groups(hk_group_id),
    load_dt datetime,
    load_src varchar(20)
)
ORDER BY load_dt
SEGMENTED BY hk_l_user_group_activity ALL NODES
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);