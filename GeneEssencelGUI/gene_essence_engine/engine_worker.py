from gene_essence_engine.engine_software import engine_software


def engine_worker(data, queue):
    def log_callback(message, progress=None):
        queue.put({'message': message, 'progress': progress})
    engine_software(data, log_callback=log_callback)
    queue.put({'done': True})
