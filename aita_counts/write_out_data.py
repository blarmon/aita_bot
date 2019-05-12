import json

def write_new_comment(time_stamp, body, ):

    with open('data.txt', 'a') as data_file:
        data_dic = {'time_stamp': time_stamp,
                    'body': body
                    }

        data_json = json.dumps(data_dic)

        data_file.write(data_json)

        data_file.close()
