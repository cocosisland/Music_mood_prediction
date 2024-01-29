Le projet consiste à vouloir prédire l'humeur musicale d'une chanson. Cette fonctionnalité pourrait permettre d'affiner la pertinence en matière de recommendation de titres à un utilisateur, en se basant sur son humeur.

Les données sont extraites depuis la plateforme de Spotify, via son API. Créer d'abord un compte sur Spotify for Developer, et créer une application pour ce projet (Web API). Retrouver les clés API. "Spotipy" est une librairie Python qui permet de s'authentifier avec ces clés et d'accéder à toutes les données de musique (artistes, albums, titres, mood, ...).

Le code est entièrement rédigé sur Spyder, le programme complet contenant 4 fichiers .py :
main.py, get_data.py, clustering.py, classif_model.py
et le fichier credential.yml (à compléter)

Un compte-rendu est également disponible : Compte-rendu-projet-Spotify.pdf
