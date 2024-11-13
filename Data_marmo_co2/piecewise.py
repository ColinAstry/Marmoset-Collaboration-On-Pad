#JS447第1次辨别
from openpyxl  import load_workbook
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
import os
import pandas as pd
import matplotlib.pyplot as plt
# Load your data into a pandas DataFrame
file_path = r'D:\Research\MarmoCo2\Data\ToProcess_Exp\analysis\xlsExp1_20241011.xlsx'
df = pd.read_excel(file_path)

# Filter rows where 'button' is either 'correct' or 'wrong'
df = df[df['button'].isin(['correct', 'wrong'])]

# Calculate the number of correct buttons and total buttons
df['correct_count'] = df['button'].eq('correct').cumsum()
df['total_count'] = df['button'].isin(['correct', 'wrong']).cumsum()

# Assign these counts to x and y
points = df[['correct_count', 'total_count']].values
X = points[:, 1]
y = points[:, 0]

# correct = 0
# cumu_correct = []
# choice_list_l = []
# choice_list_t = []
# list_l = []
# list_t = []
# list_lW = []
# list_tW = []
# day_split=[]
# for filename in [r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Raw3\7\505.772.xlsx',r'D:\Xu_Haoxin\Research\Gradu_thesis\Data\Raw3\7\505.772.xlsx']:
#     wb = load_workbook(filename)
#     ws = wb.active

#     stage = []
#     button = []
#     positionLeft = []
#     positionTop = []
#     positionLeftW = []
#     positionTopW = []
#     time = []
#     location_x = []
#     location_y = []
#     finger = []
#     for line in ws:
#         stage.append(line[0].value)
#         button.append(line[1].value)
#         positionLeft.append(line[2].value)
#         positionTop.append(line[3].value)
#         positionLeftW.append(line[4].value)
#         positionTopW.append(line[5].value)
#         time.append(line[6].value)
#         location_x.append(line[7].value)
#         location_y.append(line[8].value)
#         finger.append(line[9].value)
#     print(float(time[-1])/60000)

#     for i in range(1,len(stage)-1):
#         if button[i] == 'correct':
#             correct += 1
#             cumu_correct.append(correct)
#             choice_list_l.append(positionLeft[i])
#             choice_list_t.append(positionTop[i])
#             list_l.append(positionLeft[i])
#             list_t.append(positionTop[i])
#             list_lW.append(positionLeftW[i])
#             list_tW.append(positionTopW[i])
#         elif button[i] == 'wrong':
#             cumu_correct.append(correct)
#             choice_list_l.append(positionLeftW[i])
#             choice_list_t.append(positionTopW[i])
#             list_l.append(positionLeft[i])
#             list_t.append(positionTop[i])
#             list_lW.append(positionLeftW[i])
#             list_tW.append(positionTopW[i])
#     day_split.append(len(cumu_correct))
# X = np.arange(0,len(cumu_correct))
# y = np.array(cumu_correct)
ymax = np.max(y)
xmax = np.max(X)
plt.plot(X,y)

#分段函数线性拟合
#两段
def piecewise(x,x0,k1):
    return np.piecewise(x,[x<x0,x>=x0],[lambda x: k1*x, lambda x: (ymax-k1*x0)/(xmax-x0)*(x-x0)+k1*x0])
param_bounds = ([0,0],[xmax,1])
p,e = optimize.curve_fit(piecewise,X,y,bounds=param_bounds)
#plt.plot(X,piecewise(X,*p))

#三段
def piecewise_3(x,x0,x1,k1,k2):
    return np.piecewise(x,[x<x0,(x>=x0) & (x<x1+x0),x>=x1+x0],[lambda x: k1*x, lambda x: k2*(x-x0)+k1*x0, lambda x: (ymax-k1*x0-k2*x1)/(xmax-x1-x0)*(x-x1-x0)+(k1*x0+k2*x1)])
param_bounds = ([0,10,0,0],[xmax,xmax,1,1])
p2,e2 = optimize.curve_fit(piecewise_3,X,y,bounds=param_bounds)

#四段
def piecewise_4(x,x0,x1,x2,k1,k2,k3):
    return np.piecewise(x,[x<x0,(x>=x0) & (x<x1+x0),(x>=x0+x1) & (x<x1+x0+x2),x>=x1+x0+x2],[lambda x: k1*x, lambda x: k2*(x-x0)+k1*x0, lambda x: k3*(x-x0-x1)+k1*x0+k2*x1,lambda x: (ymax-k1*x0-k2*x1-k3*x2)/(xmax-x2-x1-x0)*(x-x2-x1-x0)+(k1*x0+k2*x1+k3*x2)])
param_bounds = ([0,20,50,0,0,0],[xmax-2,xmax-1,xmax,1,1,1])
#print("param_bounds:", param_bounds)
p3,e3 = optimize.curve_fit(piecewise_4,X,y,bounds=param_bounds)
#plt.plot(X,piecewise_4(X,*p3))
piecewise_1 = X*(ymax/xmax)

# # Open the file in write mode
# with open('output.txt', 'w') as f:
#     # Convert the output of piecewise_3 to a list and write it to the file
#     f.write(str(list(piecewise_3(X, *p2))))

# # Open the file in write mode
# with open('X_values.txt', 'w') as f:
#     # Convert X to a list and write it to the file
#     f.write(str(list(X)))

#画图
print(int(p2[0]))
plt.plot(X, y, color='blue', linewidth=2, label='real')
plt.plot(X[0:int(p2[0])],piecewise_3(X[0:int(p2[0])],*p2),linestyle='--', color='yellow', label='stage1')
plt.plot(X[int(p2[0]):int(p2[0])+int(p2[1])],piecewise_3(X[int(p2[0]):int(p2[0])+int(p2[1])],*p2),linestyle='--', color='orange', label='stage2')
plt.plot(X[int(p2[0])+int(p2[1]):xmax],piecewise_3(X[int(p2[0])+int(p2[1]):xmax],*p2),linestyle='--', color='red', label='stage3')
plt.legend()
plt.xlabel('total trial')
plt.ylabel('correct trial')

# Find the indices where the "File Name" changes
file_changes = df['Date'].ne(df['Date'].shift())
# Add vertical dashed lines at the points where the "File Name" changes
x_coords = df.loc[file_changes, 'total_count']
for x in x_coords:
    plt.axvline(x=x, color='gray', linestyle='--')

#save the plot
# Get the directory of the Excel file
dir_path = os.path.dirname(file_path)
# Get the filename of the Excel file without extension
file_name = os.path.splitext(os.path.basename(file_path))[0]
# Construct the filename for the plot
plot_filename = f"{file_name}_piecewise.png"
# Construct the full path for the plot
plot_path = os.path.join(dir_path, plot_filename)
# Save the plot
plt.savefig(plot_path)

plt.show()


#计算MSE并画图
MSE = []

mse = np.mean((y-piecewise_1)**2)
MSE.append(mse)

#print(p,xmax-p[0],(ymax-p[1]*p[0])/(xmax-p[0]))
mse = np.mean((y - piecewise(X,*p)) ** 2)
MSE.append(mse)

print('3piecefit:',p2,xmax-p2[0]-p2[1],(ymax-p2[2]*p2[0]-p2[3]*p2[1])/(xmax-p2[1]-p2[0]))
mse = np.mean((y - piecewise_3(X,*p2)) ** 2)
print('3pieceMSE:',mse)
MSE.append(mse)

mse = np.mean((y - piecewise_4(X,*p3)) ** 2)
MSE.append(mse)
plt.plot([1,2,3,4],MSE)
plt.scatter([1,2,3,4],MSE)
plt.ylim([0,20])
plt.xlabel('number of pieces')
plt.ylabel('MSE')
#save the plot
# Construct the filename for the plot
plot_filename2 = f"{file_name}_piece.png"
# Construct the full path for the plot
plot_path2 = os.path.join(dir_path, plot_filename2)
# Save the plot
plt.savefig(plot_path2)

plt.show()


# #计算空间偏好
# Stages = [0,int(p2[0]),int(p2[0]+p2[1]),xmax]
# for I in range(len(Stages)-1):
#     hit_matrix=np.zeros([3,3])
#     npLeft = 0
#     for pLeft in [0,0.33,0.66]:
#         npTop = 0
#         for pTop in [0,0.33,0.66]:
#             for i in range(Stages[I],Stages[I+1]):
#                 if choice_list_l[i] == pLeft and choice_list_t[i] == pTop:
#                     hit_matrix[npTop,npLeft] += 1
#             npTop += 1
#         npLeft += 1
#     hit_rate_matrix = hit_matrix/np.sum(hit_matrix)
#     entropy = -np.sum(hit_rate_matrix*(np.log2(hit_rate_matrix)))
#     print('entropy = %.4f'%entropy)
#     simu_hit_matrix=np.zeros([1000,3,3])
#     Top = [0,0.33,0.66]
#     Left = [0,0.33,0.66]
#     correct_rate=(cumu_correct[Stages[I+1]]-cumu_correct[Stages[I]])/(Stages[I+1]-Stages[I])
#     for i in range(Stages[I],Stages[I+1]):
#         rand_choice = np.random.random((1000))
#         for ii in range(1000):
#             if rand_choice[ii] <= correct_rate:
#                 simu_hit_matrix[ii,Top.index(list_t[i]),Left.index(list_l[i])] += 1/np.sum(hit_matrix)
#             else:
#                 simu_hit_matrix[ii,Top.index(list_tW[i]),Left.index(list_lW[i])] += 1/np.sum(hit_matrix)
#     for i in range(3):
#         for j in range(3):
#             if hit_matrix[i,j] == 0:
#                 hit_matrix[i,j] += 1e-5
#             for ii in range(1000):
#                 if simu_hit_matrix[ii,i,j] == 0:
#                     simu_hit_matrix[ii,i,j] += 1e-5
#     simu_entropy = np.zeros([1000])
#     for ii in range(1000):
#         simu_entropy[ii] = -np.sum(simu_hit_matrix[ii,:,:]*(np.log2(simu_hit_matrix[ii,:,:])))
#     print([np.percentile(simu_entropy,5),np.percentile(simu_entropy,95)])
#     print([np.percentile(simu_entropy,1),np.percentile(simu_entropy,99)])
#     per = 0
#     for p in range(1000):
#         if entropy < np.percentile(simu_entropy,p/10):
#             per = p/10
#             break
#     print(per)
#     plt.imshow(hit_rate_matrix,cmap='RdBu_r',vmin=0,vmax=0.22)
#     plt.colorbar()
#     plt.show()