import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import math

# from classifier, take classifier.Train[:,-1]
# Use the labels dict that k means return to select only those indices from y corrosponding to one cluster
# use np unique (return counts) to find the majority element and assign it the class label
# Do checks that the majority is at least 50%
# Also, check that every majority label  is different

class k_means:
	def __init__(self,k,inputs,names,test,mode,covar):
		# mode = {0 : Euclidean, 1: Manhattan, 2 : Chebyshev}
		self.covar = covar
		if mode == 3:
			self.covarinv = np.linalg.inv(self.covar)
		self.mode = mode
		self.k = k
		self.input = inputs
		n = len(inputs[0])
		self.means_arr = np.zeros((k,n))
		self.labels = {}
		self.names = names
		for i in range(0,k):
			labelList=[]
			self.labels.update({i:labelList})
		self.test = test

	def init_guess(self):
		a = len(self.input[0])
		arr = np.zeros((self.k,a))
		row_nos = len(self.input)
		rows = []
		j=0
		while(j<self.k):
			i = random.randint(0,row_nos-1)
			if(i not in rows):
				rows.append(i)
				j+=1
			else :
				continue
		for i in range(0,self.k):
			arr[i] = self.input[rows[i]]
		self.means_arr = arr

	def normalise(self):
		m = len(self.input)
		n = len(self.input[0])
		for i in range(0,n):
			maxs = max(self.input[:,i])
			mins = min(self.input[:,i])
			self.input[:,i] = (self.input[:,i]-mins)/(maxs-mins)

	def distance(self, data1, data2):


		if self.mode == 0:
			n = len(data1)
			dis = 0
			for i in range(0,n):
				dis+=pow(data1[i]-data2[i],2)
			dis = pow(dis,0.5)
			return dis

		if self.mode == 1:
			n = len(data1)
			dis = 0
			for i in range(0,n):
				dis+=math.fabs(data1[i]-data2[i])
			return dis

		if self.mode == 2:
			n = len(data1)
			dis = 0
			for i in range(0,n):
				x = math.fabs(data1[i]-data2[i])
				if x > dis:
					dis=x
			return dis

		if self.mode == 3:
			dis = np.matmul(np.matmul((data1 - data2).transpose(),self.covarinv),data1-data2)
			return dis**0.5
			

	def allocate(self, data, position):
		dis = len(self.input[0])
		pos = 0
		n = self.k
		for i in range(0, n):
			a = self.distance(data, self.means_arr[i])
			if(a<dis):
				dis = a
				pos = i
		if(position in self.labels[pos]):
			return
		else:
			self.labels[pos].append(position)

	def allocation(self):
		for i in range(0,len(self.input)):
			self.allocate(self.input[i],i)

	def update(self):
		b = False
		for i in range(0, self.k):
			lista = self.labels[i]
			init_arr = self.means_arr[i]
			arr = np.zeros(len(self.input[0]))
			n = len(lista)
			if(n==0):
				continue
			for items in lista:
				arr+=self.input[items]
			arr = arr/n
			self.means_arr[i] = arr
			if(np.array_equal(arr,init_arr)):
				continue
			else:
				b=True
		return b

	def printarr(self):
		for i in range(0, len(self.input)):
				print (self.input[i])

	def printmeans(self):
		print(self.means_arr)

	def printlabels(self):
		print(self.labels)

	def apply(self):
		self.normalise()
		self.init_guess()
		b = True
		counter = 0
		while(b and counter<=1000000):
			self.allocation()
			b = self.update()

	def find(self, i): 
		for j in range(0, self.k):
			if(i in self.labels[j]):
				return j
		return -1

	def rms(self):
		dis = 0
		#print("**")
		for i in range(0,len(self.input)):
			a = self.find(i)
			#print(a)
			dis+=self.distance(self.input[i],self.means_arr[a])
		#print("**")
		return dis

	def printall(self):
		self.printmeans()
		self.printlabels()
		self.printrms()

	def printrms(self):
		print(self.rms())

	def allot(self):
		ans = []
		for labels in self.labels:
			indices = self.labels[labels]
			arr = self.names[indices]
			u,ver  = np.unique(arr, return_counts = True)
			print(u)
			print(ver)
			a = 0
			for i in range(0,len(ver)):
				if(ver[a]<ver[i]):
					a = i
			ans.append(u[a])
		return ans

	def assign(self):
		n = len(self.test)
		test = self.test
		arr = np.zeros(n)
		means = self.means_arr
		for i in range(0,n):
			dis = self.distance(test[i],means[0])
			min_k = 0
			for j in range(0,self.k):
				new_dis = self.distance(test[i],means[j])
				if(dis>new_dis):
					dis = new_dis
					min_k = j
			arr[i] = min_k
		return arr

def kfit(arr,k,names,test,num_runs = 100,mode = 0,covar=-1):
	rms  = len(arr)*(len(arr[0]))
	min_arr = np.zeros((k, len(arr[0])))
	dic = {}
	for alpha in range(num_runs):
		# print(alpha)
		experiment = k_means(k, arr,names,test,mode,covar)
		experiment.apply()
		if(rms > experiment.rms()):
			rms = experiment.rms()
			dic = experiment.labels
			min_arr = experiment.means_arr
	experiment.labels = dic
	experiment.means_arr = min_arr
	arr_assign = experiment.assign()
	ans = experiment.allot()
	for i in range(0,len(arr_assign)):
		# print(arr_assign[i])
		arr_assign[i] = ans[int(arr_assign[i])]
	print(ans)
	# print(rms)
	return experiment.labels, experiment.means_arr, rms, arr_assign

def visualizeKMeans(data,labelDict,k):
	colors = ("red", "green", "blue")
	groups = ("HEALTHY", "MEDICATION", "SURGERY") 
	groupedData = []
	for label in labelDict:
		indices = labelDict[label]
		groupedData.append(data[indices,:].transpose())

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
	ax = fig.gca(projection='3d')

	for d, c, g in zip(groupedData, colors, groups):
		x, y, z = d
		ax.scatter(x, y, z, alpha=0.8, c=c, edgecolors='none', s=30, label=g)
	 

	plt.title('Matplot 3d scatter plot')
	plt.legend(loc=2)
	plt.show()

# self.normalise()
# 		self.init_guess()
# 		b = True
# 		counter = 0
# 		while(b and counter<=1000000):
# 			self.allocation()
# 			b = self.update()
# 		self.printlabels()
# 		self.printmeans()


def main():
	file = open("test_arr.txt","r")
	test_arr = np.asarray([[float(x) for x in line.split()] for line in file])
	file.close()
	kfit(test_arr[:,:-1],2,test_arr[:,-1],test_arr[:,:-1])

if __name__=="__main__":
	main()
