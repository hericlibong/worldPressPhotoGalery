

import os
import sys
import subprocess

# Récupérer le chemin complet du projet Django "gallery"
django_project_path = os.path.abspath('/Users/mac/WORLDPRESSPHOTO/src/gallery')
sys.path.insert(0, django_project_path)
    
# Lancer les spiders Scrapy à partir du projet Django
spiders = ['guardian_picture', 'smh_picture', 'cnn_week_pics', 'atlantic_pictures', 'washpost_picture',
           'letemps_pictures', 'theweek_pictures']
processes = []

for spider in spiders:
    cmd = ['scrapy', 'crawl', spider]
    process = subprocess.Popen(cmd, cwd=django_project_path)
    processes.append(process)

for process in processes:
    process.wait()




