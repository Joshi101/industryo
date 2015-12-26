from django.shortcuts import render, redirect
import os
import subprocess


def task_exec(request):
    print('oye bubbly')
    # os.system('cd ..')
    # subprocess.call(['python manage.py process_tasks'])
    subprocess.Popen('python manage.py process_tasks')
    print('oye oye bubbly')
    return redirect('/')