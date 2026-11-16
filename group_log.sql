CREATE TABLE VT2610287BD414__STAGING.group_log
(
    group_id     int NOT NULL REFERENCES VT2610287BD414__STAGING.groups(id),
    user_id      int NOT NULL REFERENCES VT2610287BD414__STAGING.users(id),
    user_id_from int,
    event        varchar(10),
    datetime     timestamp
)
ORDER BY group_id, user_id
SEGMENTED BY hash(group_id) ALL NODES
PARTITION BY datetime::date
GROUP BY calendar_hierarchy_day(datetime::date, 3, 2);