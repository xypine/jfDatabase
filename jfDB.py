try:
   import readline
except:
   print("Couldn't import readline")
import os

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
		  return input(prompt)  # or raw_input in Python 2
   finally:
		  readline.set_startup_hook()


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
def stats(names, starts, ends):
	print("------CONTENTS:------")
	for i in range(len(names)):
		print("name: " + names[i])
		print("index: "+str(i+1))
		print("		from: "+str(starts[i]))
		print("		to: "+str(ends[i]))
		print("########################")
def read(start, end):
	with open("database.jfDB") as fin:
				fin.seek(start)
				data = fin.read(end - start)
	return data
exit = 0
while exit == 0:
	complete = load()
	names = getNames(complete)
	starts = getStarts(complete)
	ends = getEnds(complete)
	stats(names, starts, ends)
	print("Commands:")
	print("-1: add a new entry")
	print("-2: delete an entry")
	print("-3: edit an entry")
	print("0: exit")
	print("Please choose an entry to read (0-"+str(len(names))+"), or type in a direct command")
	choice = int(input("Input: "))
	try:
		os.system("clear")
	except:
		try:
			os.system("cls")
		except:
			print("Couldn't erase screen")
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
				print("already exists")			
				has = True
		if has == False:
			size = int(input("Size: "))
			with open('database_record.jfDBR', 'a+') as f:
				f.write(name +" "+str(end_max+1)+" "+str(end_max+1+size)+"\n")
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
		print("with the size of "+ str(len(e_current)))
		try:
			e_new = rlinput("Edit: ", e_current)
		except:
			print("Old:" + e_current)
			e_new = input("New: ")
		if len(e_current) > len(e_new):
			e_new = e_new + str("0"*(len(e_current)-len(e_new)))
		if len(e_current) < len(e_new):
			print("Too big for the chosen entry size, cutting...")
			e_new = e_new[:len(e_current)]
		with open("database.jfDB", "r+") as f:
			old = f.read() # read everything in the file
			f.truncate()
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
			old = f.read() # read everything in the file
			f.truncate()
			old = old[:e_start] + old[:e_end]
			new = old[:e_start] + e_new + old[e_start:]
			f.seek(0) # rewind
			f.write(new) # write the new line before
	else:
		tindx = choice - 1
		data = read(starts[tindx], ends[tindx])
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
