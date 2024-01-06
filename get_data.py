import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
from time import sleep

# =============================================================================
# Here is the class "Get_data" which allows to create an "artist" object. 
# This object has multiple albums containing multiple tracks, with various informations about them.
# These functions work for one artist at a time.
# =============================================================================


class Get_data:
    
         
    def __init__(self, artist_name):        
        self._artist_name = artist_name

        
    # STEP 1 ******************************************************************************************************
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
    
    
    
    # STEP 2 ******************************************************************************************************
    # get artist's all albums from artist ID
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
        #print(f'Number of albums : {len(albums_ids_list)}')      
        # ***DRAFT***
        # if 1 album :
        #album_id = albums_results_dict.get('items', {})[0].get('id') 
                
        return albums_ids_list

    
    
    # STEP 3 ******************************************************************************************************
    # get all the tracks ids of all the artist's albums
    def get_tracks_ids(self, sp, albums_ids_list):
        
        tracks_ids_list = []
        
        for album_id in albums_ids_list:
            album_tracks_info = sp.album_tracks(album_id)       # one sp.album_tracks for each album ----SP
            for track in album_tracks_info['items']:            # loop over the tracks one by one to get their info
                # retrieve basic information about each track
                track_id = track['id']
                tracks_ids_list.append(track_id)
        print(f'Number of tracks : {len(tracks_ids_list)}') 
        return tracks_ids_list
                


# =============================================================================
#     sp.tracks accepts a maximum of 50 tracks IDs at a time.
#     Need to divide the artist's whole tracks list into chunks, and call sp.tracks for each of them
#     Same with sp.audio_features which accepts a maximum of 100 tracks at a time.
#     The goal is to minimize the number of API calls to avoid hitting the limit.
# =============================================================================
    
 


    # STEP 4 ******************************************************************************************************
    def get_tracks_info(self, sp, tracks_ids_list):

        # function that divide list into chunks. It creates a list of lists
        def divide_chunks(list_length, number_chunks):       
            for i in range(0, len(list_length), number_chunks):  
                yield list_length[i : i + number_chunks]        


        # chunks for sp.tracks :
        chunks_list = divide_chunks(tracks_ids_list, 50)                    # list of lists of tracks IDs
        meta_nested_list = [] 
        
        for chunk in chunks_list:
            a = sp.tracks(chunk)['tracks']            
            meta_nested_list.append(a) 
            #print(meta_nested_list)
            sleep(np.random.uniform(0.1, 0.9))                              # break of Xsec in range between 0.1 and 0.9

        meta_list = [val for sublist in meta_nested_list for val in sublist]     # list of lists is flattened into simple list
        #print(meta_list)                                                        # list of dictionaries
        
        
        # chunks for sp.audio_features :
        chunks_list_2 = list(divide_chunks(tracks_ids_list, 100))           # list of lists of tracks IDs
        features_nested_list = []
        
        for chunk in chunks_list_2:
            b = sp.audio_features(chunk)
            features_nested_list.append(b)
            sleep(np.random.uniform(0.1, 0.9))                              # break of Xsec in range between 0.1 and 0.9
            
        features_list = [val2 for sublist2 in features_nested_list for val2 in sublist2]  # contains features of all tracks

    
# =============================================================================
#         Now we can retrieve all the info we want about all the tracks
# =============================================================================
        
        # meta :
        tracks_ids, tracks_name, album, artist, artist_id, release_date = [],[],[],[],[],[]
        
        for meta in meta_list:
            
            tracks_ids.append(meta['id'])
            tracks_name.append(meta['name'])
            album.append(meta['album']['name'])
            artist.append(meta['album']['artists'][0]['name'])
            artist_id.append(meta['album']['artists'][0]['id'])
            release_date.append(meta['album']['release_date'])            


        # features :
        track_ids, danceability, energy, loudness, speechiness, acousticness, instrumentalness, \
            liveness, valence, tempo = [],[],[],[],[],[],[],[],[],[]   
        
        for features in features_list:
            
            track_ids.append(features['id'])
            danceability.append(features['danceability'])
            energy.append(features['energy'])
            loudness.append(features['loudness'])
            speechiness.append(features['speechiness'])
            acousticness.append(features['acousticness'])
            instrumentalness.append(features['instrumentalness'])
            liveness.append(features['liveness'])
            valence.append(features['valence'])
            tempo.append(features['tempo'])


        
        tracks = [tracks_ids, tracks_name, album, artist, artist_id, release_date, \
                  track_ids, danceability, energy, loudness, speechiness, acousticness,\
                      instrumentalness, liveness, valence, tempo]
        
        columns = ['track_id', 'track_name', 'album', 'artist', 'artist_id', 'release_date', \
                  'track_id', 'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',\
                      'instrumentalness', 'liveness', 'valence', 'tempo'] 
        

        df = pd.DataFrame(tracks, index=columns).T
        #print(df)
        return df

