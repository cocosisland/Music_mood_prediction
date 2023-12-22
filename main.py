import spotipy
import os 
import numpy as np
import pandas as pd
import yaml
import glob
from spotipy import SpotifyClientCredentials, util
from get_data import Get_data
from clustering import cluster



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


# Create a folder in a specific location in which we can save the results files etc.
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
    artist_name = 'Louis Armstrong' #'2pac' #'Slipknot' # 'DJ Okawari' #'Whitney Houston'
    artists_list = ['Louis Armstrong', '2pac', 'Slipknot', 'DJ Okawari', 'Whitney Houston']
    print(artist_name)
    
    path = './'
    create_dir(path, 'artists/')
    #create_dir(path+'artists/', artist_name)


    # STEP : GET TRACKS AND AUDIO FEATURES INTO .CSV    
    gd = Get_data(artist_name)
    artist_id = gd.get_artist_id(sp)       
    albums_ids_list = gd.get_albums_ids(sp, artist_id, 20)
    tracks_ids_list = gd.get_tracks_ids(sp, albums_ids_list)
    tracks_info_df = gd.get_tracks_info(sp, tracks_ids_list)
    tracks_info_df.to_csv(os.path.join('./'+artist_name, f"{artist_name}.csv"))


    # STEP : GATHER THE ARTISTS' DATA INTO ONE FILE        
    bag = glob.glob('./artists/*.csv')        
    artists = []
    for file in bag:
        df = pd.read_csv(file)
        df.reset_index(inplace=True)  
        artists.append(df)
    df_art = pd.concat(artists)   
    #df_art = df_art.sample(frac=1, axis=1).reset_index(drop=True)
    df_art.to_csv("./artists/youyou.csv")     


    # STEP : CLUSTER TRACKS BY MOOD    
    columns_keep = ['track_id', 'track_name', 'preview_url', 'artist', 'artist_id', \
                  'danceability', 'energy', 'loudness', 'speechiness', 'acousticness',\
                      'instrumentalness', 'valence'] 
    
    #filepath = path+artist_name+ f'/{artist_name}.csv'
    filepath = path+"artists/youyou.csv"
    df = pd.read_csv(filepath, usecols=columns_keep)    
    df_labeled = cluster(df)

    #df_labeled.to_csv(os.path.join('./'+artist_name, f"{artist_name}_labels.csv"))
    df_labeled.to_csv(os.path.join('./artists/', "youyou_labels.csv"))

