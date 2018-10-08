#### Functions to visualize data graphically ####

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import Preprocessing
from cycler import cycler

sns.set(color_codes=True)

def visualiseCCD(X,c,i):
	# print(X.shape)
	# X = X.astype(np.float64)
	sns.distplot(X);
	plt.title("CCD for class "+str(c)+" and feature "+str(i))
	plt.show()

def visualizeDataCCD(X):
	
	sliced_matrix = sliceMatrix(X)

	for label in sliced_matrix:
		mat = sliced_matrix[label]
		for i in range(mat.shape[1]):
			print(i)
			visualiseCCD(mat[:,i],label,i)
		# visualiseCCD(mat[:,0],label,0)


def visualizeConfusion(X):
	ax = sns.heatmap(X, annot=True, fmt="d", cbar = False)

	plt.title('Confusion matrix')
	plt.ylabel('True Class')
	plt.xlabel('Predicted Class')
	plt.show()

def visualizeCorrelation(cor_dict):

	for label in cor_dict:
		x = cor_dict[label]
		ax = sns.heatmap(x)
		plt.title('Correlation matrix for class '+str(int(label)))
		plt.ylabel('Features')
		plt.xlabel('Features')
		plt.show()

def visualizeKMeans(data,labelDict,k):
	colors = ("red", "green", "blue")
	groups = ("Class 0", "Class 1", "Class 2") 
	groupedData = []
	for label in labelDict:
		indices = labelDict[label]
		groupedData.append(data[indices,:].transpose())

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
	ax = fig.gca(projection='3d')

	for d, c, g in zip(groupedData, colors, groups):
		x, y, z = d
		ax.scatter(x, y, z, alpha=0.8, c=c, edgecolors='none', s=30, label=g)

	plt.title('3d KNN scatter plot')
	plt.legend(loc=2)
	plt.show()
	
def var_vs_comp(X, start, stop, step):
	print("Making variance v/s components plot. . . ")
	components = []
	variances = []
	d = X.shape[1]
	i_cols = np.arange(start, stop, step)
	for k in i_cols:
		pca = Preprocessing.PCA(X, k = k, whiten = False)
		components.append(k)
		variances.append(pca.var_retained)
		
	plt.plot(components, variances)
	plt.ylabel('variance retained')
	plt.xlabel('number of components')
	plt.show()

def comp_vs_var_accuracy():
	n_cols = [1,2,5,10,20,40,80,160,320,640,784]
	var_retained = [22,36.4,51.1,62,70,77,85,91.4,96.4,99.6,100]
	accuracy = [27.7,45.6,59.3,65.3,67.1,68.4,69.5,69.0,69.2,69.3,69.3]

	plt.gca().set_prop_cycle(cycler('color',['r', 'g']))
	plt.plot(n_cols,var_retained)
	plt.plot(n_cols,accuracy)
	plt.xlabel('No. of components')
	plt.legend(['Variance Retained', 'Accuracy'], loc='upper left')
	plt.show()

def plotBayesvsNaiveBayes():
	n_cols = [10,30,50,80]
	bayes = [70.2,70.67,70.84,70.51]
	naive = [65.65,65.58,68.78,69.51]

	plt.gca().set_prop_cycle(cycler('color',['r', 'g']))
	plt.plot(n_cols,bayes)
	plt.plot(n_cols,naive)
	plt.xlabel('No. of components')
	plt.legend(['Multivariate Bayes', 'Naive Bayes'], loc='upper left')
	plt.show()


def visualizeDataPoints(X):
	# data is complete matrix with labels

	colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w',(0.5,0.5,0.7),(0.9,0.2,0.7))
	groups = ("Class 0", "Class 1", "Class 2","Class 3", "Class 4", "Class 5","Class 6", "Class 7", "Class 8","Class 9") 

	sliced_matrix = sliceMatrix(X)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1, facecolor="1.0")
	ax = fig.gca(projection='3d')

	i=0
	for label in sliced_matrix:
		mat_trans = sliced_matrix[label].transpose()
		ax.scatter(mat_trans[0], mat_trans[1], mat_trans[2], alpha=0.8, c=colors[i], edgecolors='none', s=30, label=groups[i])
		i+=1

	plt.title('3d data scatter plot')
	plt.legend(loc=2)
	plt.show()

def sliceMatrix(X):
	# X is complete data matrix with the label
	N = X.shape[0]	
	# sorting according to Y
	X = X[X[:,X.shape[1]-1].argsort()]
	# slicing matrix acc. to classes
	sliced_matrix = {}
	x = X[0][len(X[0])-1]
	last_index = 0
	for i in range(1, X.shape[0]):
		elem = X[i]
		q = elem[len(elem)-1]
		if q!= x:
			sliced_matrix[x] = X[last_index:i, :X.shape[1]-1]
			last_index = i
		x = q
	sliced_matrix[x] = X[last_index:X.shape[0], :X.shape[1]-1]

	return sliced_matrix


