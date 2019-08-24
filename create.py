print("create.py for jfDataBase by jonnelafin")
print("pressing enter will erase the database files.")
size = int(input("Size: "))
name = input("Name: ")
with open(name+'.jfDB', 'w+') as f:
		f.truncate(0)
		f.write("0"*size)
with open(name+'_record.jfDBR', 'w+') as f:
		f.truncate(0)
print("Done")
