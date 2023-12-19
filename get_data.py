import numpy as np
import pandas as pd
pd.set_option("display.max_columns", None)
from time import sleep
import random

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
    # get all tracks info for an artist's albums and create .csv
    def get_tracks_info(self, sp, albums_ids_list):
        
        tracks_ids_list = []                                    # this is used for the track's features part
        track_info_dict = {}                                    # dictionary that contains info of the tracks
        for album_id in albums_ids_list:                        # loop over albums one by one
            album_info = sp.album(album_id)                     # one sp.album call for each album ----SP
            album_name = album_info['name']
            alb_release_date = album_info['release_date']
            artist_name = album_info['artists'][0]['name']
            artist_id = album_info['artists'][0]['id']
            print(artist_name)
            print('HEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')            
            #print(type(sp.album_tracks(album_id)['items']))    # list
                        
# =============================================================================
#             note : if we call sp.audio_features when we loop over each track, it can be time consuming.
#             so it may be better to create a list of the tracks IDs first and retrieve the features from it at once.
#             since the process is done album by album, the order of the tracks' basic info and the tracks ID
#             will match correctly.
#             but i changed my mind... it's not that time consuming in the end, so we call sp.audio_features in the loop for
#             for each track.
#             in order to avoid being flagged as a bot by the website, better making requests at random delays.
# =============================================================================

            
            album_tracks_info = sp.album_tracks(album_id)       # one sp.album_tracks for each album ----SP    
            for track in album_tracks_info['items']:            # loop over tracks one by one
                
                # retrieve basic information about each track
                track_id = track['id']
                tracks_ids_list.append(track_id)
                
                track_info_dict = {}#[track_id] = {}
                track_info_dict[track_id]['track_id'] = track_id
                track_info_dict[track_id]['track_name'] = track['name'] 
                track_info_dict[track_id]['track_number'] = track['track_number']
                track_info_dict[track_id]['artist_name'] = artist_name
                track_info_dict[track_id]['id'] = artist_id
                track_info_dict[track_id]['album_name'] = album_name
                track_info_dict[track_id]['album_id'] = album_id
                track_info_dict[track_id]['alb_release_date'] = alb_release_date
                
        df = pd.DataFrame.from_dict(track_info_dict, orient='index')        
        print(len(tracks_ids_list))
             
        
        all_tracks_features = sp.audio_features(tracks_ids_list)   # bypass the overall nb requests limit and works on 100 ids at a time
        print(all_tracks_features)
        
        danceability = all_tracks_features[0]['danceability']
        energy = all_tracks_features[0]['energy']
        loudness = all_tracks_features[0]['loudness']
        speechiness = all_tracks_features[0]['speechiness']
        acousticness = all_tracks_features[0]['acousticness']
        instrumentalness = all_tracks_features[0]['instrumentalness']
        liveness = all_tracks_features[0]['liveness']
        valence = all_tracks_features[0]['valence']
        tempo = all_tracks_features[0]['tempo']
        
        
# =============================================================================
#                 # retrieve features about each track
#                 track_info_dict[track_id]['danceability'] = sp.audio_features(track_id)[0]['danceability']
#                 track_info_dict[track_id]['energy'] = sp.audio_features(track_id)[0]['energy']
#                 track_info_dict[track_id]['loudness'] = sp.audio_features(track_id)[0]['loudness']
#                 track_info_dict[track_id]['speechiness'] = sp.audio_features(track_id)[0]['speechiness']
#                 track_info_dict[track_id]['acousticness'] = sp.audio_features(track_id)[0]['acousticness']
#                 track_info_dict[track_id]['instrumentalness'] = sp.audio_features(track_id)[0]['instrumentalness']
#                 track_info_dict[track_id]['liveness'] = sp.audio_features(track_id)[0]['liveness']
#                 track_info_dict[track_id]['valence'] = sp.audio_features(track_id)[0]['valence']
#                 track_info_dict[track_id]['tempo'] = sp.audio_features(track_id)[0]['tempo']   
#                 
#             sleep(np.random.uniform(0.1, 0.9))   # break of Xsec in range between 0.1 and 0.9           
#                 
#         df = pd.DataFrame.from_dict(track_info_dict, orient='index')
#         print(df)
#         df.to_csv('./music.csv')
# =============================================================================


# note : no need to return these info retrieved at the end of the function, just need to create a .csv right
# away when we got the info, otherwise it is just a waste of memory                



# extract features from tracks
# sp.audio_features(track_uri)[0]
# https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50
