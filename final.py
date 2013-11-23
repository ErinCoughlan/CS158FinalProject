# Erin Coughlan and Evan Casey
# Machine Learning Final Project

from collections import defaultdict
import echonest.remix.audio as audio
import pyechonest.config as config
import pyechonest.track as echotrack
import pyechonest.song as echosong
import pyechonest.util as echoutil
import numpy as np
import sklearn
import csv
import time

config.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_file = "data/kaggle_visible_evaluation_triplets.txt"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"
data_subset_song_track = "data/subset_unique_tracks.txt"

data = {}
data = defaultdict(list)
f = open(data_file, 'rt')
reader = csv.reader(f, delimiter='\t')
for row in reader:
	user = row[0]
	data[user].append(row[1:])

songs = []
f = open(data_songs, 'rt')
reader = csv.reader(f, delimiter=' ')
for row in reader:
	song = row[0]
	songs.append(song)

users = []
f = open(data_users, 'rt')
reader = csv.reader(f)
for row in reader:
	users.append(row)

songToTrack = {}
f = open(data_subset_song_track, 'rt')
reader = csv.reader(f)
for row in reader:
	row = row[0].split('<SEP>')
	track, song, artist, songName = row
	songToTrack[song] = [track, artist, songName]

"""
# Test to determine which data we have access to
songId = songs[0]
trackId, artist, songName = songToTrack[songId]
if trackId != None:
	s = echosong.Song(songId, buckets=['audio_summary'])
	t = echotrack.track_from_id(trackId)
	print s
	artist = s.artist_name
	print artist
	tempo = s.audio_summary["tempo"]
	print tempo
	dance = s.audio_summary["danceability"]
	print dance
	genre = s.song_type
	print genre
"""


# List of songs for training on
# [Artist, Tempo, Danceability]
trainData = []
for song, trackInfo in songToTrack.items():
	trackId, artist, songName = trackInfo
	while True:
		try:
			t = echotrack.track_from_id(trackId)
			t.get_analysis()
			tempo = t.tempo
			dance = t.danceability
			trainData.append([artist, tempo, dance])
		except echoutil.EchoNestAPIError: # We exceeded our access limit
			print "too many accesses per minute - retry in a minute"
			time.sleep(60)
			continue
		except IndexError: # The song wasn't found on echo nest
			print "index error - skip"
			break
		except echoutil.EchoNestIOError: # Unknown error from echo nest
			print "unknown error - retry"
			continue
		break # retry request


