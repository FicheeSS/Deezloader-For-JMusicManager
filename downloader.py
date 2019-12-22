# coding: utf8
import sys
import os
import time
import requests
import socket
import os

try : 
    lib_path = os.path.abspath("./lib/")
    sys.path.insert(0, lib_path)
    if(sys.path[0] != lib_path):
        sys.exit("???")    
    from deezloader import exceptions
    import deezer
    import deezloader   
except ModuleNotFoundError :
    sys.exit("Module not found check the import") 

from pathlib import Path
from os import path
import multiprocessing


FORBIDEN_CHAR = [(":", "_"), ("<", "_"), (">", "_"), ("&", "_"), ("|", "_")]
URL_CARSET = [("ä", "a"), ("'", ""), (",", ""), ("/", "-"), (".", ""), ("û", "u"),
              ("ü", "u"), ("ù", "u"), ("?", ""), (":", ""), ("ö", "o"), ("ô", "o"), ("_", "")]
RESSOURCES_NAME = ["Album","Track","Artist" ]


class Downloader():
    def __init__(self, key=""):
        self.client = deezer.Client()
        self.strLastError = ""
        self.notfound = []
        self.error = ""
        if key != "":
            try:
                self.downloa = deezloader.Login(key)
            except socket.gaierror:
                self.strLastError = "Impossible to connect to internet"
                sys.exit("Impossible to connect to the internet please check your internet connection")
            except requests.exceptions.ConnectionError:
                self.strLastError = "Impossible to connect to internet"
                sys.exit("Impossible to connect to the internet please check your internet connection")
            except exceptions.BadCredentials:
                self.strLastError = "Wrong ARL"
                sys.exit("Check Arl")

    def getError(self):
        return self.strLastError

    def DownloadTracksFromAlbum(self,id, cwd):
        #get a the album.resource objet from the id 
        album = self.getAlbumFromID(id)
        if  not not album:
            #get a list of track.resource objet
            RList = album.get_tracks()
            idList = []
            #get the track id from the resource 
            for rs in RList:
                time.sleep(0.1)
                idList.append(rs.get_id())
            #handler of the download 
            error = self.DownloadByTrackResource(idList, cwd)
            if(not not error):
                return self.strLastError
            else:
                return ""
        else:
            pass

    def clearFromIllegalChars(self, tobeclean):
        #remove all problematic chars
        for char in FORBIDEN_CHAR:
            tobeclean = tobeclean.replace(char[0], char[1])
        return tobeclean

    def downloadAlbums(self, ids, cwd):
        #handler of multiples albums to be downloaded
        output = []
        for id in ids:
            time.sleep(0.1)
            output.append(self.DownloadTracksFromAlbum(id, cwd))
        return output

    def getAlbumsFromArtist(self, artist):
        #search all the available album from a artist 
        artist = self.clearFromIllegalChars(artist)
        return self.client.advanced_search({"Artist": artist}, limit=1000, relation="album")

    def getAlbumResourceFromAlbumArtist(self, artist, albums):
        #get album.resource from album list
        result = []
        artist = self.clearFromIllegalChars(artist)
        for album in albums:
            album[0] = self.clearFromIllegalChars(album[0])
            result.append(self.client.advanced_search(
                {"Artist": artist, "Album": album}, limit=1, relation="album"))
            time.sleep(0.1)
        return result

    def searchMissingAlbums(self, artist, albums=""):
        #search all the missing album available from the given artist 
        alreadyAlbums = self.getAlbumResourceFromAlbumArtist(artist, albums)
        allAlbumsAv = self.getAlbumsFromArtist(artist)
        result = False
        toBeDwlAlbums = []
        for albumAv in allAlbumsAv:
            for albumAr in alreadyAlbums:
                if albumAr[0].get_id() == albumAv.get_id():
                    result = True
            if result != True:
                toBeDwlAlbums.append(albumAv)
            result = False
        return toBeDwlAlbums

    def DownloadByTrackResource(self, tracksid, cwd):
        #multithreading the download
        jobs = []
        for track in tracksid:
            p = multiprocessing.Process(
                target=self.DownloadByTrackName, args=(track, self.downloa, cwd))
            p.start()
            time.sleep(0.1)
            jobs.append(p)
        for proc in jobs:
            proc.join()
        if(not not self.strLastError):
            return self.strLastError
        else:
            return ""

    def DownloadByTrackName(self, trackid, dwl, cwd):
        #final downloader to be multithreaded
        try:
            dwl.download_trackdee(
                "https://www.deezer.com/fr/track/"+str(trackid),
                output=cwd,
                quality="FLAC",
                recursive_quality=True,
                recursive_download=True,
                not_interface=False
            )
        except TypeError:
            print("Invalid type make sure you use utf8 encoding")
            self.strLastError = "Bad Encoding"
        except exceptions.TrackNotFound:
            print("Track Not found ")
            self.notfound.append(trackid)
        except exceptions.BadCredentials:
            print("Invalid credidentials")
            self.strLastError = "Wrong credidentials check arl"
        except exceptions.QuotaExceeded:
            print("Exceeded quota")
            self.strLastError = "Exceeded quota"
        except KeyError :
            print("Key Error")
            self.strLastError = "Key Error"

    def getAlbumIdFromAlbumName(self, artist, album):
        s = self.client.advanced_search(
            {"Artist": artist, "Album": album}, limit=1, relation="album")
        if not not s:
            return s[0].get_id()

    def searchTracksFromAlbumName(self, artist, album):
        print("Artist : "+ str(artist) + ", album : "+ str(album))
        s = self.client.advanced_search(
            {"Artist": artist, "Album": album}, limit=50, relation="track")
        if not not s:
            return s
        else :
            return ""

    def getTrackIdFromTrackName(self, artist, track):
        s = self.client.advanced_search(
            {"Artist": artist, "Track": track}, limit=1, relation="track")
        if not not s:
            return s[0].get_id()
        else :
            return ""

    def getTrackFromID(self,trackid):
        track = self.client.get_tracks(trackid)
        print(track)
        return track

    def getAlbumFromID(self,albumid):
        if type(albumid) is list : 
            albumid = albumid[0]
        album = self.client.get_album(albumid)
        print(album)
        return album

    def getArtistFromID(self,id):
        artist = self.client.get_artist(id)
        print(artist)
        return artist
    
    def getGenreFromId(self,id):
        return self.client.get_genre(id)
    
    def getArtistFromAlbumId(self,id):
        album = self.clearStrForSearch(self.getAlbumFromID(id))
        artist = self.clearStrForSearch(self.client.advanced_search(
            {"Album": album}, limit=1, relation="artist"))
        if not not artist :
            return self.clearStrForSearch(artist)
            
    def clearStrForSearch(self,string):
        for ressource in RESSOURCES_NAME:
            string = str(string).replace(ressource+": " , "").replace("<","").replace(">","") 
        return string
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
# quality can be FLAC, MP3_320, MP3_256 or MP3_128
# recursive_quality = True if selected quality isn't avalaible download with best quality possible
# recursive_download = True if song has already been downloaded don't ask for download it again
# not_interface = True if you want too see no download progress

# Modules python à charger avec pip :
# - mutagen
# - deezloader
# - deezer-python
