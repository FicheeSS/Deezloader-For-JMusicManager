import argparse
import csv
from downloader import Downloader
import sys 
import re
tab = re.compile("[^\t]+")

parser = argparse.ArgumentParser()
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
    if (errors == ""):   
        tracks = []
        output = []
        try : 
            csvfile = open(args.csvLoc,"r")
            csvReader = csv.reader(csvfile,delimiter="\n")
        except OSError :
            sys.exit("Impossible to read the csv")
        for row in csvReader:
            tracks.append(row)
        for track in tracks :
            if not not id :
                output.append(int(track[0]))
        errors = download.DownloadByTrackResource(output,cwd)
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


