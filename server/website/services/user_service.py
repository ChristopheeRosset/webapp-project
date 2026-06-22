import pandas as pd
from server.website.models import User,Vocabulary, db
from flask import session, request

def upload_csv_into_profile(data, userId):
    try:
        #Create Dataframe with pandas lib
        df = pd.read_csv(data)
        #Convert Dataframe to list of dicts for html rendering
        vocabulary_data = df.to_dict(orient='records')

        #Store the vocabulary data in DB vocabulary table using df
        voc_entries = []
        for data in vocabulary_data:
            word = data.get("Word")
            reading = data.get("Reading")
            meaning = data.get("Meaning")

            # Create 
            voc_entries.append(
                 Vocabulary(user_id = userId, word=word, reading=reading, meaning=meaning)
            )

        # Add entries to the table vocabulary
        db.session.add_all(voc_entries)
        db.session.commit()
        
        if voc_entries is not None:
            return True
        else:
            return False
         
    except Exception as e:
        print(f"Error uploading CSV: {e}")
        return None

def get_user_vocabulary (userId):
    voc = db.session.execute(db.select(Vocabulary).filter_by(user_id=userId)).scalars()
    vocabulary_data = [
        {
            "id": v.id,
            "Word": v.word,
            "Reading": v.reading,
            "Meaning": v.meaning
        }
        for v in voc
    ]

    return vocabulary_data

def save_voc (userId):
    vocs = db.session.execute(db.select(Vocabulary).filter_by(user_id=userId)).scalars().all()
    for voc in vocs:
        word_value = request.form.get(f"word-{voc.id}")
        reading_value = request.form.get(f"reading-{voc.id}")
        meaning_value = request.form.get(f"meaning-{voc.id}")

        if word_value is not None:
            voc.word = word_value
        if reading_value is not None:
            voc.reading = reading_value
        if meaning_value is not None:
            voc.meaning = meaning_value
    
    db.session.commit()