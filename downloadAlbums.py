import argparse
import csv
from downloader import Downloader
import sys 

parser = argparse.ArgumentParser()
parser.add_argument(dest='artist', metavar='a', type=str,
                    help='artist name')
parser.add_argument(dest='csvLoc', metavar='c', type=str,
                    help='csv location')
parser.add_argument(dest='downloadLoc', metavar='d', type=str,
                    help='download location ')
parser.add_argument(dest='error', metavar='e', type=str,
                    help='error file location')
args = parser.parse_args()

if __name__ == "__main__":
    errors = ""
    cwd = args.downloadLoc
    download = Downloader()
    errors = download.getError()
    if (errors == ""):   
        inputAlbums = []
        try : 
            csvfile = open(args.csvLoc,"r")
            csvReader = csv.reader(csvfile,delimiter="\n")
        except OSError :
            sys.exit("Impossible to read the csv")
        for row in csvReader:
            inputAlbums.append(row)
        errors = download.downloadAlbums(inputAlbums,args.artist,cwd)
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


