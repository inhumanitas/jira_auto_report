INSTALLATION
============

# Getting sources
    $ git clone https://github.com/inhumanitas/jira_auto_report

# Install package
    $ cd jira_auto_report
    $ python setup.py install

    
SET VARIABLES
=============

Edit before installation settings file 

    $ cp /etc/jira_auto_report/config.yaml.example /etc/jira_auto_report/config.yaml
    $ vi /etc/jira_auto_report/config.yaml

Edit settings:

    # Jira url
    jira_url: 'http://jira.cg.ru'
    # Jira project id
    project_id: 12533
    # Jira login/password
    login: 'login'
    passwd: 'pass'
    # output directory date format
    dir_fmt: '%m.%d'
    # report base directory
    base_dir: '/tmp/reports'

USAGE
=====

After installation in environment package installs script - jira_auto_report
Just run it to start download reports:

    $ jira_auto_report
