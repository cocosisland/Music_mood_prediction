import numpy as np
import pandas as pd

# =============================================================================
# Here is the class "Get_data" which allows to create an "artist" object. 
# This object has multiple albums containing multiple tracks, with various informations about them.
# =============================================================================


class Get_data:
    
         
    def __init__(self, artist_name):        
        self._artist_name = artist_name

        

    # get artist's ID from his name
    def get_artist_id(self, sp):
    
        results = sp.search(q = 'artist:' + self._artist_name, type = 'artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print(artist['name'], '\n', artist['uri'])   # spotify:artist:6XpaIBNiVzIetEPCWDvAFP
            #artist_id = artist['uri'].split(':')[2]
            artist_id = artist['id']
            
        return artist_id
    
    

    
    # ATTENTION CODE POUR UN SEUL ALBUM POUR LE MOMENT - A ARRANGER POUR PLUS
    def get_albums_id(self, sp, artist_id, limit):
        print('hahahahha')
        albums_results = sp.artist_albums(artist_id, limit=1)
        print(list(albums_results.keys()))  # ['href', 'items', 'limit', 'next', 'offset', 'previous', 'total']
          
        # =============================================================================
        #         inside the main dictionary, access 'items' key. 
        #         'items' has a unique value which is a list of a single element containing 
        #         a nested dictionary from which we access to the value of the key 'id'
        # =============================================================================
        album_id = albums_results.get('items', {})[0].get('id') 
        
        # we can also access to the its name, if needed
        album_name = albums_results.get('items', {})[0].get('name')
        
        print(album_id + '\n' + album_name)
        
        return album_id
    
    
    
    
    def get_tracks_id(self, sp, album_id):
       
        tracks_results = sp.album_tracks(album_id)
        print(tracks_results)
        
        return tracks_results
        


# extract features from tracks
# sp.audio_features(track_uri)[0]
# https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50
