from prefect import Flow
from prefect.schedules import CronSchedule

from tasks import (free_up_report_storage, get_data, load_to_database,
                   parse_data, process_data, run_dbt, save_report)

every_minute = CronSchedule(cron="* * * * *")

with Flow("DIT: BRT GPS - Captura", schedule=every_minute) as brt_captura_flow:
    """
    Fluxo para captura dos dados de GPS do BRT. Ocorre a cada minuto
    """

    api_content = get_data()
    df_raw = parse_data(api_content)
    filepath = save_report(df_raw)
    df_cleaned = process_data(filepath)
    load_to_database(df_cleaned)


every_five_minutes = CronSchedule(cron="*/5 * * * *")
with Flow("DIT: BRT GPS - Materialização", schedule=every_five_minutes) as brt_dbt_flow:
    """
    Fluxo para materialização dos modelos DBT. É executado a cada 5 minutos.
    Em um cenário real, sua execução seria diária, mas para motivos de teste está ocorrendo a cada 5 minutos.
    """
    run_dbt()

every_month = CronSchedule(cron="0 0 1 * *")
with Flow(
    "DIT: BRT GPS - Liberação de espaço de armazenamento", schedule=every_month
) as janitor_flow:
    """
    Fluxo para liberação de espaço de armazenamento no diretório de salvamento dos CSVs.
    É executado mensalmente.
    """
    free_up_report_storage()
