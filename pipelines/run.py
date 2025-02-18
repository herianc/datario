from flows import brt_captura_flow, brt_dbt_flow

if __name__ == "__main__":

    brt_captura_flow.run(run_on_schedule=True)
    brt_dbt_flow.run(run_on_schedule=True)

 