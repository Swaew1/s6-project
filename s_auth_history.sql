CREATE TABLE VT2610287BD414__DWH.s_auth_history (
	hk_l_user_group_activity int NOT NULL CONSTRAINT fk_s_auth_history_l_user_group_activity REFERENCES VT2610287BD414__DWH.l_user_group_activity(hk_l_user_group_activity),
	user_id_from int, 
	event varchar(10), 
	event_dt datetime, 
	load_dt datetime, 
	load_src varchar(20)
)
ORDER BY load_dt
segmented BY hk_l_user_group_activity ALL nodes 
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

INSERT INTO VT2610287BD414__DWH.s_auth_history (
    hk_l_user_group_activity,
    user_id_from,
    event,
    event_dt,
    load_dt,
    load_src
)
SELECT
    luga.hk_l_user_group_activity,
    gl.user_id_from,
    gl.event,
    gl.datetime AS event_dt,
    now() AS load_dt,
    's3' AS load_src
FROM VT2610287BD414__STAGING.group_log AS gl
LEFT JOIN VT2610287BD414__DWH.h_groups AS hg
    ON gl.group_id = hg.group_id
LEFT JOIN VT2610287BD414__DWH.h_users AS hu
    ON gl.user_id = hu.user_id
LEFT JOIN VT2610287BD414__DWH.l_user_group_activity AS luga
    ON hg.hk_group_id = luga.hk_group_id
   AND hu.hk_user_id = luga.hk_user_id
WHERE luga.hk_l_user_group_activity IS NOT NULL;