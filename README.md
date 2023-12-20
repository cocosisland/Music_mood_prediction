Le projet consiste à vouloir prédire l'humeur musicale d'une chanson. Cette fonctionnalité pourrait permettre d'affiner
la pertinence en matière de recommendation de titres à un utilisateur, en se basant sur son humeur.

Les données sont extraites depuis la plateforme de Spotify, via son API. Créer d'abord un compte sur Spotify for Developer,
et créer une application pour ce projet (Web API). Retrouver les clés API. "Spotipy" est une librairie Python qui permet de s'authentifier avec ces clés et 
d'accéder à toutes les données de musique (artistes, albums, titres, mood, ...).

Le code est entièrement rédigé sur Spyder, le programme complet contenant X fichiers :

Pour extraire les données :
- main.py, qui permet de :
Lancer le code, s'authentifier pour utiliser l'API de Spotify, choisir un artiste, créer un dossier pour l'artiste, appeler les fonctions dans get_data.py 
pour extraire les titres et leurs informations pour ensuite les stocker sur un fichier CSV généré dans le dossier créé.

- credentials.yml :
Contient les clés API confidentielles (identifiant, mot de passe et nom d'utilisateur) pour pouvoir utiliser l'API de Spotify.

- get_data.py, qui permet de :
Récolter toutes les données de musique que l'on veut sur un artiste. Procédé par successions d'appels de fonctions et de modules Spotipy :
Nom de l'artiste (main) -> ID de l'artiste (step 1) -> liste d'albums (step 2) --> liste des IDs des titres de ces albums (step 3) -->-- 
--> liste de dictionaries, chaque dictionary contenant les informations et moods de chaque titre. Renvoie un dataframe au main pour créer un CSV.

- get_data2(?).py :
C'est une première tentative de programme qui extrait les données voulues, et qui marche, mais on atteint assez rapidement la limite
du nombre d'appels API. Le code dans get_data.py contourne ce problème en réduisant le nombre d'appels. get_data2.py n'est pas appelé dans le programme final!
