# Deezloader-For-JMusicManager
This set of scripts is made for a specific purpose this is why the interfaces are so special.
# How to 
To understand how the different Python script interact with each other visite [this](https://docs.google.com/document/d/1Cm7vSd-qv1KZDDZmV4ThJmtIWmdKyo3nsw3UuEH44hQ/edit?usp=sharing) Google Doc

You can get an arl key by following this [link](https://notabug.org/RemixDevs/DeezloaderRemix/wiki/Login+via+userToken)

## Search For all the Albums of an Artist  
```
python searchAlbum.py artistName ./file.csv ./errors.txt
```
 ## Search for all Tracks of an Album
 
 ```
 python searchTrack.py albumId ./file.csv ./errors.txt
 ```
 
 ## Download Albums 
 ```
 python downloadAlbums.py ./file.csv ./download/ ./errors.txt arlKey
 ```
 
 ## Download a specific Tracks
 Please prefer the downloadAlbum method because the downloading of tracks is not multithreaded and much more slower.
 ```
 python downloadTracks.py ./file.csv ./download/ ./errors.txt arlKey 
 ```
 ## Autodownloader (work in progress)
 Check every 2 minutes for a new csv file in the csvFolder and download all the albums found inside 
  ```
  python autodownloader.py ./csvFolder/ ./downloadLoc/ ./errors.txt arlKey
  ```
  
  # Simple Use
  If you just want to download all the albums of the artist Art in the folder Music with your arlKey : 
 ```
 python searchAlbums.py Art ./csv.csv ./e.txt && python downloadAlbums.py ./csv.csv ./Music/ ./e.txt arlKey   
 ```
 # Dependecies 
 Build using  :
 
 -[Deezloader](https://github.com/An0nimia/deezloader) for Python by AnOnimia
 
 -[Deezer-python](https://github.com/browniebroke/deezer-python) 
 
 Only thier depencies and standarts python libraries are required 
 
  
