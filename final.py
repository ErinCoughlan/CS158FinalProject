# Erin Coughlan and Evan Casey
# Machine Learning Final Project

from collections import defaultdict
import echonest.remix.audio as audio
import pyechonest.config as config
import pyechonest.track as echotrack
import numpy as np
import sklearn
import csv

config.ECHO_NEST_API_KEY = "U98ZZRHBZWNWUDKPW"
data_file = "data/kaggle_visible_evaluation_triplets.txt"
data_songs = "data/kaggle_songs.txt"
data_users = "data/kaggle_users.txt"
data_song_track = "data/taste_profile_song_to_tracks.txt"

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
f = open(data_song_track, 'rt')
reader = csv.reader(f, delimiter='\t')
for row in reader:
	song = row[0]
	if len(row) == 2:
		track = row[1]
	else:
		track = None
	songToTrack[song] = track

# Test to determine which data we have access to
trackId = songToTrack[songs[0]]
if trackId != None:
	t = echotrack.track_from_id(trackId)
	print t.tempo



