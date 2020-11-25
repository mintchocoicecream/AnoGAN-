import glob
import sys
import os

result_path = 'C:/Users/sxxhn/Desktop/finalproject/main/datasets/mnist_2_0.0/validation/anomaly/test_result'
result_output = glob.glob(f'{result_path}/*')
files=[]
#for p in result_output:
#    files.append(int(result_output[-18:-4]))
#print(result_output[0].replace('\\', '/'))
print(result_output[0][93:])
# a = ['\\']
# b = []
# for item in a:
#     b.append(item.replace('\\','/'))
# a = b
# print(a)


