# coding: utf-8

from __future__ import unicode_literals

import datetime
import os

import yaml

# Jira url
jira_url = 'http://jira.cg.ru'
# Jira project id
project_id = 12533
# Jira login/password
login, passwd = 'login', 'pass'
# output directory date format
dir_fmt = '%m.%d'
# report base directory
base_dir = '/tmp/reports'

# send mail to recipient
recipient = None
mail_server_url = None
user_mail = None
user_password = None


local_settings_file = '/etc/jira_auto_report/config.yaml'


def update(path):
    config = yaml.load(open(path))
    gl = globals()
    for key, value in config.iteritems():
        if key in gl:
            if isinstance(value, dict):
                for k, v in value.iteritems():
                    gl[key][k] = v
            else:
                gl[key] = value

if os.path.exists(local_settings_file):
    update(local_settings_file)
elif os.path.exists('config.yaml'):
    update('config.yaml')


from_mail = globals().get('from_mail', user_mail)

mail_message_temlate = '''Reports generate finished!

Working period: {begin} - {end}

Generated files:
{file_list}
'''

mail_subject_template = 'Jira auto report: {begin} - {end}'

report_begin_map = {
    0: -3,
    1: -4,
    2: -5,
    3: -6,
    4: -7,
    5: -1,
    6: -2,
}


report_end_map = {
    0: 3,
    1: 2,
    2: 1,
    3: 0,
    4: -1,
    5: 5,
    6: 4,
}


def get_period(today=None):
    """ Get report period from last friday to next thursday
    :param today: custom current date
    :return: tuple such as (last_friday_date, next_thursday_date)
    """
    if not today:
        today = datetime.date.today()

    start_date, end_date = today, today

    today_weekday = today.weekday()
    start_date += datetime.timedelta(report_begin_map[today_weekday])
    end_date += datetime.timedelta(report_end_map[today_weekday])

    return start_date, end_date


def run_test():
    start_date = datetime.date(day=1, month=1, year=2016)
    end_date = datetime.date(day=7, month=1, year=2016)

    # test min
    day = datetime.date(day=1, month=1, year=2016)
    s, e = get_period(day)
    assert s == datetime.date(day=25, month=12, year=2015)
    assert e == datetime.date(day=31, month=12, year=2015)

    # test max
    day = datetime.date(day=7, month=1, year=2016)
    s, e = get_period(day)

    assert s == start_date and e == day

    # test in period
    day = datetime.date(day=3, month=1, year=2016)
    s, e = get_period(day)

    assert s == start_date and e == end_date

    # test in period different date
    day = datetime.date(day=5, month=1, year=2016)
    s, e = get_period(day)

    assert s == start_date and e == end_date

    # test in outer period
    day = datetime.date(day=9, month=1, year=2016)
    s, e = get_period(day)

    assert s == datetime.date(day=8, month=1, year=2016)
    assert e == datetime.date(day=14, month=1, year=2016)


if __name__ == '__main__':
    run_test()
