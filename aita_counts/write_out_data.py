import json

def write_new_comment(time_stamp, body, called_by, submission_id, thread_lock):

    with open('data.txt', 'a') as data_file:
        thread_lock.acquire()
        data_dic = {'time_stamp': time_stamp,
                    'body': body,
                    'called_by': called_by,
                    'submission_id': submission_id
                    }

        data_json = json.dumps(data_dic)

        data_file.write(data_json)

        data_file.close()

        thread_lock.release()
