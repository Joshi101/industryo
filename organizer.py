from io import BytesIO
from PIL import Image
import csv
import os
import django
import re
from django.core.files.base import ContentFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "industryo.settings")
django.setup()

from cleaning.models import HTML, PY
from nodes.models import Images


def new_csv(result, name):
    with open(name+'.csv', 'w', newline='') as f:
        # w = csv.DictWriter(f, result.keys())
        # w.writeheader()
        w = csv.writer(f)
        w.writerow(result)


def check_in(list1, list2):
    """
    Checks if items in 'list1' list exists in 'list2' list
    """
    for ex in list2:
        if ex in list1:
            return True
    return False


def get_file(path='.', exclude_path=[], exclude_files=[], include_types=[]):
    """
    Gets files starting from 'path' directory where
    the directory is not in 'exclude_path'
    the file is not in 'exclude_file'
    the filetype is in 'include_types'
    """
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        if check_in(dirpath, exclude_path):
            print('> Excluding Path : '+dirpath)
            continue
        c = 0
        dirpath = dirpath.replace("\\", "/")
        print('> Checking Path : '+dirpath)
        for filename in filenames:
            ext = filename.split('.')[-1]
            if not check_in(filename, exclude_files) and check_in(ext, include_types):
                files.append({'filename': filename, 'dirpath': dirpath})
                c += 1
        print('Found '+str(c)+' files')
    return files


def crawl_templates():
    """
    Crawls the directory for all the html files and create any new entries in
    the table if they don't exist.
    """
    files = get_file(path='./templates', exclude_path=['static'], include_types=['html'])
    for file in files:
        try:
            HTML.objects.get(name=file['filename'], path=file['dirpath'])
        except:
            HTML.objects.create(name=file['filename'], path=file['dirpath'])


def crawl_py():
    """
    Crawls the directory for all the '.py' files and create any new entries in
    the table if they don't exist.
    """
    files = get_file(
            path='.',
            exclude_path=['.git', '.idea', '__pycache__', 'migrations', 'img', 'images',
                          'docs', 'tests', 'templates'],
            exclude_files=['__init__.py', 'manage.py', 'organizer.py'],
            include_types=['py'])
    for file in files:
        print('++ Creating ', file)
        try:
            PY.objects.get(name=file['filename'], path=file['dirpath'])
        except:
            PY.objects.create(name=file['filename'], path=file['dirpath'])


def find_pattern(path, patterns):
    """
    find patterns within a file at 'path'
    """
    results = []
    with open(path) as f:
        data = f.read()
        for p in patterns:
            results.append(re.findall(p, data))
    return results


def template_calls():
    """
    finding out the calls to other template files withing a template file
    via 'include' and 'extend'
    """
    patterns = ['{% include (.*\.html)', '{% extends (.*\.html)']
    files = HTML.objects.all()
    for file in files:
        print("> Scanning file : "+file.complete_path)
        found = find_pattern(file.complete_path, patterns)
        for finding in found[0]:
            p = './templates/'+finding.strip('"\'')
            print("- Found Include : "+p)
            try:
                inc = HTML.objects.get(complete_path=p)
                if inc not in file.includes.all():
                    file.includes.add(inc)
                    print('++ Added include')
            except:
                print("** Include call for, "+p+" doesn't exist")

        for finding in found[1]:
            p = './templates/'+finding.strip('"\'')
            print("- Found Extend : "+p)
            try:
                inc = HTML.objects.get(complete_path=p)
                if inc not in file.extends.all():
                    file.extends.add(inc)
                    print('++ Added extend')
            except:
                print("** Extend call for, "+p+" doesn't exist")


def py_temp_calls():
    """
    finding out the calls to other template files withing a template file
    via 'include' and 'extend'
    """
    patterns = ['["\'](\S*\.html)["\']']
    files = PY.objects.all()
    for file in files:
        print("> Scanning file : "+file.complete_path)
        found = find_pattern(file.complete_path, patterns)
        for finding in found[0]:
            p = './templates/'+finding.strip('"\'')
            print("- Found Include : "+p)
            try:
                inc = HTML.objects.get(complete_path=p)
                if inc not in file.includes_temp.all():
                    file.includes_temp.add(inc)
                    print('++ Added include')
            except:
                print("** Include call for, "+p+" doesn't exist")


def dead_templates():
    for page in HTML.objects.all():
        if not os.path.exists(page.complete_path):
            page.delete()
            print("-- Deleted "+page.complete_path)


def all_includes(html):
    result = []
    for p in html.includes.all():
        if p.includes.all().exists():
            result.extend(all_includes(p))
        result.append(p)
    return result


def all_extends(html):
    result = []
    for p in html.extends.all():
        if p.extends.all().exists():
            result.extend(all_extends(p))
        result.append(p)
    return result


def py_templates():
    direct = []
    for page in PY.objects.all():
        for html in page.includes_temp.all():
            direct.append(html)
            direct.extend(all_includes(html))
            direct.extend(all_extends(html))
    used = set(direct)
    all_temp = set(HTML.objects.all())
    dead = all_temp.difference(used)
    # new_csv(direct, 'used_templates')
    dead_names = []
    for i in dead:
        dead_names.append(i.complete_path)
    dead_names.sort()
    for i in dead_names:
        print(i)


THUMB_SIZES = [
    (233, 233),
    (89, 89),
    (34, 34)
]


def crawl_images():
    """
    Crawls the model for all the image files
    """
    images = Images.objects.all()
    for i in images:
        if not i.image:
            print('** Image not available for id : '+str(i.id))
        else:
            if not i.image_thumbnail_xs:
                try:
                    file = Image.open(i.image)
                    name = i.image.name
                    f_format = file.format
                    i.image_format = f_format
                    thumb = []
                    for size in THUMB_SIZES:
                        f_thumb = file
                        f_thumb.thumbnail(size, resample=2)
                        thumb_io = BytesIO()
                        if f_format == 'JPEG':
                            f_thumb.save(thumb_io, f_format, optimize=True, progressive=True)
                        else:
                            f_thumb.save(thumb_io, f_format, optimize=True)
                        thumb.append(thumb_io)
                    i.image_thumbnail.save(name, content=ContentFile(thumb[0].getvalue()))
                    i.image_thumbnail_sm.save(name, content=ContentFile(thumb[1].getvalue()))
                    i.image_thumbnail_xs.save(name, content=ContentFile(thumb[2].getvalue()))
                    i.save()
                    print('++ Images created for id : '+str(i.id))
                    print('   '+i.image.name)
                except FileNotFoundError:
                    print('-- File not found for id : '+str(i.id))
            else:
                print(">> All good for id: "+str(i.id))
