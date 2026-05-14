from gene_essence_engine.engine_worker import engine_worker

def run_engine_in_subprocess(data, queue):
    engine_worker(data, queue)
