# import dateutil.parser
# import getpass
# import json
# import time

# import os, ssl

import datetime
import json
import getpass
import time
import os
import ssl
import config
import re
from pyelice import Elice, EliceResponseError

URL_PATTERN = r'\/courses\/(\d+)\/lectures\/(\d+)\/materials\/(\d+)'

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def parse_target_path(path):
    match = re.search(URL_PATTERN, path)
    course_id = int(match.group(1))
    lecture_id = int(match.group(2))
    order_no = int(match.group(3))
    return {
      'course_id': course_id,
      'lecture_id': lecture_id,
      'order_no': order_no
    }

def parse_target_paths(paths):
    return [parse_target_path(path) for path in paths]

def get_due_timestamp():
    due_datetime = datetime.datetime.strptime(config.due_datetime, r'%Y-%m-%d %H:%M')
    return int(time.mktime(due_datetime.timetuple()) * 1000)

def init_elice(email, organization):
    elice = Elice()
    password = getpass.getpass('%s\'s password: ' % email)
    elice.login(email, password, organization)
    return elice

def load_users(elice, course_id):
    users_iter = elice.get_iter('/common/course/user/list/', {
        'course_id': course_id
    }, lambda x: x['users'])
    users = []
    for user in users_iter:
        users.append(user)
    return users
# max_ts = 0 # DEBUG
def load_usercode_contents_timestamps(elice, exercise, room_id, last_datetime):
    usercode_contents = {}
    usercode_timestamps = {}
    for filename in exercise['exercise_image']['task_filelist']:
        try:
            usercode = elice.get('/common/material_exercise/exercise_usercode/get/', {
                'exercise_room_id': room_id,
                'filename': filename,
                'last_datetime': last_datetime
            })['exercise_usercode']
            content = usercode['content']
            timestamp = usercode['created_datetime']
        except KeyboardInterrupt:
            raise
        except:
            content = None
            timestamp = None
        # global max_ts # DEBUG
        # if max_ts < timestamp: # DEBUG
            # max_ts = timestamp # DEBUG
        usercode_contents[filename] = content
        usercode_timestamps[filename] = timestamp
    return usercode_contents, usercode_timestamps

def init_data_path():
    if not os.path.exists('./data'):
        os.makedirs('./data')

def main():
    init_data_path()
    elice = init_elice(config.email, config.organization)
    targets = parse_target_paths(config.target_paths)

    print('Loading users.')
    # Load users.
    course_ids = set([target['course_id'] for target in targets])
    users_dict = {}
    for course_id in course_ids:
        print('Loading users for course %d.' % course_id)
        users_dict[course_id] = load_users(elice, course_id)

    print('Loading materials.')
    # Load materials.
    materials = []
    for target in targets:
        material = elice.get('/common/lecture_page/get/', {
            'lecture_id': target['lecture_id'],
            'locator_type': 0,
            'order_no': target['order_no']
        })['material_exercise']
        materials.append(material)

    print('Loading code.')
    # Load codes.
    due_timestamp = get_due_timestamp()
    for material_index, material in enumerate(materials):
        result = []
        users = users_dict[material['course_id']]
        for user_index, user in enumerate(users):
            print('Loading code for material %d/%d user %d/%d.' %
                  (material_index + 1, len(materials), user_index + 1, len(users)))
            runnings = elice.get('/common/exercise_running/list/', {
                'material_exercise_id': material['id'],
                'user_id': user['id'],
                'begin_datetime': 0,
                'end_datetime': due_timestamp,
                'offset': 0,
                'count': 1
            })['exercise_runnings']

            if runnings:
                run_datetime = runnings[0]['created_datetime']
                room_id = runnings[0]['exercise_room_id']
                usercode_contents, usercode_timestamps = load_usercode_contents_timestamps(
                    elice, material, room_id, run_datetime)
            else:
                usercode_contents = None
                usercode_timestamps = None

            if 'firstname' not in user:
                user['firstname'] = '__unknown__'
            if 'lastname' not in user:
                user['lastname'] = '__unknown__'
            result.append({
                'user_id': user['id'],
                'firstname': user['firstname'],
                'lastname': user['lastname'],
                'organization_uid': user['organization_uid'],
                'code': usercode_contents,
                'code_update_datetime': usercode_timestamps
            })

        material_title = material['title'].replace(' ', '_').lower()
        code_file_path = './data/%d_%s_code.json' % (material['id'], material_title)
        f = open(code_file_path, 'w')
        f.write(json.dumps(result))
        f.close()

if __name__ == '__main__':
    main()
    # print(max_ts) # DEBUG
