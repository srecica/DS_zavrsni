import math
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD #komunikator, metoda koja komunicira medu procesima
rank = comm.Get_rank() #vraca rank procesa u komunikator, svaki klon dobiva svoj rank od 0 do (n-1)
size = comm.Get_size() #vraca broj procesa u komunikator, 4

number_of_steps = 1000000  #postupak izračunavanja sljedećeg stanja sustava
time_step = 1000 #vremenski interval za koji će simulacija napredovati tijekom sljedećeg koraka

#racunanje akceleracije jednog tijela
def calculate_acceleration(bodies, body_index):
    g_const = 6.67408e-11  
    acceleration = [0, 0, 0]
    body = bodies[body_index]
    for index, external_body in enumerate(bodies):
        if index != body_index:
            r = (body['location'][0] - external_body['location'][0]) ** 2 + (
                        body['location'][1] - external_body['location'][1]) ** 2 + (
                            body['location'][2] - external_body['location'][2]) ** 2
            r = math.sqrt(r)
            tmp = g_const * external_body['mass'] / r ** 3
            acceleration[0] += tmp * (external_body['location'][0] - body['location'][0])
            acceleration[1] += tmp * (external_body['location'][1] - body['location'][1])
            acceleration[2] += tmp * (external_body['location'][2] - body['location'][2])

    return acceleration


## podaci o planetima (lokacija (m), masa (kg), brzina (m/s)
sun = {"location": [0, 0, 0], "mass": 2e30, "velocity": [0, 0, 0], 'name': 'sun'}
mercury = {"location": [0, 5.7e10, 0], "mass": 3.285e23, "velocity": [47000, 0, 0], 'name': 'mercury'}
venus = {"location": [0, 1.1e11, 0], "mass": 4.8e24, "velocity": [35000, 0, 0], 'name': 'venus'}
earth = {"location": [0, 1.5e11, 0], "mass": 6e24, "velocity": [30000, 0, 0], 'name': 'earth'}
mars = {"location": [0, 2.2e11, 0], "mass": 2.4e24, "velocity": [24000, 0, 0], 'name': 'mars'}
jupiter = {"location": [0, 7.7e11, 0], "mass": 1e28, "velocity": [13000, 0, 0], 'name': 'jupiter'}
saturn = {"location": [0, 1.4e12, 0], "mass": 5.7e26, "velocity": [9000, 0, 0], 'name': 'saturn'}
uranus = {"location": [0, 2.8e12, 0], "mass": 8.7e25, "velocity": [6835, 0, 0], 'name': 'uranus'}
neptune = {"location": [0, 4.5e12, 0], "mass": 1e26, "velocity": [5477, 0, 0], 'name': 'neptune'}
pluto = {"location": [0, 3.7e12, 0], "mass": 1.3e22, "velocity": [4748, 0, 0], 'name': 'pluto'}


bodies = [sun, earth, mars, venus]
bodies_indices = np.arange(0, len(bodies), dtype='int')
index = np.empty(1, dtype='int')
comm.Scatter(bodies_indices, index, root=0)
index = index[0]
body = bodies[index]

for i in range(number_of_steps):
    acceleration = calculate_acceleration(bodies, index)

#racunanje akceleracije nebeskih tijela u sve 3 dimenzije
    body['velocity'][0] += acceleration[0] * time_step
    body['velocity'][1] += acceleration[1] * time_step
    body['velocity'][2] += acceleration[2] * time_step

#lokacija tijela (na temelju prethodnog brzina*time stamp tj koliki je korak u vremenu)
    body['location'][0] += body['velocity'][0] * time_step
    body['location'][1] += body['velocity'][1] * time_step
    body['location'][2] += body['velocity'][2] * time_step

    for j in range(size):
        if j != rank:
            comm.send(body, dest=j, tag=rank) #metoda za slanje
            #body - objekt koji sadrzi podatke koje saljemo 
            #dest – rang procesa (njegov ID) kojem saljemo poruku
            #tag – oznaka vrste poruke


    for j in range(size):
        if j != rank:
            bodies[j] = comm.recv(source=j, tag=j) 
            #- source – proces (njegov ID) koji ãalje poruku
            #- tag – oznaka vrste poruke



comm.Barrier()

location = np.array([body['location'][0], body['location'][1], body['location'][2]], dtype='float64')
locations = np.empty((4, 3), dtype='float64')
#- datatype – tip podatka koji se salje/prima

comm.Gather(location, locations, root=0)

#ispis lokacije i ime tijela
if rank == 0:
    for i in range(len(locations)):
        print(bodies[i]['name'], locations[i])
        # print(bodies[int(location[3])]['name'], location)