import argparse
import csv
from downloader import Downloader
import sys 

parser = argparse.ArgumentParser()
parser.add_argument(dest='artist', metavar='a', type=str,
                    help='artist name')
parser.add_argument(dest='album', metavar='b', type=str,
                    help='album name')
parser.add_argument(dest='csvLoc', metavar='c', type=str,
                    help='csv location')
parser.add_argument(dest='error', metavar='e', type=str,
                    help='error file location')
args = parser.parse_args()

if __name__ == "__main__":
    errors = "" 
    download = Downloader()
    errors = download.getError()
    artist = args.artist  
    album = args.album
    if (errors == ""):
        tracks  = download.searchTracksFromAlbumName(artist,album)
        try : 
            csvfile = open(args.csvLoc,"w", encoding='utf-8')
            csvWriter = csv.writer(csvfile,delimiter="\n")
        except OSError :
            sys.exit("Impossible to write the csv")
        output = []
        print(tracks)
        for track in tracks: 
            track = str(track).replace("Track: " , "").replace("<","").replace(">","") 
            id = str(download.getTrackIdFromTrackName(artist,track))
            if(id.lower() != 'none'):
                output.append(track + "\t" + id )
        csvWriter.writerow(output)
    if(errors != "" ):
        try : 
            outputFile = open(args.error,"w")
        except OSError :
            sys.exit("Impossible to write the output file")
        for error in errors :
            outputFile.write(error)
        sys.exit(download.getError())
    else : 
        sys.exit(0)


