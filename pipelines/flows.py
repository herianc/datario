from prefect import Flow
from prefect.schedules import CronSchedule

from tasks import get_data, load_to_database, parse_data, process_data, save_report, run_dbt

every_minute = CronSchedule(cron="* * * * *")

with Flow("DIT: BRT GPS - Captura", schedule=every_minute) as brt_captura_flow:
    data = get_data()
    df_raw = parse_data(data)
    filepath = save_report(df_raw)
    df_cleaned = process_data(filepath)
    load_to_database(df_cleaned)


every_ten_minutes = CronSchedule(cron='*/10 * * * *')
with Flow('DIT: BRT GPS - Materialização', schedule=every_ten_minutes) as brt_dbt_flow:
    run_dbt()