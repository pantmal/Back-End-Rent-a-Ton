import numpy 
import numpy as np
import pandas as pd
import os
import progressbar as pb
from django.db.models import Avg

#The following commands are necessary in order to use the Django models in this script.
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

#Defining the Matrix Factorization function.
#Steps are how many times the algorithm will re-run.
#Alpha is the learning rate and beta is the normalization factor
def Matrix_Factorization(R, P, Q, K, steps=1000, alpha=0.02, beta=0.02, gamma=0.05):
    #Q = Q.T
    #print(range(len(R)))

    #Executing the algorithm for 'steps' times.
    for step in pb.progressbar(range(steps)):
        for i in range(len(R)): #i in this case is the row number
            for j in range(len(R[i])): #j in this case is the column number
                if R[i][j] > 0: #For values in R that are not unknown
                    
                    #eij is the error variable that is calculated by taking the difference between value in the real matrix and the corresponding value in the predicted P*Q array.
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])

                    #Updating values in P and Q using K latent features.
                    #The idea for gradient descent formula used for the updating was inspired from the following link: http://proceedings.mlr.press/v36/li14.pdf
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * ( eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * ( eij * P[i][k] - beta * Q[k][j])

        #Now we create the updated predicted array with updated values of P and Q.
        eR = numpy.dot(P,Q)
        
        #Here we calculate the Mean Squared Error and save it in e, to evaluate the accuracy of the algorithm.
        #Ideas for the calculation of the Mean Squared Error used by: https://www.diva-portal.org/smash/get/diva2:927190/FULLTEXT01.pdf
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta) * (pow(P[i][k],2) + pow(Q[k][j],2))/2
        
        #Setting a boundary for e. We may want to stop the execution of the algorithm if it the value of e is good enough.
        if e < 0.001:
            break

    #Returning the final versions of P and Q and the Mean Squared Error.
    return P, Q, e


#Getting rooms and users
rooms = Room.objects.all()
users = CustomUser.objects.all()

#Only renters matter to us.
users = users.filter(is_renter=True)

#For this example we used the last 200 rooms.
df = pd.DataFrame(list(Room.objects.all().values()))
df = df.sort_values(by=['id'])
df = df.tail(200)
id_list = df['id'].tolist()
print(len(id_list))

#Getting the last 200 users too.
us_df = pd.DataFrame(list(users.values()))
us_df = us_df.sort_values(by=['id'])
us_df = us_df.tail(200)
id_list_users = us_df['id'].tolist()
print(len(id_list_users))

#Initializing an empty 'R' array.
Real_Items = [['' for i in range(len(id_list))] for j in range(len(id_list_users))]

#Setting values for the Real_Items array.
#If the user has rated a room we get the average of his ratings and add it in the array.
#If there are no ratings we check his Reservations, his Clicks, and his Searches (with this order).
#If he has performed any of the following we add a 3 because this is the 'middle' value for the ratings, so it is considered an average value. 
#If the user doesn't meet any of our criteria we add a 0, so the Matrix Factorization algorithm can make predictions for this room.
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

#Getting coordinates of all the items to be predicted.        
zeros = []
for i, user_id in enumerate(Real_Items):
    zero_list = []
    for j, room_id in enumerate(user_id):
        if Real_Items[i][j] == 0.0:
            zero_list.append((i,j))
    zeros.append(zero_list)        


#Getting rows(M) and columns(N) of the Real_Items array.
R = numpy.array(Real_Items)
M = len(R)
N = len(R[0])

#Setting latent features.
K = 2

# print(M)
# print(N)

#Initializing two random P and Q arrays using M, N and K.
P = numpy.random.rand(M,K)
Q = numpy.random.rand(K,N)

#print(P)
#print(Q)

#Executing the Matrix Factorization algorithm.
nP, nQ, e = Matrix_Factorization(R, P, Q, K)

#Getting the final predicted array.
nR = numpy.dot(nP, nQ)

print(nR)
#ADD A MESSAGE FOR e
print(e)

#Converting the predicted array from numpy to list format.
new_array = nR.tolist()

#Getting values that were predicted.
preds = []
for i, user_id in enumerate(new_array):
    pred_list = []
    for j, room_id in enumerate(user_id):
        if (i,j) in zeros[i]:
            pred_list.append((new_array[i][j],i,j))
    preds.append(pred_list)        

#Sorting the predictions.
final_preds = []
for pred_list in preds:
    final_preds.append(sorted(pred_list, key=lambda x: float(x[0]),reverse=True))

print(final_preds)

#Creating a recommendation for each prediction.
for pred_list in final_preds:
    top = 0
    for x,y,z in pred_list:
        # print(id_list_users[y])
        # print(id_list[z])

        #Room that was predicted.
        room = Room.objects.get(pk=id_list[z])
        host = room.host_id

        #User to make recommendations for.
        user = CustomUser.objects.get(pk=id_list_users[y])

        #If the user is a host in this room skip it.
        if user.id == host.id:
            top += 1
            continue

        #Don't create a recommendation if it already exists.
        case = Recommendation.objects.filter(room_id_rec=Room.objects.get(pk=id_list[z]), renter_id_rec=CustomUser.objects.get(pk=id_list_users[y])).exists()

        #Otherwise create one and stop if we reached our top number.
        if case == False:
            recommendation = Recommendation(room_id_rec=Room.objects.get(pk=id_list[z]), renter_id_rec=CustomUser.objects.get(pk=id_list_users[y]))
            recommendation.save()
            top += 1
            if top == 10:
                break
    