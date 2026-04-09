import spotipy
import os
import subprocess
from spotipy.oauth2 import SpotifyOAuth
import Agent.debug

clientID = os.getenv("SP_CLIENT_ID")
clientSecret = os.getenv("SP_CLIENT_SECRET")

SCOPE = "user-read-playback-state,user-modify-playback-state,playlist-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=clientID,
    client_secret=clientSecret,
    redirect_uri="https://google.com/callback",
    scope=SCOPE
))


def play_song(query:str="song"):
    results = sp.search(q=query, limit=1, type="track")
    print(results)

    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        uri = track["uri"]
        try:
            sp.start_playback(uris=[uri])
        except:
            __restart_spotify()
            sp.start_playback(uris=[uri])
        return f"Playing: {track['name']} by {track['artists'][0]['name']}"
        
    else:
        return "Song not found."


def play_playlist_by_name(name:str="playlist"):
    playlists = sp.current_user_playlists(limit=50)
    print(playlists)

    for playlist in playlists["items"]:
        if playlist["name"].lower() == name.lower():
            try:
                sp.start_playback(context_uri=playlist["uri"])
            except :
                __restart_spotify()
                sp.start_playback(context_uri=playlist["uri"])
            return f"Playing playlist: {playlist['name']}"

    return "Playlist not found."

def get_playlists():
    playlists = []
    results = sp.current_user_playlists(limit=50)

    while results:
        for item in results["items"]:
            playlists.append({
                "name": item["name"],
                "uri": item["uri"],
                "tracks": item["tracks"]["total"]
            })

        # Pagination (if more than 50 playlists)
        if results["next"]:
            results = sp.next(results)
        else:
            results = None

    return playlists

def spotify_pause():
    playback = sp.current_playback()

    if playback and playback["is_playing"]:
        sp.pause_playback()
        return ("Playback paused.")
    else:
        return ("Nothing is currently playing.")

def spotify_resume():
    try:
        sp.start_playback()
        return ("Playback resumed.")
    except spotipy.exceptions.SpotifyException as e:
        return ("Error resuming playback:", e)

def next_track():
    try:
        sp.next_track()
        return ("Skipped to next track.")
    except spotipy.exceptions.SpotifyException as e:
        return ("Error skipping track:", e)

def previous_track():
    try:
        sp.previous_track()
        return ("Went to previous track.")
    except spotipy.exceptions.SpotifyException as e:
        return ("Error going to previous track:", e)

def __restart_spotify():
    subprocess.run("pkill spotify", shell=True)
    subprocess.run("spotify &", shell=True)

# ----------- INPUT HANDLER -----------
if __name__ =="__main__":
    user_input = input("Enter song or playlist: ")

    mode = input("Type 'song' or 'playlist': ").lower()

    if mode == "song":
        play_song(user_input)

    elif mode == "playlist":
        play_playlist_by_name(user_input)

    else:
        print("Invalid mode.")