'''
Epidemic simulation
Qijian Liu
'''

import numpy as np
import matplotlib.pyplot as plt
# import time
# import pandas as pd


# Setup constants
N = 100
rate = 0.5 # rate of infection for adult
death_rate = 0.016 # rate of death
seeds = np.arange(1, 11)

# setup function
def det_infection(i, j, infected):
    '''
    Determines if the person in this tile will be infected

    '''
    p = np.random.random()
    
    # determine the infection rate for the individual based on their age group
    infect = rate
    if status[(i,j)][1] == 1:
        infect /=  2
    elif status[(i,j)][1] == 3:
        infect *= 1.5
    
    if p < infect:
        epidemic_map[i,j] = 2
        status[(i,j)][0] = 1
        infected += 1
        
    return infected

tot_days = []
tot_active = []
tot_infect = []
tot_death = []

for seed in seeds:
    np.random.seed(seed)
    
    # Generate a network of lattice
    network = np.ones((N,N), int)
    
    while np.sum(network)>int(0.65*(N*N)):
        i = np.random.randint(0, N)
        j = np.random.randint(0, N)
        
        if network[i, j] == 1:
            network[i, j] = 0
            
    # plt.figure(dpi=300)
    # plt.imshow(network)
    # #plt.savefig('seed = {} network.png'.format(seed))
    # plt.show()
    
    epidemic_map = np.copy(network)
    
    status = {} # status = {(i,j):[a, b, c]} where (i,j) is the position of the person, a is the infection status, and b is the agegroup, c is the days infected
    
    infected = 0
    
    # Put people into agegroups according to the distribution, and randomly select initial patients 
    for i in range(N):
        for j in range(N):
            if network[i,j] == 1:
                p = np.random.random()
                q = np.random.random()
                if 0.21 < p < 0.87:
                    # adults
                    network[i,j] = 2
                    if q > 0.01:
                        status[(i,j)] = [0, 2, 0] 
                    else:
                        status[(i,j)] = [1, 2, 0] 
                        epidemic_map[i, j] = 2
                        infected += 1
                elif p > 0.87:
                    # elderly
                    network[i, j] = 3
                    if q > 0.01:
                        status[(i,j)] = [0, 3, 0] 
                    else:
                        status[(i,j)] = [1, 3, 0] 
                        epidemic_map[i, j] = 2
                        infected += 1
                else:
                    # youth
                    if q > 0.01:
                        status[(i,j)] = [0, 1, 0] 
                    else:
                        status[(i,j)] = [1, 1, 0] 
                        epidemic_map[i, j] = 2
                        infected += 1
    
    # plt.figure(dpi=300)
    # plt.imshow(network)
    # #plt.savefig('seed = {} distribution of agegroups.png'.format(seed))
    # plt.show()
    
    # plt.figure(dpi=300)
    # plt.imshow(epidemic_map)
    # #plt.savefig('seed = {} epidemic map.png'.format(seed))
    # plt.show()
    
    # # infection simulation
    death_count = 0
    recovered = 0
    iterations = 0
    days = []
    n_deaths = []
    n_infect = []
    
    while 0 < infected: 
        for i in range(N):
            for j in range(N):
                if network[i, j] != 0: # check only open sites
                
                    # The current tile is a patient
                    if epidemic_map[i, j] == 2:
                        status[(i,j)][-1] += 1 # add 1 to the days infected
                        
                        if status[(i,j)][-1] == 14: # determine if the patient recovers or dies when days infected is 14
                            d = np.random.random()
                            if d < death_rate:
                                # the patient dies
                                status[(i,j)][0] = status[(i,j)][-1] = -1
                                death_count += 1
                                epidemic_map[i,j] = 0
                                network[i, j] = 0
                                
                            else:
                                status[(i,j)][0] = 0
                                status[(i,j)][-1] = 0 # Scenario 2: no immunity when recovered
                                # status[(i,j)][-1] = -1 # Scenario 1: immunity
                                epidemic_map[i,j] = 1
                                recovered += 1
                            infected -= 1
                    
                    # The current tile is not a patient
                    else:
                        if status[(i,j)][-1] == 0:
                            # the tile is not on the edges of the grid
                            if 0 < i < N-1 and 0 < j < N-1:
                                if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) \
                                    or (epidemic_map[i,j+1] == 2 and status[i,j+1][-1] > 0)\
                                        or (epidemic_map[i-1,j] == 2 and status[i-1,j][-1] > 0)\
                                            or (epidemic_map[i,j-1] == 2 and status[i,j-1][-1] > 0):
                                    infected = det_infection(i, j, infected)
                            
                            # the tile is on the edges of the grid
                            else:
                                if i == 0 and j == 0:
                                    if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) or (epidemic_map[i, j+1] == 2 and status[i,j+1][-1] > 0):
                                        infected = det_infection(i, j, infected)
                                elif i == 0 and j == N-1:
                                    if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) or (epidemic_map[i, j-1] == 2  and status[i,j-1][-1] > 0):
                                        infected = det_infection(i, j, infected)
                                elif i == N-1 and j == 0:
                                    if (epidemic_map[i, j+1] == 2 and status[i,j+1][-1] > 0) or (epidemic_map[i-1, j] == 2 and status[i-1,j][-1] > 0):
                                        infected = det_infection(i, j, infected)
                                elif i == N-1 and j == N-1:
                                    if (epidemic_map[i-1,j] == 2 and status[i-1,j][-1] > 0) or (epidemic_map[i, j-1] == 2 and status[i,j-1][-1] > 0):
                                        infected = det_infection(i, j, infected)
                                elif i == 0 and 0 < j < N-1:
                                    if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) \
                                        or (epidemic_map[i,j+1] == 2 and status[i,j+1][-1] > 0)\
                                            or (epidemic_map[i,j-1] == 2 and status[i,j-1][-1] > 0):
                                                infected = det_infection(i, j, infected)
                                elif i == N-1 and 0 < j < N-1:
                                    if (epidemic_map[i-1,j] == 2 and status[i-1,j][-1] > 0) \
                                        or (epidemic_map[i,j+1] == 2 and status[i,j+1][-1] > 0)\
                                            or (epidemic_map[i,j-1] == 2 and status[i,j-1][-1] > 0):
                                                infected = det_infection(i, j, infected)
                                elif 0 < i < N-1 and j == 0:
                                    if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) \
                                        or (epidemic_map[i,j+1] == 2 and status[i,j+1][-1] > 0)\
                                            or (epidemic_map[i-1,j] == 2 and status[i-1,j][-1] > 0):
                                        infected = det_infection(i, j, infected)
                                else:
                                    if (epidemic_map[i+1,j] == 2 and status[i+1,j][-1] > 0) \
                                        or (epidemic_map[i,j-1] == 2 and status[i,j-1][-1] > 0)\
                                            or (epidemic_map[i-1,j] == 2 and status[i-1,j][-1] > 0):
                                        infected = det_infection(i, j, infected)
                            
                            
        iterations += 1
        
        if iterations%5 == 0:
            # print('Infections: ', infected)
            # print('Deaths: ', death_count)
            days.append(iterations)
            n_deaths.append(death_count)
            n_infect.append(infected)
            # plt.figure(dpi=300)
            # plt.title('Day {}'.format(iterations))
            # plt.imshow(epidemic_map)
            # plt.show()

                                
                                    
    plt.figure(dpi=300)
    plt.imshow(epidemic_map)
    #plt.savefig('seed = {} final epidemic map.png'.format(seed))
    plt.show()
    
    print('Days: ', iterations)
    print('Active cases: ', infected)
    print('Deaths: ', death_count)
    print('Recoveries: ', recovered)
    
    tot_days.append(iterations)
    tot_active.append(infected)
    tot_death.append(death_count)
    tot_infect.append(recovered)
    
    plt.figure(dpi=300)
    plt.scatter(days, n_infect)
    plt.scatter(days, n_deaths)
    plt.xlabel('Days')
    plt.ylabel('Number of people')
    plt.legend(['Number of active cases', 'Number of Deaths'])
    #plt.savefig('seed = {} infections and deaths.png'.format(seed))
    plt.show()
    
# results = pd.DataFrame(
#     {
#      'total days': tot_days,
#      'total active': tot_active,
#      'total infections': tot_infect,
#      'total deaths': tot_death   
#      }
#     )
# results.to_csv('results.csv', mode='a', header=True)
        
