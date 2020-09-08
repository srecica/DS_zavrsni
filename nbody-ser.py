import math
import numpy as np

number_of_steps = 1000000
time_step = 1000


def calculate_acceleration(bodies, body_index):
    g_const = 6.67408e-11  # m3 kg-1 s-2
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

for i in range(number_of_steps):
    for j in range(len(bodies)):
        acceleration = calculate_acceleration(bodies, j)

        bodies[j]['velocity'][0] += acceleration[0] * time_step
        bodies[j]['velocity'][1] += acceleration[1] * time_step
        bodies[j]['velocity'][2] += acceleration[2] * time_step

        bodies[j]['location'][0] += bodies[j]['velocity'][0] * time_step
        bodies[j]['location'][1] += bodies[j]['velocity'][1] * time_step
        bodies[j]['location'][2] += bodies[j]['velocity'][2] * time_step

for body in bodies:
    print(body['name'], body['location'])