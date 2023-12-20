import spotipy
import os 
from spotipy import SpotifyClientCredentials, util
from get_data import Get_data
import yaml


def credentials_spotify():
        
    credentials = yaml.load(open('./credentials.yml'), Loader=yaml.FullLoader)
    client_id = credentials['credentials']['client_id']    
    client_secret = credentials['credentials']['client_secret']
  
    
    # Credentials to access the Spotify music data
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    
# =============================================================================
#     # IF WE CAN ACCESS TO A USER'S PLAYLIST : Credentials to access the playlist's tracks
#     #username = config.username
#     username = credentials['credentials']['username']
#     scope = 'playlist-modify-public'
#     redirect_uri = 'https://example.com'
#     token = util.prompt_for_user_token(username,
#                                scope,
#                                client_id = client_id,
#                                client_secret = client_secret,
#                                redirect_uri = redirect_uri)
#     spt = spotipy.Spotify(auth=token)
# =============================================================================
  
    return sp #, spt


# Create a folder specific to the artist in which we save the results file etc.
def create_dir(path, dirname):
    if not os.path.exists(dirname):
        os.mkdir(path + dirname)  
  


# =============================================================================
# To begin with :
# Set up Spotify credentials and get access authorisation
# Choose few artists
# Retrieve albums and tracks and informations related
# =============================================================================

if __name__ == "__main__" :
    
    #sp, spt = credentials_spotify()
    sp = credentials_spotify()

    #artist_name = input('Artist name : ')
    artist_name = 'Whitney Houston'
    print(artist_name)
    
    create_dir('./', artist_name)
    
    gd = Get_data(artist_name)

    artist_id = gd.get_artist_id(sp)   
    
    albums_ids_list = gd.get_albums_ids(sp, artist_id, 20)

    tracks_ids_list = gd.get_tracks_ids(sp, albums_ids_list)

    tracks_info_df = gd.get_tracks_info(sp, tracks_ids_list)
    tracks_info_df.to_csv(os.path.join('./'+artist_name, f"{artist_name}.csv"))

