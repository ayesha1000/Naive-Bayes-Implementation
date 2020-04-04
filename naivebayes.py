from math import sqrt
from math import exp
from math import pi
from csv import reader

#loading file containing dataset
def load_file(filename):
  dataset=list() #for storing rows in dataset
  with open(filename,'r') as file:
    data=reader(file)
    for row in data:
      if not row:
        continue
      dataset.append(row) #converting dataset in file to list of ordered collectiom
    return dataset

#converting string-to-float 
def column_str_to_float(dataset,column):
  for row in dataset:
    row[column]=float(row[column].strip())
 
#converting class column to int Value
def column_str_to_int(dataset,column):
  class_values=[row[column] for row in dataset]
  unique=set(class_values)
  lookup = dict()
  #making a mapping function for classes
  print('CLASSES:')
  for i, value in enumerate(unique):
    lookup[value] = i
    print('%s => %d' % (value, i))
  print('----------------------------')
  #changing string class value to integer value 
  for row in dataset:
    row[column] = lookup[row[column]]
  return lookup

def str_to_int(dataset,column):
  class_values=[row[column] for row in dataset]
  unique=set(class_values)
  lookup = dict()
  #making a mapping function for classes
  print('DEPARTMENTS:')
  for i, value in enumerate(unique):
    lookup[value] = i
    print('%s => %d' % (value, i))
  print('----------------------------')
  #changing string class value to integer value 
  for row in dataset:
    row[column] = lookup[row[column]]
  return lookup
  
#splitting data set by class  
def split_data_by_class(dataset):
  separated = dict()
  for i in range(len(dataset)):
    vector = dataset[i]
    class_value = vector[-1]  
    #making each record of seperated dictionary a list
    if (class_value not in separated):
      separated[class_value] = list()     
    separated[class_value].append(vector)#appending row with its class list
  return separated  

#calculating mean for dataset\
def mean(values):
  avg=sum(values)/float(len(values))
  return avg

#calculating standard deviation
def standard_deviation(values):
  avg=mean(values)
  variance=sum([(x-avg)**2 for x in values])/float(len(values)-1)
  stdev=sqrt(variance)
  return stdev

def data_calculation(dataset):
  summaries = [(mean(column), standard_deviation(column), len(column)) for column in zip(*dataset)]
  del(summaries[-1])
  return summaries

#splitting data set by classes and performing calculations
def class_calculation(dataset):
  #1. Splitting the data by the classes which were converted to integer values
  #2. Calculating mean and standard deviation for each column of each class_calculation
  #3. storing values of each row in a dictionary summary according to each class
  split=split_data_by_class(dataset)
  summary=dict()
  for value,rows in split.items():
    summary[value]=data_calculation(rows)
  return summary

def gaussian_probability(x,mean,std):
  e=exp(-((x-mean)**2/(2*std**2)))
  d=(1/(sqrt(2*pi)*std))
  ans=d*e
  return ans

def class_probability(summaries,newrow):  
  #getting total rows of the records for calculating probability of class
  #classvalues=names of classes in integer
  #classsummaries= summary of statistics for each class
  totalrows=sum([summaries[label][0][2] for label in summaries])
  total_probability=dict()
  for class_value,class_summaries in summaries.items():
    total_probability[class_value]=summaries[class_value][0][2]/float(totalrows)
    for i in range(len(class_summaries)):
      mean,stdev,_=class_summaries[i]
      total_probability[class_value]*=gaussian_probability(newrow[i],mean,stdev)
  return total_probability
 
def findclass(summaries, row):
  probabilities = class_probability(summaries, row)
  
  best_label=None
  best_prob=-1

  for class_value, probability in probabilities.items():
  #finding class with highest probability  
    if best_label is None or probability > best_prob:
      best_prob = probability
      best_label = class_value
     
  return best_label

filename='mydataset.csv'
#reading file
dataset=load_file(filename)

#converting string column values to floating values
for i in range (1,len(dataset[0])-1):#till columns length
  column_str_to_float(dataset,i)

#converting class column to int Value
department=dict()
classes=column_str_to_int(dataset, len(dataset[0])-1)
department=str_to_int(dataset,0)
#fitting Model
summary=class_calculation(dataset)

row=['sales',31,35,66,70]
s=row[0]
for x in department:
  if x==s:
    row[0]=department[x]

# predict the label
predicted_status = findclass(summary, row)
print("RESULTS:")
for y in classes:
  if classes[y]==predicted_status:
    myclass=y

print('Data=%s, Predicted: %s' % (row, myclass))

