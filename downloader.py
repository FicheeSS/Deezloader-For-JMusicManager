# coding: utf8
import sys
import os 
sys.path.insert(0, os.getcwd()+"/lib/")
import deezloader
import os
import deezer
import multiprocessing
import time 
from os import path
from pathlib import Path
from deezloader import exceptions 
import socket
import requests
import sys
FORBIDEN_CHAR = [(":","_"),("<","_"),(">","_"),("&","_"),("|","_")]
URL_CARSET = [("ä", "a"), ("'", ""), (",", ""), ("/", "-"), (".", ""), ("û", "u"),
              ("ü", "u"), ("ù", "u"), ("?", ""), (":", ""), ("ö", "o"), ("ô", "o"),("_","")]


class Downloader():
	def __init__(self,key=""):
		self.client = deezer.Client()
		self.strLastError = ""
		self.notfound = []
		self.error = ""
		if key != "":
			try : 
				self.downloa = deezloader.Login(key)
			except socket.gaierror : 
				print("Impossible to connect to the internet please check your internet connection")
				self.strLastError = "Impossible to connect to internet"
			except requests.exceptions.ConnectionError : 
				print("Impossible to connect to the internet please check your internet connection")
				self.strLastError = "Impossible to connect to internet"	
			except exceptions.BadCredentials:
				print("Bad credidential check arl")
				self.strLastError = "Wrong ARL"

	def getError(self):
		return self.strLastError

	def DownloadTracksFromAlbum(self,album,artist, cwd):
		album = self.client.advanced_search({"Artist" : artist , "Album" :album },limit=1,relation="album")
		print(album)
		if(album != ""):
			RList = album[0].get_tracks()
			idList = []
			for rs in RList :
				time.sleep(0.1)
				idList.append(rs.get_id())
			error = self.DownloadByTrackResource(idList,cwd)
			if(not not  error):
				return self.strLastError
			else:
				return ""
		else : 
			pass
		

	def clearFromIllegalChars(self,tobeclean):
		for char in FORBIDEN_CHAR :
			tobeclean = tobeclean.replace(char[0],char[1])
		return tobeclean

	def downloadAlbums(self,albums,artist,cwd):
		output = []
		print(len(albums))
		for album in albums :
			time.sleep(0.1)
			output.append(self.DownloadTracksFromAlbum(album,artist,cwd))
		return output 

	def getAlbumsFromArtist(self,artist):
		artist = self.clearFromIllegalChars(artist)
		return self.client.advanced_search({"Artist" : artist },limit=1000,relation="album")

	def getAlbumResourceFromAlbumArtist(self,artist,albums):
		result = []
		artist = self.clearFromIllegalChars(artist)
		for album in albums :
			album[0] = self.clearFromIllegalChars(album[0])
			result.append(self.client.advanced_search({"Artist" : artist , "Album" :album },limit=1,relation="album"))
			time.sleep(0.1)
		return result


	def searchMissingAlbums(self,artist,albums=""):		
		alreadyAlbums = self.getAlbumResourceFromAlbumArtist(artist,albums)
		allAlbumsAv = self.getAlbumsFromArtist(artist)
		result = False
		toBeDwlAlbums = []
		for albumAv in allAlbumsAv :
			for albumAr in alreadyAlbums :
				if albumAr[0].get_id() == albumAv.get_id() :
					result = True
			if result != True:
				toBeDwlAlbums.append(albumAv)
			result = False
		return toBeDwlAlbums

	def DownloadByTrackResource(self,tracksid,cwd):
			jobs = []
			for track in tracksid: 
				p = multiprocessing.Process(
					target=self.DownloadByTrackName, args=(track,self.downloa,cwd))
				p.start()
				time.sleep(0.1)
				jobs.append(p)
			for proc in jobs:
				proc.join()
			if(not not  self.strLastError ):
				return self.strLastError 
			else :
				return ""


	def DownloadByTrackName(self,trackid,dwl,cwd):
		try : 
			dwl.download_trackdee(
			"https://www.deezer.com/fr/track/"+str(trackid),
			output = cwd ,
			quality = "FLAC",
			recursive_quality = True,
			recursive_download = True,
			not_interface = False
			)
		except TypeError:
			print("Invalid type make sure you use utf8 encoding")
			self.strLastError = "Bad Encoding"
		except exceptions.TrackNotFound :
			print("Track Not found ")
			self.notfound.append(trackid)
		except exceptions.BadCredentials :
			print("Invalid credidentials")
			self.strLastError = "Wrong credidentials check arl"
		except exceptions.QuotaExceeded : 
			print("Exceeded quota")
			self.strLastError = "Exceeded quota"
		
	def getAlbumIdFromAlbumName(self,artist,album):
		s = self.client.advanced_search({"Artist" : artist , "Album" :album },limit=1,relation="album")
		if not not  s :
			return s[0].get_id()


	def searchTracksFromAlbumName(self,artist,album):
		s = self.client.advanced_search({"Artist" : artist , "Album" :album },limit=50,relation="track")
		return s
	
	def getTrackIdFromTrackName(self,artist,track):
		s =  self.client.advanced_search({"Artist" : artist , "Track" : track },limit=1,relation="track")
		if not not s :
			return s[0].get_id()

"""
downloa.download_name(
	artist = "Eminem",
	song = "Berzerk",
	output = os.getcwd() +"/" ,
	quality = "FLAC",
	recursive_quality = False,
	recursive_download = False,
	not_interface = False
)
"""
#quality can be FLAC, MP3_320, MP3_256 or MP3_128
#recursive_quality = True if selected quality isn't avalaible download with best quality possible
#recursive_download = True if song has already been downloaded don't ask for download it again
#not_interface = True if you want too see no download progress
#bridge java : https://pythonhosted.org/javabridge/java2python.html

# Modules python à charger avec pip :
# - mutagen
# - deezloader
# - deezer-python
