import os
import sqlite3
#import django


class ApipicturesPipeline:
    """"Pipeline to register scraped data in the database sqlite3"""
    
    def __init__(self):
       
        db_path ='src\db.sqlite3'
        self.con = sqlite3.connect(db_path) 
    
        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pictures_photogallery(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            media TEXT,
            sectionTitle TEXT,
            pubDate TEXT,
            pageUrl TEXT,
            caption TEXT,
            location TEXT,
            author TEXT,
            credits TEXT,
            picture TEXT,
            pictureEditor TEXT,
        CONSTRAINT unique_caption_picture UNIQUE (caption, picture)
        )
        """)
           
    
    def process_item(self, item, spider):
        # Vérifier l'existence de l'enregistrement basé sur les colonnes spécifiées
        existing_record = self.cur.execute("""
            SELECT * FROM pictures_photogallery WHERE caption = ? AND picture = ?
        """, (item['caption'], item['picture'])).fetchone()

        if existing_record:
            # Enregistrement existant, éviter l'insertion du doublon
            return item
        else:
            # Insérer le nouvel enregistrement dans la base de données
        
            self.cur.execute("""
                INSERT INTO pictures_photogallery (media, sectionTitle, pubDate, pageUrl, caption, location, author, 
                             credits, picture, pictureEditor) VALUES (?, ?, ?, ?, ?, ?, ? , ?, ?, ?)
            """,
            (
                item['media'],
                item['sectionTitle'],
                item['pubDate'],
                item['pageUrl'],
                item['caption'], 
                item['location'],
                item['author'],
                item['credits'],
                item['picture'],
                item['pictureEditor']
                
            ))

            
            self.con.commit()
            return item
