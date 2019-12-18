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
parser.add_argument(dest='key', metavar='k', type=str,
                    help='deezer arl key')
args = parser.parse_args()

if __name__ == "__main__":
    errors = ""
    cwd = args.downloadLoc
    download = Downloader(args.key)
    errors = download.getError()
    if (errors == "" and args.key != ""):   
        unsplits = []
        try : 
            csvfile = open(args.csvLoc,"r")
            csvReader = csv.reader(csvfile,delimiter="\n")
        except OSError :
            sys.exit("Impossible to read the csv")
        for row in csvReader:
            unsplits.append(row)
            inputAlbum = []
        for unsplit in unsplits :
            tmp = unsplit[0].split("\t")
            inputAlbum.append(tmp[1])
        print(inputAlbum)
        errors = download.downloadAlbums(inputAlbum,cwd)
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


