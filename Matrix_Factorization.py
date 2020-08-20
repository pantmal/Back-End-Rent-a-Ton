import numpy 
import numpy as np
import pandas as pd
import os
from django.db.models import Avg

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backendManager.settings")
import django
django.setup()

import django.db.models
from backendManager import settings
from django.conf import settings
from django.apps import apps
from users.models import *
from rooms.models import *

from operator import itemgetter

#alpha = learning rate
#beta = normalization factor
def Matrix_Factorization(R, P, Q, K, steps=3000, alpha=0.02, beta=0.02, gamma=0.05):
    #Q = Q.T
    print(range(len(R)))
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * ( eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * ( eij * P[i][k] - beta * Q[k][j])

        eR = numpy.dot(P,Q)
        e = 0
        #e_sum = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta) * (pow(P[i][k],2) + pow(Q[k][j],2))/2
                    #e_sum += e
        #print(e)
        if e < 0.001:
            print('yup')
            break
        # mp = numpy.matmul(P,Q)
        # e2 = numpy.sum((R-mp)**2)
    return P, Q, e


#Main

rooms = Room.objects.all()
users = CustomUser.objects.all()

# print(len(rooms))
users = users.filter(is_renter=True)

df = pd.DataFrame(list(Room.objects.all().values()))
df = df.sort_values(by=['id'])
id_list = df['id'].tolist()

us_df = pd.DataFrame(list(users.values()))
us_df = us_df.sort_values(by=['id'])
id_list_users = us_df['id'].tolist()

Real_Items = [['' for i in range(len(rooms))] for j in range(len(users))]


for num_i, user_id in enumerate(id_list_users):
    for num_j, room_id in enumerate(id_list):
        if RoomRating.objects.filter(room_id_rate=room_id, renter_id_rate=user_id).exists():
            avg = RoomRating.objects.filter(room_id_rate=room_id,renter_id_rate=user_id).aggregate(Avg('rating'))
            Real_Items[num_i][num_j] = avg['rating__avg']
        elif Reservation.objects.filter(room_id_res=room_id, renter_id_res=user_id).exists():
            Real_Items[num_i][num_j] = 3.0
        elif ClickedItem.objects.filter(room_id_click=room_id, renter_id_click=user_id).exists():
            Real_Items[num_i][num_j] = 3.0
        elif SearchedItem.objects.filter(room_id_search=room_id, renter_id_search=user_id).exists():
            Real_Items[num_i][num_j] = 3.0
        else:
            Real_Items[num_i][num_j] = 0.0
        
zeros = []
for i, user_id in enumerate(Real_Items):
    zero_list = []
    for j, room_id in enumerate(user_id):
        if Real_Items[i][j] == 0.0:
            zero_list.append((i,j))
    zeros.append(zero_list)        



R = numpy.array(Real_Items)
M = len(R)
N = len(R[0])
K = 10

P = numpy.random.rand(M,K)
Q = numpy.random.rand(K,N)

#print(P)
#print(Q)

nP, nQ, e = Matrix_Factorization(R, P, Q, K)
nR = numpy.dot(nP, nQ)

print(nR)
print(e)
# print(e2)
# print(es)

new_array = nR.tolist()

preds = []
for i, user_id in enumerate(new_array):
    pred_list = []
    for j, room_id in enumerate(user_id):
        if (i,j) in zeros[i]:
            pred_list.append((new_array[i][j],i,j))
    preds.append(pred_list)        

#print(preds)
#print('spave')
final_preds = []
for pred_list in preds:
    final_preds.append(sorted(pred_list, key=lambda x: float(x[0]),reverse=True))

print(final_preds)


for pred_list in final_preds:
    top = 0
    for x,y,z in pred_list:
        # print(id_list_users[y])
        # print(id_list[z])
        recommendation = RecommendedItem(room_id_rec=Room.objects.get(pk=id_list[z]), renter_id_rec=CustomUser.objects.get(pk=id_list_users[y]))
        recommendation.save()
        top += 1
        if top == 10:
            break
    