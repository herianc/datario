from prefect import Flow
from prefect.schedules import CronSchedule

from tasks import get_data, load_to_database, parse_data, process_data, save_report, run_dbt

every_minute = CronSchedule(cron="* * * * *")

with Flow("DIT: Pipeline BRT", schedule=every_minute) as brt_flow:

    data = get_data()
    df_raw = parse_data(data)
    filepath = save_report(df_raw)
    df_cleaned = process_data(filepath)
    flag = load_to_database(df_cleaned)
    run_dbt(flag)

    