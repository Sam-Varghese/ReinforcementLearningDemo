from turtle import *
import random
import turtle
import numpy as np
import math

title("Moon Lander")

def createSurface():

    """Function to create the surface of the moon. This surface for sure will contain only 1 part which is not inclined."""

    bgcolor("black")
    pencolor("white")
    

    flat_surface_color = "green"
    flat_surface_width = 5
    path_details = []

    possible_y_coordinates = [i*5 for i in range(20)]
    steps = [i*100 for i in range(-6, 7)]
    landing_point = random.sample(steps, random.choice([i for i in range(2,10)]))
    # print("Landing point is {}".format(landing_point))

    up()
    goto(-700, 0)
    path_details.append([-700, 0])
    down()

    y_coordinate = random.choice(possible_y_coordinates)
    for i in range(-650, 700, 50):

        if(i in landing_point):
            # print("HIGHLIGHTING SIR...")
            pencolor(flat_surface_color)
            turtle.width(flat_surface_width)
            goto(i, y_coordinate)
            path_details.append([i, y_coordinate])
            pencolor("white")
            turtle.width(1)
            y_coordinate = random.choice(possible_y_coordinates)

        else:

            goto(i, y_coordinate)
            path_details.append([i, y_coordinate])
            if (i+50 not in landing_point ):
                y_coordinate = random.choice(possible_y_coordinates)

    goto(700, 0)
    path_details.append([700, 0])
    return path_details

path_details = createSurface()

def startJourney(landingX, landingY, path_details):


    y_paths = [i[1] for i in path_details]
    x_paths = [i[0] for i in path_details]

    point1 = [-700, 0]
    goto(-700, 0)
    speed(1)
    pencolor("gold")
    turtle.shape("triangle")
    turtle.fillcolor("gold")
    left(90)
    input("Press enter to start the rover...")
    
    x_subset=y_subset = []

    x_subset = [i for i in x_paths if i <= landingX]
    y_subset = [i for i in y_paths[0: x_paths.index(landingX)]]

    # print("X paths = ", x_paths)
    # print("X subset  = ", x_subset)

    point2 = [x_subset[y_subset.index(max(y_subset))], max(y_subset)]
    point3 = [landingX, landingY]

    # print("Point1  = ", point1)
    # print("Point2  = ", point2)
    # print("Point3  = ", point3)

    ys = np.array([point1[1], point2[1], point3[1]])
    xs = np.array([[i**2, i, 1] for i in [point1[0], point2[0], point3[0]]])
    # print("xs = ", xs)
    # print("path = ", path_details)
    # print("Inverse = ", np.linalg.inv(xs))

    [a,b,c] = np.dot(np.linalg.inv(xs), ys)

    for i in range(x_subset[0], x_subset[-1]+10, 10):

        # print("Going to ", [i, a*(i**2)+b*i+c])
        goto(i, a*(i**2)+b*i+c)

    goto(x_subset[-1]+25, a*(x_subset[-1]**2)+b*x_subset[-1]+c)

def RLearning1():

    discountFactor = 2
    rewards = 0
    rewards_list = []
    landingSites = []
    counter = 0

    for i in range(len(path_details)-1):

        rewards += (path_details[i][0]/50)*(discountFactor**(counter))

        if(path_details[i][1] == path_details[i+1][1]):

            # startJourney(path_details[i][0], path_details[i][1], path_details)
            rewards_list.append(rewards)
            landingSites.append([path_details[i][0], path_details[i][1]])
            # break

        counter += 1

    max_reward = max(rewards_list)
    max_reward_site_index = rewards_list.index(max_reward)
    max_reward_path = landingSites[max_reward_site_index]

    print("Computed max reward path details")

    startJourney(max_reward_path[0], max_reward_path[1], path_details)

RLearning1()

done()