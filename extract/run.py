from flows import brt_flow

if __name__ == "__main__":

    # `Prefect run -p run.py -s` para executar o flow com o scheduler
    brt_flow.run(run_on_schedule=True)