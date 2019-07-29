#!/usr/bin/python3
import sys
import os
import re
import pprint


def fuck_tasks(path):
    with open(path) as f:
        content = f.read()
    
    # First, scan for all the methods we have
    task_methods = re.findall(r'^def (.*)\(', content, re.M)

    # Second, find dependencies
    regex_for_task_methods = '|'.join(f'(?:{tm})' for tm in task_methods)
    split_content = content.split('\ndef ')
    dependencies = {}
    for code_block in split_content[1:]:
        method, body = code_block.split('\n', 1)
        method_title = re.match(regex_for_task_methods, method)
        method_calls = re.findall(regex_for_task_methods, body, re.M)
        dependencies[method_title.group()] = set(method_calls) or []

    # Finally, print
    pprint.pprint(dependencies)


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print('Please provide the path to the tasks file')
        exit(1)
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f'Looks like {path} isn\'t a file')
        exit(1)
    fuck_tasks(path)
