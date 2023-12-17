import numpy as np
import pandas as pd

# =============================================================================
# Here is the class "Get_data" which allows to create an "artist" object. 
# This object has multiple albums containing multiple tracks, with various informations about them.
# These functions work for one artist at a time.
# =============================================================================


class Get_data:
    
         
    def __init__(self, artist_name):        
        self._artist_name = artist_name

        
    # STEP 1
    # get artist's ID from his name
    def get_artist_id(self, sp):
    
        results = sp.search(q = 'artist:' + self._artist_name, type = 'artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print('************************ ' + artist['name'], '\n', artist['uri'])   # spotify:artist:6XpaIBNiVzIetEPCWDvAFP
            #artist_id = artist['uri'].split(':')[2]
            artist_id = artist['id']
            
        return artist_id
    
    

    
    # STEP 2
    # get artist's albums from artist ID
    def get_albums_ids(self, sp, artist_id, limit=False):

        albums_results_dict = sp.artist_albums(artist_id, limit=limit)
        #print(list(albums_results_dict.keys()))  # ['href', 'items', 'limit', 'next', 'offset', 'previous', 'total']

        # =============================================================================
        #         inside the main dictionary, access 'items' key. 
        #         'items' has a unique value which is a list of a single element containing 
        #         a nested dictionary from which we access to the value of the key 'id'
        # =============================================================================
             
        # create list of albums ids
        albums_ids_list = []
        for album in albums_results_dict['items']:
            albums_ids_list.append(album['id'])
        print(albums_ids_list)
                
        # ***DRAFT***
        # for multiple albums :
        #album_items_list = albums_results.get('items', {})[0:limit]#.get('id')    # NO
        #res = [value['id'] for key, value in albums_results_dict.items() if 'id' in value]
        # it works if 1 album :
        #album_id = albums_results_dict.get('items', {})[0].get('id') 
                
        return albums_ids_list
    
    
    
    # STEP 3    
    # get all tracks URI for each of the artist's album
    def get_tracks_id(self, sp, albums_ids_list):
        
        track_info_dict = {}
        for album_id in albums_ids_list:
            album_name = sp.album(album_id)['name']
            alb_release_date = sp.album(album_id)['release_date']
            print(album_name)
            print('HEYYYYYYYYYYYYYYYYYYY')

            for track in sp.album_tracks(album_id)['items']:
                track_id = track['id']
                #track_name = track['name']
                #print(track_id, track_name)    # type->str
                
                track_info_dict[track_id] = {}
                track_info_dict[track_id]['track_name'] = track['name'] 
                track_info_dict[track_id]['track_number'] = track['track_number']
                track_info_dict[track_id]['track_id'] = track['id']
                track_info_dict[track_id]['album_name'] = album_name
                track_info_dict[track_id]['album_id'] = album_id
                track_info_dict[track_id]['alb_release_date'] = alb_release_date
                print(track_info_dict)
                df = pd.DataFrame.from_dict(track_info_dict, orient='index')
                print(df)




# extract features from tracks
# sp.audio_features(track_uri)[0]
# https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50
