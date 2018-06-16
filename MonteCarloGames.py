# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 12:58:23 2018

@author: Philipp
"""
import numpy as np
stepsize = 100

class Team:
    def __init__(self, posession=.5, hits=.1):
        self.posession = posession
        self.hits = hits # probability of scoring while having the ball

def normalize(array):
    array = np.array(array)
    array = array/np.linalg.norm(array)
    return array

def monte_carlo_run(team1, team2):
    #relposession1 = normalize([team1.posession, team2.posession])
    #relhits1 = normalize([team1.hits, team2.hits])
    ballwith = 0 # 0:team1; 1:team2
    goals = [0, 0]
    for i in range(0,90):
        #print('Simulating one minute of game')
        rand = np.random.random()
        chance = np.random.random()
        # chance to switch posession
        if chance < .5:
            if rand < team1.posession:
                ballwith = 0
        else: 
            if rand < team2.posession:
                ballwith = 1
        # chance to hit goal:
        rand = np.random.random()
        chance = np.random.random()
        if chance < .5:
            if rand < [team1.hits, team2.hits][ballwith]:
                goals[ballwith] += 1
    return goals
        
def simulate(nrOfRuns, team1, team2):
    """ 
    Simulate a monte carlo simulation with nrOfRuns number of steps
    returns: all results of runs; mean of all runs
    """
    results = []
    for i in range(nrOfRuns):
        [res1, res2] = monte_carlo_run(team1, team2)
        results.append([res1, res2])
        if not i % stepsize:
            print('Monte Carlo run: {}%; team1: {}, team2: {}'.format(i/nrOfRuns, res1, res2))
    results = np.array(results)
    mean = results.mean(axis=0)
    print('The prediction made by Monte-Carlo is {} - {}'.format(round(mean[0])\
          , round(mean[1])))
    return results, results.mean(axis=0), np.std(results, axis=0)

def odds(results):
    t1wins = results[results[:,0]>results[:,1]]
    odds1 = t1wins.shape[0]/results.shape[0]
    return odds1, 1-odds1
