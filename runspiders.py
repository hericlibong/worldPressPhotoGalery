import os
import subprocess

os.makedirs('json_datas', exist_ok=True)

spiders = [
    'guardian_picture',
    'smh_picture',
    'cnn_week_pics',
    'atlantic_pictures',
    'theweek_pictures'
]

for spider in spiders:
    outfile = f"json_datas/{spider}.json"

    # Scrapy >= 2.9 => on spécifie :json pour indiquer le format
    cmd = [
        'scrapy', 'crawl', spider,
        '-O', f'{outfile}:json',  # Overwrite + JSON format
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

print("All spiders done!")
