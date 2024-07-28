import subprocess

spiders = ['guardian_picture', 'smh_picture', 'cnn_week_pics', 'atlantic_pictures',  
         'theweek_pictures']

processes = []
for spider in spiders:
    cmd = ['scrapy', 'crawl', spider]
    process = subprocess.Popen(cmd)
    processes.append(process)
    
for process in processes:
    process.wait()