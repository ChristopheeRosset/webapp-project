import pandas as pd
from server.website.models import User,Vocabulary, db
from flask import session

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