import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

r = 40
s = 60
fps = 25
deltaTimeForVelodiagram = 10
deltaTimeForAntsInCenter = 250


def velodiagram(filename, file = False):
	if file:
		fileSpeed = open(filename)
		speed = [float(fileSpeed.readline()[0:-1])]

		while True:
			speedValue = fileSpeed.readline()
			if speedValue == "":
				break
			speed.append(float(speedValue))
	else:
		speed = filename

	speed = [i for i in speed if i <= 7]
	t = np.arange(0.0, len(speed)/(fps/deltaTimeForVelodiagram), 0.4)
	fig = plt.figure(figsize=(10, 5))

	vax = fig.add_subplot(121)
	vax.vlines(t, [0], speed)

	vax.set_xlabel('time (s)')
	vax.set_ylabel('speed (v)')
	vax.set_title("Ant's average speed")
	plt.savefig('averageVelocityDiagramm.png', format = 'png')
	#plt.show()


def antsInCenterDiagram(filename, file = False):
	if file:
		fileTime = open(filename)
		time = [float(fileTime.readline()[0:-1])]

		while True:
			timeValue = fileTime.readline()
			if timeValue == "":
				break
			time.append(float(timeValue))
	else:
		time = filename

	t = np.arange(0.0, len(time)/(fps/deltaTimeForVelodiagram), 10)
	fig = plt.figure(figsize=(10, 5))
	
	vax = fig.add_subplot(122)
	vax.vlines(t, [0], time)

	vax.set_xlabel('time (s)')
	vax.set_ylabel('time in center(t)')
	vax.set_title("Ant's time in center")

	#plt.show()

def threeD_Graf(filename, file = False):
	if file:
		file1 = open(filename)
		speed = [list(map(float, file1.readline()[0 : -1].split()))]

		while True:
			a = file1.readline()
			if a == "":
				break
			speed.append(list(map(float, a.split())))

	else:
		speed = filename

	fig = plt.figure()
	axes = fig.gca(projection = '3d')

	x = [speed[i][0] for i in range(0, len(speed))]
	y = [speed[i][1] for i in range(0, len(speed))]
	z = np.arange(0, len(y) / 2.5, 0.4)
	axes.plot(x, y, z)
	plt.savefig('3dGraph.png', format = 'png')
	#plt.show()

def piechart(s,r):
	stay = s
	run  = r
	labels = 'Stay ', 'Run'
	sizes = [stay, run]
	explode = (0.1, 0.0)  #пробелы между частями
	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode = explode, labels = labels, autopct = '%1.1f%%', shadow = True, startangle = 90)
	ax1.axis('equal')  
	plt.savefig('piechart.png', format = 'png')
	#plt.show()
	
	


if __name__ == '__main__':
	#diagrams("avvelo.txt", file = True)
	antsInCenterDiagram("valuesOfMovingInCenter.txt", file = True)
	threeD_Graf("track.txt", file = True)
	piechart(r,s)
	

