#!/usr/bin/python3
'''
Q: what does this script do?
A: when a user converts a demo file to a sequence of TGA files in source games, the files are named as so:
    MOVIENAME0000.tga MOVIENAME0001.TGA ...
 however, if the amount of frames goes above 9999, then the zero pad for the previous files does not change
 and the rest of the frames are as such
    MOVIENAME10000.tga MOVIENAME10001.tga
 
 this can make it difficult for ffmpeg to process them into a video, as it expects a consistent zero pad
 amount
 
 So this script's function is to fix the zero padding in the file name so the filename lengths are the same
 for all the files.
'''
import os
import argparse

def get_matching_tga_files(filelist, basename, ext=".tga"):
 # basically just filters strings in a list and only keeps ones that start with prefix basename and
 # end with suffix ext
 output = []
 for file in filelist:
  if file.startswith(basename) and file.endswith(ext):
   output.append(file)
 return output

def fix_zero_padded_file(filename, basename, zeropadlength, ext=".tga"):
 #example:
 #
 # fix_zero_padded_file("myMovie002.tga", "myMovie", 4)
 #should return
 # "MyMovie0002.tga"
 #
 #
 #basename is the prefix, and ext is the suffix.
 newfilename = filename
 newfilename = newfilename.removeprefix(basename)
 newfilename = newfilename.removesuffix(ext)
 newfilename.lstrip("0")
 try: int(newfilename)
 except: raise ValueError("could not file number sequence from file: \""+filename+"\", got \""+newfilename+"\" instead, did you not specify the entire basefilename?")
 newfilename = newfilename.zfill(zeropadlength)
 newfilename = basename + newfilename + ext
 return newfilename

def main():
 # set up arguments...
 parser = argparse.ArgumentParser(
  prog = "Demo tga files movie renamer",
  description = "Fixes the inconsistent zero padding for movie's rendered from source game demo files")
 
 parser.add_argument('basefilename', help = "the base filename of the tga files: for example, for mymovie0001.tga, the basefilename would be mymovie")
 parser.add_argument('-d', '--folder', help = "folder containing the tga files, defaults to current dir", default = os.getcwd())
 parser.add_argument('-v', '--verbose', action = 'store_true', help = "print out each file operation verbosely")
 parser.add_argument('-e', '--extension', help = "file extension, defaults to \".tga\"", default = ".tga")
 
 
 args = parser.parse_args()
 args.folder = os.path.abspath(args.folder)
 
 #change dir to the specified folder, and get list of files, only the files!
 os.chdir(args.folder)
 
 files = os.listdir(args.folder)
 files = list(filter(os.path.isfile, files))
 
 # run the filter so we only get files starting with basefilename and ending with extension
 files = get_matching_tga_files(files, args.basefilename, args.extension)
 
 if len(files) == 0:
  raise ValueError("Error, no files found with basename "+args.basefilename+" in "+args.folder)
 
 
 zeropadlength = len(str(len(files)-1)) # here we get the largest file number in the list, and get the length of the string of that number
 print('found',len(files),'files!')
 print('zero pad length be set to',zeropadlength)
 
 # here is the main payload, where we actually do the renaming
 
 for file in files:
  newfile = fix_zero_padded_file(file, args.basefilename, zeropadlength, args.extension)
  if args.verbose: print( 'moving ',file,'\t->', newfile)
  os.rename(file, newfile)
 
 print("done!~ renamed",len(files),"files!")
 
 
main()
