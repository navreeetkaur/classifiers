import inputReader
import performanceAnalyser
import numpy as np

class multi_perceptron:
	def __init__(self,input_data,labels,num_classes,test_data):
		self.input_data = input_data
		self.labels = labels
		self.num_classes = num_classes
		a = len(input_data[0])
		self.weights = np.zeros((num_classes,a))
		self.test_data = test_data

	def change_weights(self,instance,label,weight_instance,desired_label):
		pred = weight_instance.dot(instance)
		if(pred>0 and label==desired_label):
			return weight_instance
		elif(pred<0 and label!=desired_label):
			return weight_instance
		elif(pred<=0 and label==desired_label):
			a = weight_instance+instance
			return a
		elif(pred>=0 and label!=desired_label):
			a = weight_instance-instance
			return a

	def process(self,iterations):
		n = len(self.input_data)
		for i in range(0,iterations):
			for j in range(0,n):
				a = self.input_data[j]
				label = self.labels[j]
				for l in range(0,self.num_classes):
					desired_label = l
					instance = a
					weight_instance = self.weights[l]
					b = self.change_weights(instance,label,weight_instance,desired_label)
					self.weights[l] = b

	def pred(self):
		predictions = np.zeros(self.num_classes)
		test_data = self.test_data
		n = len(test_data)
		output = np.zeros(n)
		for i in range(0,n):
			for j in range(0,self.num_classes):
				predictions[j] = self.weights[j].dot(test_data[i])
			output[i] = np.argmax(predictions)
		return output

def main():
	inp = inputReader.InputReader('railwayBookingList.csv',2)
	training_data = inp.Train
	test_data = inp.Test[:,:-1]
	ytrue = inp.Test[:,-1]
	input_data = training_data[:,:-1]
	labels = training_data[:,-1]
	per = multi_perceptron(input_data,labels,2,test_data)
	per.process(5)
	ypred = per.pred()
	print(performanceAnalyser.calcAccuracyTotal(ypred,ytrue))

if __name__=="__main__":
	main()
