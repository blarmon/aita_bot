import json

def log_error(time_stamp, error):

    with open('logs.txt', 'a') as logs_file:
        error_dic = {'time_stamp': time_stamp,
                    'error': error
                    }

        error_json = json.dumps(error_dic)

        logs_file.write(error_json)

        logs_file.close()
