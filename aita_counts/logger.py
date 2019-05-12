import json

def log_error(time_stamp, error, source, thread_lock):

    with open('logs.txt', 'a') as logs_file:
        thread_lock.acquire()

        error_dic = {'time_stamp': time_stamp,
                    'error': error,
                     'source': source
                    }

        error_json = json.dumps(error_dic)

        logs_file.write(error_json)

        logs_file.close()

        thread_lock.release()
