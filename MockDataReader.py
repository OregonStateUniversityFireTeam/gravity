import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--filename", type=str, default="dataset1.txt", help="the name of the file to read")

	args = parser.parse_args()
	
	
	ReadDataSet()

def ReadDataSet(filename="dataset1.txt"):

	f = open(filename, 'r')
	
	dataset = [[],[]]
	lastline = False
	
	#read, line by line, and populate a new dataset
	for thisline in f:
		if not lastline:
			if not "#Final" in thisline:
				if not "#" in thisline:
					splitline = str.split(thisline, ",")
					ident = str.split(splitline[0], "_")
					lin = int(ident[1])
					yr = int(ident[3])
					if lin >= len(dataset[0]):
						dataset[0].append([])
					dataset[0][lin].append([]) 
					for element in range(1,len(splitline)):
						dataset[0][lin][yr].append(int(splitline[element])) 
						
			else:
				#this line contains "#Final" which means it's the second-to-last
				#so, read the next line
				lastline = True
				
		else:
			splitline = str.split(thisline, ",")
			for element in range(len(splitline)):
				dataset[1].append(int(splitline[element]))
	
	return dataset
			

if __name__ == "__main__":
   main()