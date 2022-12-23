import re
from enum import Enum
from copy import deepcopy

debug_filename = "debug.txt"
input_filename = "input.txt"

DEBUG = 33
TIME = 24

class Resources(Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'

class State:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.robots = {
            Resources.ORE: 1,
            Resources.CLAY: 0,
            Resources.OBSIDIAN: 0,
            Resources.GEODE: 0
        }
        self.resources = {r:0 for r in Resources}
        self.time = TIME

        self.saturation = {r:0 for r in Resources}
        self.isUseful = {r:True for r in Resources}
    
    def canBuild(self, robot: Resources):
        if robot not in self.blueprint.keys():
            raise Exception('Robot {} not in blueprint {}'.format(robot, self.blueprint))

        recipe = self.blueprint[robot]
        
        return sum([recipe[r]<=self.resources[r] for r in recipe.keys()])
    
    def build(self, robot: Resources):
        if not self.canBuild(robot):
            raise Exception("Not enough resouces for {}\nI need {} but I have {}".format(robot, self.blueprint[robot], self.resources))

        new = deepcopy(self)
        recipe = self.blueprint[robot]

        for r in recipe.keys():
            new.resources[r] -= recipe[r]
        
        new.robots[robot] += 1

        if robot!=Resources.GEODE:
            self.isUseful[robot] = sum([self.blueprint[x][robot]>=self.robots[robot] for x in Resources if self.isUseful[x] and robot in self.blueprint[x].keys()])!=0

        return new
    
    def step(self, time=1):
        if self.time-time<0:
            raise Exception("Trying to step after timeout")
        
        new = deepcopy(self)

        for robot in new.robots.keys():
            new.resources[robot] += new.robots[robot]*time
        new.time -=time
        
        return new

    def getDistances(self):
        if self.distanceTo(Resources.GEODE) == 0:
            return {Resources.GEODE: 0}

        result = {}
        for kk,r in self.blueprint.items():
            if self.isUseful[kk] and sum([self.robots[res]>0 for res in r.keys()]) == len(r.keys()):
                dst = self.distanceTo(kk)
                if dst < self.time:
                    result[kk] = dst
        
        return result
        
    def isTimeout(self):
        return self.time<=0

    def __eq__(self, other):
        return self.blueprint==other.blueprint and self.resources==other.resources and self.robots==other.robots and self.time==other.time

    def maxProduction(self):
        additional_robots = {kk:0 for kk in Resources}
        potential_materials = deepcopy(self.resources)
        for _ in range(self.time):
            for robot in self.blueprint:
                potential_materials[robot] += self.robots[robot] + additional_robots[robot]
            for robot, costs in self.blueprint.items():
                if all(
                    potential_materials[material] >= cost * (additional_robots[robot] + 1)
                    for material, cost in costs.items()
                ):
                    additional_robots[robot] += 1
        return potential_materials[Resources.GEODE]

    def distanceTo(self, resource):
        recipe = self.blueprint[resource]
        if sum([self.resources[r]>=recipe[r] for r in recipe])==len(recipe):
            return 0
        for r in recipe:
            if self.robots[r] == 0:
                return 10e7

        return max([(recipe[r]-self.resources[r])//self.robots[r] + min(1, (recipe[r]-self.resources[r])%self.robots[r]) for r in recipe])            

def readInput(f):
    blueprints = []

    for line in f:
        line = line.strip()
        blueprint = {}
        _, body = line.split(': ')
        robots = body.split('. ')
        for robot in robots:
            matches = re.match(r'Each (\w+) robot costs (.+)$', robot)
            robotType = matches.group(1)
            robotType = Resources[robotType.upper()]
            blueprint[robotType] = {}
            resources = matches.group(2)
            resources = re.findall(r'(\d+) (\w+)', resources)
            for r in resources:
                blueprint[robotType][Resources[r[1].upper()]] = int(r[0])
        blueprints.append(blueprint)
    return blueprints

def quelityLevel(state: State, idx):
    idx = idx+1
    res = 0
    timeStats = [0]*(TIME+1)

    queue = [state]

    while len(queue)>0:
        current = queue.pop()
        timeStats[current.time]+=1
        if current.isTimeout():
            if current.resources[Resources.GEODE] > res:
                res = current.resources[Resources.GEODE]
                print("New best res for blueprint {}: {}".format(idx, res))
        else:
            nextSteps = current.getDistances()
            for resource, distance in nextSteps.items():
                ns = current.step(distance+1).build(resource)
                if  ns.maxProduction()>res:
                    queue.append(ns)

    print("Blueprint {} solved with {} geodes".format(idx, res))
    print(timeStats)

    return res*idx

def solve(model):
    return sum([quelityLevel(State(model[i]), i) for i in range(len(model))])


if __name__=='__main__':
    with open(debug_filename, 'r') as f:
        model = readInput(f)
    res = solve(model)

    if res == DEBUG:
        print("Debug test passed, running on probelm input...")
    else:
        print("Debug test failed.\nExpected output: {}\nActual output: {}".format(DEBUG, res))
        exit(-1)
    
    with open(input_filename, 'r') as f:
        model = readInput(f)
    print(solve(model))

