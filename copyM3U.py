from shutil import copyfile
import os
import sys
import glob
import re
import hashlib
from fuzzysearch import find_near_matches

GlobalFileList = []
GlobalSearchQueue = []
GlobalOutFileList = []

if len(sys.argv) > 1:
	m3ufile = sys.argv[2]
	DoDeepSearch = sys.argv[1]
else:
	m3ufile = '01 Urban Party.m3u'

baseLoc = "/Volumes/SideSpinMob/SS" 
missingLoc = baseLoc + "/missing_songs"
m3ufile = "/Users/chadmonden/Dropbox/music/MOVE_Crates/" + m3ufile
ExportFiles = "/Volumes/SideSpinMob/Crates"
#SearchLocation = "E://Temp"
SearchLocation ="/Volumes/XFer/AllMusic"
DestinationStr = ''


def FixSlashes(inFileName):
    if ":" in inFileName:
        inFileName = inFileName.replace(os.sep, '/')
    return inFileName

m3ufile = FixSlashes(m3ufile)
ExportFiles = FixSlashes(ExportFiles)
missingLoc = FixSlashes(missingLoc)
SearchLocation = FixSlashes(SearchLocation)

def IntializeGlobalFileList(inLocation):
	global GlobalFileList
	path=inLocation + "//**"
	if not GlobalFileList:
		print("Initializing Global File List......")
		for file in glob.iglob(path, recursive=True):
			filename = os.path.basename(file)
			readable_hash = hashlib.sha256(str(filename).encode('utf-8')).hexdigest()
			#print(readable_hash)
			GlobalFileList.append([FixSlashes(file),readable_hash])
		print(str(len(GlobalFileList)) + " loaded into Global File List.")

def SearchforString(inStringObject):
	global SearchLocation
	global GlobalFileList
	TrimSpacesString = inStringObject.strip()
	inLocation = SearchLocation
	path=inLocation + "//**"
	OutFileList = []

	# It returns an iterator which will
	# be printed simultaneously.
	#print("\nUsing glob.iglob()")
	print("Searching for " + TrimSpacesString + " in this location: " + inLocation +"...")
	#for name in glob.glob('/home/geeks/Desktop/gfg/*'):
    #	print(name)

	# Prints all types of txt files present in a Path
	for file in GlobalFileList:
		if inStringObject.lower() in file[0].lower():
			OutFileList.append(file[0])
	print("Files found:" + str( len(OutFileList)))
	return OutFileList

def SplitStringforSearch(InStringVal, PositionInt):
	#InputString = InStringVal.replace("-", " ")
	#InputString = InputString.replace("Clean", "")
	#InputString = InputString.replace("Dirty", "")
	#InputString = InputString.replace("Radio", "")
	#InputString = InputString.replace("(", "")
	#InputString = InputString.replace(")", "")
	StringList = InStringVal.split(' ')
	lenList = len(StringList)
	OutStr = ""

	for PositionCounter in range(PositionInt-1, lenList):
		OutStr = OutStr + " " +  StringList[PositionCounter]
	return OutStr

def containsLetterAndNumber(input):
    has_letter = False
    has_number = False
    for x in input:
        if x.isalpha():
            has_letter = True
        elif x.isnumeric():
            has_number = True
        if has_letter and has_number:
            return True
    return False

def RemoveNumPrefixforSearch(InStringVal, PositionInt):
	InputString = InStringVal.replace("-", "")
	#InputString = InputString.replace("Clean", "")
	#InputString = InputString.replace("Dirty", "")
	#InputString = InputString.replace("Radio", "")
	#InputString = InputString.replace("(", "")
	#InputString = InputString.replace(")", "")
	StringList = InStringVal.split(' ')
	lenList = len(StringList)
	OutStr = ""

	for PositionCounter in range(PositionInt-1, lenList):
		if (not containsLetterAndNumber(StringList[PositionCounter])) and PositionInt < 3:
			OutStr = OutStr + " " +  StringList[PositionCounter]
	return OutStr

def ChooseFileForCopy(inFileName):
	pageslength = 10
	StartCounter = 0
	EndCounter = pageslength
	ListLength = len(inFileName)
	#regex = "^[1-9][0-9]?$|^100$"
	regex = "^([0-9]|[1-9][0-9]|100)$"
	ChosenFile = ''
	if ListLength>=1:	
		while StartCounter < ListLength:
			for ListCounter in range(StartCounter, StartCounter + 10):
				if (ListLength - 1) >= ListCounter:
					#print("["+str(ListCounter)+"] " + FixSlashes(inFileName[ListCounter]))
					# os.path.basename(m3ufile)
					print("["+str(ListCounter)+"] " + os.path.basename(inFileName[ListCounter]))
			ChooseAFile = input("Select a file number or [q] to quit: ")
			print("Option {} chosen.".format(ChooseAFile))
			ChooseAFile = ChooseAFile.strip()
			if isinstance(ChooseAFile,int):
				if (ChooseAFile > ListLength) or (ChooseAFile < 0 ):
					ChooseAFile = input("Please enter a number! Select a file number or [q] to quit: ")
			if ChooseAFile.upper() =="Q":
				print("Option {} chosen. Quitting.".format(ChooseAFile))
				StartCounter = ListLength
			
			if re.match(regex, ChooseAFile):
				x = int(ChooseAFile)
				ChosenFile = inFileName[x]
				# print(ChosenFile)
				break
			StartCounter = StartCounter + 10
	return ChosenFile			

def WritetoErrorFile(FileName, m3ufile):
    global missingFiles
    missingFiles =  m3ufile + ".err"
    WriteErrs = open(missingFiles, 'a') 
    WriteErrs.writelines(FileName + "\n")
    WriteErrs.close

def MP3toFolder():
	#m3ufile=inm3ufiles
	global m3ufile
	global ExportFiles
	global DestinationStr
	global GlobalOutFileList
	global GlobalSearchQueue

	ExportFileLoc=ExportFiles
	# Using readlines() 
	mp3FileList = []
	counter = 0 
	print("Running MP3toFolder.....")
	print("m3u file name: " + m3ufile)
	isFile = os.path.isfile(m3ufile)
	if isFile:
		file1 = open(m3ufile, 'r', encoding="utf-8") 
		Lines = file1.readlines() 
		m3uFileName = os.path.basename(m3ufile)
		dst = os.path.join(ExportFileLoc,os.path.splitext(m3uFileName)[0])
		DestinationStr = FixSlashes(dst)
		print("Destination: " + DestinationStr)
		file1.close()

	#Check Directory
	isdstDir = os.path.isdir(DestinationStr)
	if not isdstDir:
		os.mkdir(DestinationStr)  
  
	Filecount = 0
	# Strips the newline character 
	for line in Lines: 
		txt = line.strip()
		if not txt.startswith("#"):
			mp3FileList.append(txt)
			#print("Adding line {} as, {}.".format(str(counter),txt))
			counter = counter + 1  


	length = len(mp3FileList)
	print("Length of m3ufiles: " + str(length))
	ListofMissingFiles = []
	for musicfile in mp3FileList:
		Filecount = Filecount + 1
		musicfile = FixSlashes(musicfile)
		BaseName = os.path.basename(musicfile)
		# #PathOnly = os.path.dirname(musicfile)
		cstr = str(Filecount)
		# OrgName = NameOnly
		# NameOnly = cstr.zfill(2) + " - " + NameOnly	
		# #print(NameOnly)
		# FullName = os.path.join(dst,NameOnly)
		# FullName = FixSlashes(FullName)
		#print(FullName)
		#print("Check source file: " + musicfile)
		checkSource = os.path.isfile(musicfile)
		if checkSource:
			#print('Writing {} to {} as Track #: {}'.format(musicfile, DestinationStr, cstr))
			#CopyToExportFolder(musicfile, cstr.zfill(2) )
			GlobalOutFileList.append([musicfile, cstr.zfill(2)])
		else:
			NameOnly = os.path.splitext(BaseName)[0]
			ListofMissingFiles.append([BaseName,cstr.zfill(2)])
			#FoundMusicFile = RecurseDirSearch(NameOnly)
			#if os.path.isfile(FoundMusicFile):
				#CopyToExportFolder(FoundMusicFile,cstr.zfill(2))
	#WritetoErrorFile(ListofMissingFiles)
	GlobalSearchQueue = ListofMissingFiles
	return ListofMissingFiles

def check_space(string): 
    # counter
    count = 0
    # loop for search each index
    for i in range(0, len(string)):
        # Check each char
        # is blank or not
        if string[i] == " ":
            count += 1  
    return count

def CopyToExportFolder(FileNameStr, PositionInt):
		musicfile = FixSlashes(FileNameStr)
		NameOnly = os.path.basename(musicfile)
		#PathOnly = os.path.dirname(musicfile)
		cstr = str(PositionInt)
		OrgName = NameOnly
		NameOnly = cstr.zfill(2) + " - " + NameOnly	
		#print(NameOnly)
		FullName = os.path.join(DestinationStr,NameOnly)
		FullName = FixSlashes(FullName)
		if len(FullName) > 255:
			copyfile("////?//" + musicfile, FullName)
		else:
			copyfile(musicfile, FullName)

def RecurseDirSearch(FileNameStr,CounterStr):
	# Receives a missing file name

	# Loop to pass the search the Global list for the search phrase
	# After first pass, present user with search results
	# Ask if the search should continue with fewer terms
	# On each pass, reduce the search phrase by one term
	# After user has selected the found mp3, copy file to folder
	ListPosInt = 1
	SearchStr = SplitStringforSearch(FileNameStr,ListPosInt)	
	NumberofWordsInt = check_space(SearchStr)
	LoopCounter = NumberofWordsInt
	PickedFileName = ""
	print("Searching for: " + SearchStr + " " + CounterStr)
	while LoopCounter > 0:
		#ErrFileName = SearchforString(SearchStr)
		ErrFileName = initFuzzySearch(SearchStr,5)
		PickedFileName = ChooseFileForCopy(ErrFileName)
		if PickedFileName == '':
			KeepGoing = input("Nothing selected. Keep Going? Y/N: ")
			if KeepGoing.upper() == "N":
				break
		else:
			break
		ListPosInt = ListPosInt + 1
		SearchStr = SplitStringforSearch(FileNameStr,ListPosInt)
		LoopCounter = LoopCounter - 1
	if PickedFileName != '':
		PickedFileName = FixSlashes(PickedFileName)
	return PickedFileName

def MP3FileNameHashSearch(inFileName):
	FileNameHash  = hashlib.sha256(str(inFileName).encode('utf-8')).hexdigest()
	print(FileNameHash)
	OutFileList = []
	for file in GlobalFileList:
		if FileNameHash in file[1]:
			OutFileList.append(file)
	print("Files found:" + str( len(OutFileList)))
	return OutFileList

def RemovefromSeachList(inRemoveFromFileList):
	global GlobalSearchQueue
	tmpGlobalSearchQueue = GlobalSearchQueue
	for rowid in inRemoveFromFileList:
		print("Marked for removal: ")
		print(rowid)
		tmpGlobalSearchQueue.remove(rowid)
	GlobalSearchQueue  = tmpGlobalSearchQueue
	return inRemoveFromFileList


def SearchforMissingFiles01():
	OutFileList = []
	RemoveFromFileList = []
	RemainingFiles = []
	FileListIndex = 0
	global GlobalSearchQueue
	inMissingFileList = GlobalSearchQueue
	print("Initiate Search #1....") 

	for searchfile in inMissingFileList:
		FileName  = searchfile[0]
		FileName = FixSlashes(FileName)
		FileName = os.path.basename(FileName)
		print("Searching for: " + FileName)
		PlaylistNbr = searchfile[1]
		FileNameHash  = hashlib.sha256(str(FileName).encode('utf-8')).hexdigest()
		for file in GlobalFileList:
			if FileNameHash in file[1]:
				GlobalOutFileList.append([file[0],PlaylistNbr])
				#OutFileList.append([file[0],PlaylistNbr])
				RemoveFromFileList.append([searchfile[0],searchfile[1]])
				break
		FileListIndex = FileListIndex + 1
		print("Files found:" + str( len(OutFileList)))
	if len(RemoveFromFileList) >0:
		print("Start removal.......")
		RemainingFiles  = RemovefromSeachList(RemoveFromFileList)
	return RemainingFiles

def SearchforMissingFiles02():
	StatusCounter = 1
	RemoveFromFileList = []
	RemainingFiles = []
	global GlobalSearchQueue
	inMissingFileList = GlobalSearchQueue
	print("Initiate Search #2....") 

	for f in inMissingFileList:
		StatusCounterStr = str(StatusCounter) + ' of ' + str(len(GlobalSearchQueue)) + "."
		SearchStr = SplitStringforSearch(f[0],1)
		print("Searching for: " + SearchStr + " " + StatusCounterStr)
		FoundMusicFileList = initFuzzySearch(SearchStr,0)
		if len(FoundMusicFileList) > 0:
			FoundMusicFile = FoundMusicFileList[0]
			print("Found: " + FoundMusicFile)
			if os.path.isfile(FoundMusicFile):
				GlobalOutFileList.append([FoundMusicFile, f[1]])
				RemoveFromFileList.append([f[0], f[1]])
		StatusCounter = StatusCounter + 1
	if len(RemoveFromFileList) >0:
		print("Start removal.......")
		RemainingFiles  = RemovefromSeachList(RemoveFromFileList)
	return RemainingFiles

def SearchforMissingFiles03():
	StatusCounter = 1
	RemoveFromFileList = []
	RemainingFiles = [] 
	global GlobalSearchQueue
	inMissingFileList = GlobalSearchQueue
	print("Initiate Search #3....") 

	for f in inMissingFileList:
		ListPosInt = 1
		StatusCounterStr = str(StatusCounter) + ' of ' + str(len(GlobalSearchQueue)) + "."
		#SearchStr = RemoveNumPrefixforSearch(f[0],1)
		FileName = f[0]
		print("Searching for: " + FileName + " " + StatusCounterStr)
		LoopCounter =  FileName.count(' ') - 1
		while LoopCounter > 0:
			SearchStr = SplitStringforSearch(f[0],ListPosInt)
			FoundMusicFileList = initFuzzySearch(SearchStr,0)
			if len(FoundMusicFileList) > 0:
				FoundMusicFile = FoundMusicFileList[0]
				#print("Found: " + FoundMusicFile)
				if os.path.isfile(FoundMusicFile):
					print("Found: " + str(FoundMusicFile))
					GlobalOutFileList.append([FoundMusicFile, f[1]])
					RemoveFromFileList.append([f[0], f[1]])
					break
			ListPosInt = ListPosInt + 1
			LoopCounter = LoopCounter - 1
		StatusCounter = StatusCounter + 1
	
	if len(RemoveFromFileList) >0:
		print("Start removal.......")
		RemainingFiles  = RemovefromSeachList(RemoveFromFileList)
	return RemainingFiles

def SearchforMissingFiles04():
	StatusCounter = 1
	RemoveFromFileList = [] 
	RemainingFiles = []
	global GlobalSearchQueue
	inMissingFileList = GlobalSearchQueue
	print("Initiate Search #4....") 

	for f in inMissingFileList:
		StatusCounterStr = str(StatusCounter) + ' of ' + str(len(GlobalSearchQueue)) + "."
		FoundMusicFile =RecurseDirSearch(f[0], StatusCounterStr)
		if os.path.isfile(FoundMusicFile):
			GlobalOutFileList.append([FoundMusicFile, f[1]])
			RemoveFromFileList.append([f[0], f[1]])
		StatusCounter = StatusCounter + 1
	
	if len(RemoveFromFileList) >0:
		print("Start removal.......")
		RemainingFiles  = RemovefromSeachList(RemoveFromFileList)
	return RemainingFiles


def initFuzzySearch(inFileName,inDistance):
	global GlobalFileList
	Distance = int(inDistance)
	SortSearch = []
	OutPutList = []
	FileNameRowID = 0
	#print("Searching for...." + inFileName)
	for FileName in GlobalFileList:
		SearchObject = os.path.basename(FileName[0])
		FindFile = find_near_matches(inFileName, SearchObject, max_l_dist=5)
		if FindFile:
			if FindFile[0].dist <= Distance:
				#print(FileName)
				#SortSearch.append({'rowid':FileNameRowID, 'startval':FindFile[0].start })
				SortSearch.append([FileName[0], FindFile[0].dist])
		FileNameRowID = FileNameRowID + 1
		SortSearch.sort(key=lambda SortSearch: SortSearch[1])
	#print(SortSearch[0])
	for j in SortSearch:
		OutPutList.append(j[0])
	return OutPutList


def FlushtoExport():
	global GlobalOutFileList
	global m3ufile
	global ExportFiles

	m3uFileName = os.path.basename(m3ufile)
	NameOnly = os.path.splitext(m3uFileName)[0]
	counter = 1
	for mp3file in GlobalOutFileList:
		FileNameStr = mp3file[0]
		PositionInt = mp3file[1]
		MusicFileNameOnly = os.path.basename(FileNameStr)		
		print("...Writing " + MusicFileNameOnly + " to " +  NameOnly)
		CopyToExportFolder(FileNameStr, PositionInt)
		counter = counter + 1
	print("Songs written to playlist " + m3ufile + ": " + str(counter))	

def FlushtoErrFile():
	global GlobalSearchQueue
	global m3ufile
	for mp3file in GlobalSearchQueue:
		FileNameStr = mp3file[1] + " " + mp3file[0]
		#PositionInt = GlobalSearchQueue[1]
		WritetoErrorFile(FileNameStr, m3ufile)		
		#CopyToExportFolder(FileNameStr, PositionInt)

def main():
	#m3ufile = "/Users/chadmonden/Dropbox/music/playlists/12-13-20.m3u"
	global SearchLocation
	#SearchLocation = "E://Temp"

	#print(m3ufile)
	#print(ExportFiles)
	#print(missingLoc)
	#print(SearchLocation)
	#ListofMissingFiles = MP3toFolder(m3ufile,ExportFiles)
	#WritetoErrorFile(ListofMissingFiles, m3ufile) 
	#ListPosInt = input("Enter Integer Value:")
	#ListPosInt = int(ListPosInt)
	ListPosInt = 1
	#print(SplitStringforSearch('86 Paper Planes-Clean',ListPosInt))
	#print(SearchforString('Paper Planes',SearchLocation))
	#GetFiles = SearchforString('Paper Planes',SearchLocation)
	#print(len(GetFiles))

	#SearchString = '86 Paper Planes-Clean'
	SearchString = '86 Paper Planes-Clean'
	#SearchString = 'Paper Planes'
	#SearchString = '00 - Paper Planes(Clean) Ft. Bun B & Rich Boy.mp3'
	#GetFiles = SearchforString(SearchString)
	#print(ChooseFileForCopy(GetFiles))	


	MissingFiles01 = MP3toFolder()
	print("Missing files: " + str(len(GlobalSearchQueue)))
	
	if DoDeepSearch >= "1":
		IntializeGlobalFileList(SearchLocation)
		MissingFiles02 = SearchforMissingFiles01()
		print("Remaining missing files: " + str(len(GlobalSearchQueue)))
		MissingFiles03 = SearchforMissingFiles02()
		print("Remaining missing files: " + str(len(GlobalSearchQueue)))
		MissingFiles04 = SearchforMissingFiles03()
		print("Remaining missing files: " + str(len(GlobalSearchQueue)))
		MissingFiles05 = SearchforMissingFiles04()
		print("Remaining missing files: " + str(len(GlobalSearchQueue)))

	FlushtoExport()
	FlushtoErrFile()
	#initFuzzySearch(SearchString)
	#print("Final Remaining Missing files: " + str(len(MissingFiles03)))	

	""" MissingFiles01 = MP3toFolder()
	MissingFiles02 = SearchforMissingFiles01(MissingFiles01)
	
	
	for files in MissingFiles03:
		print (files[1] + " " + files[0])
 """	#print(len(MissingFiles))
	#print(MP3FileNameHashSearch(SearchString))
if __name__ == "__main__":
    main()
