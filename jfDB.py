try:
   import readline
except:
   print("Couldn't import readline")
import os

rows, columns = os.popen('stty size', 'r').read().split()

version = "beta 0.1"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def done():
	print(bcolors.OKGREEN + "Completed succesfully." + bcolors.ENDC)
def faild(error):
	print(bcolors.FAIL + "Error: " + str(error) + bcolors.ENDC)
def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
		  return input(prompt)  # or raw_input in Python 2
   finally:
		  readline.set_startup_hook()

def empty_db():
	with open('database.jfDB','w'): pass
def load():
	with open('database_record.jfDBR', 'r+') as f:
#		print(f.readlines())
		outp = f.readlines()
	return outp
def parseLines(complete):
	names = []
	name = ""
	for i in list(complete):
		if(i == "\n"):
			names.append(name)
#			print(name)
			name = ""
		else:
			name = name + i
	return names
def getNames(lines):
	names = []
	for y in lines:
		names.append(y.split()[0])
	return names
def getStarts(complete):
	starts = []
	for y in complete:
		starts.append(int(y.split()[1]))
	return starts
def getEnds(complete):
	ends = []
	for y in complete:
		ends.append(int(y.split()[2]))
	return ends
def getSizes(starts, ends):
	sizes = []
	for i in range(len(starts)):
		size = ends[i] - starts[i]
		sizes.append(size)
	return(sizes)
def stats(names, starts, ends, sizes, size, full):
	title = "JFDataBase " + version
	fill = "█"*int((int(int(columns) - len(title))/2))
	print(bcolors.HEADER + fill + title + fill + bcolors.ENDC)
	title = "Operating database.jfDB with the database size of " + str(size)
	fill = "█"*int((int(int(columns) - len(title))/2))
	print(bcolors.HEADER + fill + title + fill + bcolors.ENDC)
	title = "------CONTENTS:------"
	fill = "█"*int((int(int(columns) - len(title))/2))
	print(bcolors.OKBLUE + fill + title + fill + bcolors.ENDC)
#	print(bcolors.HEADER + "█" * int(columns) + bcolors.ENDC)
	print()
	for i in range(len(names)):
		title = "name: " + names[i]
		fill = "█"*int((int(int(columns) - len(title))/2))
		print(fill + title + fill)
		print("index: "+str(i+1))
		print("		from: "+str(starts[i]))
		print("		to: "+str(ends[i]))
		print("		size: "+str(sizes[i]))
		print("########################")
	print(str(full) + " units used of "+str(size))
def read(start, end):
	with open("database.jfDB", encoding = "ISO-8859-1") as fin:
				fin.seek(start)
				data = fin.read(end - start)
	return data
exit = 0
while exit == 0:
	complete = load()
	names = getNames(complete)
	starts = getStarts(complete)
	ends = getEnds(complete)
	sizes = getSizes(starts, ends)
	full = 0
	for x in sizes:
		full = full + x
	db_size = os.path.getsize('database.jfDB')
	try:
		os.system("cls")
		os.system("clear")
	except:
		print("Couldn't clear screen")
	stats(names, starts, ends, sizes, db_size, full)
	print("Commands:")
	print("-1: add a new entry")
	print("-2: delete an entry")
	print("-3: edit an entry")
	print("0: exit")
	print("Please choose an entry to read (0-"+str(len(names))+"), or type in a direct command")
	
	choice = int(input("Input: "))
	
	if choice == 0:
		exit = 1
		break
	elif choice == -1:
		end_max = 0
		for end in ends:
			if end > end_max:
				end_max = end
		name = input("Name: ")
		has = False
		for nam in names:
			if nam == name:
				faild("Name Already Exists")		
				has = True
		if has == False:
			size = int(input("Size: "))
			with open('database_record.jfDBR', 'a+') as f:
				f.write(name +" "+str(end_max)+" "+str(end_max+size)+"\n")
	elif choice == -2:
		index = int(input("index to delete: "))-1
		with open("database_record.jfDBR", "r+") as f:
					d = f.readlines()
					f.seek(0)
					for i in range(len(d)):
							if i != index:
										f.write(d[i])
					f.truncate()
	elif choice == -3:
		index = int(input("Index to edit: "))-1
		e_start = starts[index]
		e_end = ends[index]
		print("editing from "+str(e_start)+" to "+str(e_end))
		e_current = read(e_start, e_end)
		e_size = e_end - e_start
		print("with the size of "+ str(e_size))
		try:
			e_new = rlinput("Edit: ", e_current)
		except:
			print("Old:" + e_current)
			e_new = input("New: ")
		if len(e_current) > len(e_new):
			e_new = e_new + str("0"*(len(e_new)-size))
		if e_size < len(e_new):
			print(bcolors.WARNING + "Too big for the chosen entry size, cutting..." + bcolors.ENDC)
			e_new = e_new[:len(e_current)]
		with open("database.jfDB", "r+") as f:
			old = read(0, db_size)
			empty_db()
			old = old[:e_start] + old[:e_end]
			new = old[:e_start] + e_new + old[e_start:]
			f.seek(0) # rewind
			f.write(new) # write the new line before
	elif choice == -4:
		index = int(input("index to purge: "))-1
		e_start = starts[index]
		e_end = ends[index]
		e_current = read(e_start, e_end)
		e_new = "0"*len(e_current)
		with open("database_record.jfDBR", "r+") as f:
					d = f.readlines()
					f.seek(0)
					for i in range(len(d)):
							if i != index:
										f.write(d[i])
					f.truncate()
		with open("database.jfDB", "r+") as f:
			old = read(0, db_size) # read everything in the file
			old = old[:e_start] + old[:e_end]
			new = old[:e_start] + e_new + old[e_start:]
			empty_db()
			f.seek(0) # rewind
			f.write(new) # write the new line before
	elif choice == -5:
		print(bcolors.WARNING + "Using manual purge might be dangerous if used incorrectly." + bcolors.ENDC)
		print("file end:" + str(db_size))
		proceed = input("Proceed? (y/n):")
		if(proceed == "y"):
			p_start = int(input("from: "))
			p_end = int(input("end: "))
			with open("database.jfDB", "r+") as f:
				old = read(0, db_size) # read everything in the file
				old = old[:p_start] + str("0"*(p_end - p_start)) + old[:p_end]
				empty_db()
				f.seek(0) # rewind
				f.write(old) # write the new line before
	else:
		tindx = choice - 1
		try:
			data = read(starts[tindx], ends[tindx])
		except Exception as e:
			faild(e)
			data = "operation failed"
		toprint = ""
		lasti = ""
		for i in data:
			if i != "*":
				toprint = toprint + i
			else:
				print(toprint)
				toprint = ""
			lasti = i
		print(toprint)
print("Exit code " + str(exit))
