# WorldPressPhotoGallery

<p align="center">
  <img src="media/worldpressphoto.PNG" alt="worldpressphoto" width="600" height="400">
</p>

**WorldPressPhotoGallery** is a web application designed for photojournalism enthusiasts. It allows users to view, select, and vote for the most striking news images, highlighted for their photojournalistic impact.

Each week, we collect these emblematic images from the weekly selections of major media outlets. This collection is performed through scraping, using Scrapy, to gather the most compelling works of global photojournalism. Subsequently, with Django, we provide an interface where users can interact with these images, assess them, and soon, share their impressions.

## Main Features

- **Voting and Rating:** Registered users can vote for their favorite images and rate them on a scale from 1 to 10.

## Technology

This application utilizes Scrapy to collect images through spiders dedicated to each media outlet. The images are processed via Scrapy items before being sent to the database.

  - **Scrapy:** Collects images via individual spiders.
  - **Django:** The collected images are stored in a SQLite3 database and managed by a model of the framework, then displayed in the views and templates.

## Supported Media

The list of supported media includes renowned international publications:

- Washington Post (USA)
- Sydney Morning Herald (Australia)
- CNN (USA)
- Le Temps (Switzerland)
- The Week Pictures (USA)
- Guardian (UK)
- Atlantic (USA)
- Spiegel (Germany)
- Die Welt (Germany)

These publications source images from major international news agencies, including:

- Associated Press (AP)
- Reuters
- Agence France-Presse (AFP)
- Getty Images
- European Pressphoto Agency (EPA)



# Installation and Usage Instructions

## Clone the repository
In the terminal:  
```console
git clone https://github.com/hericlibong/worldPressPhotoGalery
```

**Navigate to the directory** 
Change into the directory with:
```console
cd worldPressPhotoGalery
```

**Create a virtual environment**
```console
`python -m venv venv`
```

**Activate the virtual environment**:
On Windows:
```console
`venv\Scripts\activate
````
On Unix or MacOS: 
```console
`source venv/bin/activate`
```

**Update the database with the latest images** 
Execute:
```console
`python run_spiders.py`
```
 
**Navigate to the `src` directory**: 
Change directories with:
`cd src`

**Start the Django server**: 
```console
`python manage.py runserver`
```

**Access the application**: 
After starting the server, open your web browser and go to:
`http://127.0.0.1:8000/`
to enjoy browsing and voting on photojournalistic images.


