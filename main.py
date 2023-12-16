import spotipy
import sys
from spotipy import SpotifyClientCredentials, util
import config
from get_data import Get_data
import yaml


def credentials_spotify():
    
    #client_id = config.client_id
    #client_secret = config.client_secret
    
    credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)
    client_id = credentials['credentials']['client_id']    
    client_secret = credentials['credentials']['client_secret']
    
    
    # Credentials to access the Spotify music data
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
    
    # IF WE CAN ACCESS TO A USER'S PLAYLIST : Credentials to access the playlist's tracks
    #username = config.username
    username = credentials['credentials']['username']
    scope = 'playlist-modify-public'
    redirect_uri = 'https://example.com'
    token = util.prompt_for_user_token(username,
                               scope,
                               client_id = client_id,
                               client_secret = client_secret,
                               redirect_uri = redirect_uri)
    spt = spotipy.Spotify(auth=token)
    
    return sp, spt



#######

# get artist's ID from his name
def get_artist_id(sp):
    
    results = sp.search(q = 'artist:' + artist_name, type = 'artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        print(artist['name'], '\n', artist['uri'])   # spotify:artist:6XpaIBNiVzIetEPCWDvAFP
        #artist_id = artist['uri'].split(':')[2]
        artist_id = artist['id']
        
    return artist_id
    
    

    
# ATTENTION CODE POUR UN SEUL ALBUM POUR LE MOMENT - A ARRANGER POUR PLUS
def get_albums_id(sp, artist_id, limit_nb_albums=False):
    
    albums_results = sp.artist_albums(artist_id, limit_nb_albums)
    #print(list(albums_results.keys()))  # ['href', 'items', 'limit', 'next', 'offset', 'previous', 'total']
      
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
    
#########    


# =============================================================================
# To begin with :
# Set up Spotify credentials and get access authorisation
# Choose few artists
# Retrieve albums and tracks and informations related
# =============================================================================

if __name__ == "__main__" :
       
    sp, spt = credentials_spotify()
    
    #artist_name = input('Artist name : ')
    artist_name = 'Whitney Houston'   
    
    gd = Get_data(artist_name)
    print(sp)
    artist_id = get_artist_id(sp)
    print(sp)
    
    albums_results = sp.artist_albums(artist_id, limit=1)
    print(list(albums_results.keys()))  # ['href', 'items', 'limit', 'next', 'offset', 'previous', 'total']    
    
    #albums_id = get_albums_id(sp, artist_id, 1)

    #tracks_id = gd.get_tracks_id(albums_id)


