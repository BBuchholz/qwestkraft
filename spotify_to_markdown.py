#!/usr/bin/env python3
import os
import sys
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Ensure credentials are present
if not os.getenv("SPOTIFY_CLIENT_ID") or not os.getenv("SPOTIFY_CLIENT_SECRET"):
    sys.exit("Error: Please set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")

# 1. SETUP AUTHORIZATION WITH SCOPES
# Note: You MUST add 'http://127.0.0.1:8080' to your Redirect URIs in the Spotify Developer Dashboard!
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0",
    scope="playlist-read-private playlist-read-collaborative"
))

def extract_playlist_id(url: str) -> str:
    match = re.search(r"playlist/([A-Za-z0-9]+)", url)
    if not match:
        sys.exit(f"Error: Could not parse playlist ID from URL:\n {url}")
    return match.group(1)

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python script.py <playlist_url>")
        
    playlist_url = sys.argv[1]
    playlist_id = extract_playlist_id(playlist_url)
    
    print("Fetching playlist information...")
    try:
        # Fetch playlist details and items using Spotipy's built-in handlers
        playlist = sp.playlist(playlist_id, fields="name")
        playlist_name = playlist["name"]
        
        print(f"Fetching tracks for '{playlist_name}'...")
        results = sp.playlist_items(playlist_id)
        
        tracks = []
        while results:
            for item in results['items']:
                # Use safe .get() just in case the item contains an empty/local placeholder
                track = item.get('item') or item.get('track') 
                if track and track.get('name'):
                    tracks.append(track)
            if results['next']:
                results = sp.next(results)
            else:
                results = None
                
        print(f"Success! Found {len(tracks)} tracks.")
        # Process your tracks markdown logic here...
        
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")

if __name__ == "__main__":
    main()
