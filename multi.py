import multiprocessing as mp 


def tp1(manlist,sqlist):
	print manlist
	for x in manlist:
		square=x*x 
		print "square:",square
		sqlist.append(square)

def tp2(manlist,cubelist):
	print manlist
	for x in manlist:
		cube=x*x*x
		print "cube:",cube
		cubelist.append(cube)


if __name__=="__main__":

	with mp.Manager() as manager:
 
		numlist=[1,2,3]
		
		manlist=manager.list(numlist)
		
		sqlist=manager.list()
		cubelist=manager.list()


		p1=mp.Process(target=tp1,args=(manlist,sqlist))
		p2=mp.Process(target=tp2,args=(manlist,cubelist))

		

		p1.start()
		p2.start()
		p1.join()
		p2.join()

		
		
		print sqlist
		print cubelist


