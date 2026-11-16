WITH user_group_log AS (
    SELECT
        luga.hk_group_id,
        COUNT(DISTINCT luga.hk_user_id) AS cnt_added_users
    FROM VT2610287BD414__DWH.s_auth_history AS sah
    INNER JOIN VT2610287BD414__DWH.l_user_group_activity AS luga
        ON sah.hk_l_user_group_activity = luga.hk_l_user_group_activity
    WHERE sah.event = 'add'
      AND luga.hk_group_id IN (
          SELECT hk_group_id
          FROM VT2610287BD414__DWH.h_groups
          ORDER BY registration_dt ASC
          LIMIT 10
      )
    GROUP BY luga.hk_group_id
)
SELECT
    hk_group_id,
    cnt_added_users
FROM user_group_log
ORDER BY cnt_added_users
LIMIT 10;