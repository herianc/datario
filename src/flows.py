from prefect import Flow
from tasks import get_data, parse_data, save_report, process_data, load_to_database


with Flow("DIT: BRT - Regitros") as brt_flow:
    
    data = get_data()
    df_raw = parse_data(data)
    filepath = save_report(df_raw)
    df_cleaned = process_data(filepath)
    load_to_database(df_cleaned)