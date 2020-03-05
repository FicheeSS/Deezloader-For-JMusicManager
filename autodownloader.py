import argparse
from downloader import Downloader
import os 
import glob 
import time
import sys 
parser = argparse.ArgumentParser()
parser.add_argument(dest='csvLoc', metavar='c', type=str,
                    help='lookup folder location')
parser.add_argument(dest='downloadLoc', metavar='d', type=str,
                    help='download location ')
parser.add_argument(dest='error', metavar='e', type=str,
                    help='error file location')
parser.add_argument(dest='key', metavar='k', type=str,
                    help='deezer arl key')
args = parser.parse_args()

    

if __name__ == "__main__":  
    errors = ""
    csvLoc = args.csvLoc
    cwd = args.downloadLoc
    download = Downloader(args.key)
    errors = download.getError()
    os.chdir(csvLoc)
    if(errors != "" ):
        try : 
            outputFile = open(args.error,"w")
        except OSError :
            sys.exit("Impossible to write the output file")
        for error in errors :
            outputFile.write(error)
        sys.exit("Error check log")
    print("Initialisation succesful ! \nAutoLookup is now running ")
    while(True):
        try : 
            print("Looking for new csv ...")
            csvList = []
            for file in glob.glob("*.csv"):
                csvList.append(file)
        except OSError as e :
            sys.exit(str(e) + "Cannot get to csv directory exiting ...")
        except :
            sys.exit("Input csv error exiting ...")
        if not not csvList :
            print("CSV found processing ...")
            for csvfile in csvList :  
                inputAlbum = []
                try : 
                    csvfile = open(args.csvLoc,"r")
                    csvReader = csv.reader(csvfile,delimiter="\n")
                except OSError :
                    sys.exit("Impossible to read the csv")
                for row in csvReader:
                    inputAlbum.append(row)
                unsplit = inputAlbum.copy()
                split = []
                #can be use with only the id or with the name before
                for t in unsplit :
                    tmp = t[0].split("\t")
                    try : 
                        split.append(tmp[1])
                    except IndexError:
                        split.append(tmp[0])
                inputAlbum = split.copy()
                errors = download.downloadAlbums(inputAlbum,cwd)
                if(errors != "" ):
                    try : 
                        outputFile = open(args.error,"w")
                    except OSError :
                        sys.exit("Impossible to write the output file")
                    for error in errors :
                        outputFile.write(error)
                try:
                    os.remove(csvfile)
                except OSError :
                    sys.exit("Cannot delete file check permissions")
                
        else : 
            time.sleep(120)
        

        