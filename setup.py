# coding: utf-8
import shutil
import os
from setuptools import setup, find_packages


def process_dir(from_path, dest_path='/'):
    for root, dirs, files in os.walk(from_path):
        for d in dirs:
            try:
                os.mkdir(os.path.join(dest_path, root, d))
            except OSError:
                pass

        for f in files:
            try:
                shutil.copy(os.path.join(root, f),
                            os.path.join(dest_path, root, f))
            except IOError:
                pass

process_dir('etc/')


setup(
    name='jira_auto_report',
    version='0.1',
    description='Automation for report launch',
    author='inhumanitas',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    install_requires=['jira', 'pyyaml'],
    entry_points={
        'console_scripts': [
            'jira_auto_report = jira_auto_report.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: CLI Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
