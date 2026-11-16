# Проектная работа 6 спринта: DWH на базе Vertica и Data Vault

## Описание проекта
В рамках проекта реализован ETL-пайплайн для загрузки логов активности пользователей в группах (`group_log.csv`) из S3-хранилища в аналитическое хранилище данных на базе **Vertica**, спроектированное по методологии **Data Vault**. Итоговая цель — расчёт конверсии пользователей из вступления в группу в отправку сообщений (`group_conversion`) для 10 самых ранних сообществ.

## Стек технологий
* **Хранилище данных:** Vertica (методология Data Vault: слои `STAGING` и `DWH`)
* **Оркестрация:** Apache Airflow
* **Языки и библиотеки:** Python (`pandas`, `vertica-python`, `boto3`), SQL

## Структура репозитория
* `dags/sprint6_project_get_data_dag.py` — DAG для выгрузки файла `group_log.csv` из S3 в локальную директорию.
* `dags/sprint6_project_load_staging_dag.py` — DAG для предобработки данных (приведение `user_id_from` к типу `Int64`) и загрузки в staging-слой (`COPY ... FROM STDIN`).
* `group_log.sql` — DDL-скрипт создания таблицы `group_log` в схеме `*__STAGING`.
* `l_user_group_activity.sql` — DDL-скрипт создания таблицы связи (Link) `l_user_group_activity` в схеме `*__DWH`.
* `insert_data_l_user_group_activity.sql` — скрипт миграции данных из `*__STAGING.group_log` в линк `l_user_group_activity`.
* `s_auth_history.sql` — DDL-скрипт создания и скрипт наполнения сателлита (Satellite) `s_auth_history` историей событий (`create`, `add`, `leave`).
* `7.1_cnt_users_in_group_with_messages.sql` — CTE `user_group_messages` для подсчёта уникальных активных авторов в группах.
* `7.2_cnt_added_users.sql` — CTE `user_group_log` для подсчёта вступивших пользователей в 10 самых ранних группах.
* `7.3_group_conversin.sql` — итоговый аналитический запрос для расчёта метрики `group_conversion`.