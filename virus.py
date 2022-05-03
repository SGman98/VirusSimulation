# Create a model that simulates a virus spreading and predict the number of
# cases for the next generation.

# Import libraries
import numpy as np
import matplotlib.pyplot as plt
from analisis import data_analisis
from analisis import data_analisis_graph


# Start
N = 500
INF_THRESHOLD = N/2
DEAD_THRESHOLD = N/4
PREV_MEASURE = True

INFECTED = 20
GRID_AREA = 100

# Parameters
INFECTION_RADIUS = 8
INFECTION_DURATION = 20
MASK_USE = 0.5
VACCINE_USE = 0.5

# Probabilities
INFECTION_PROBABILITY = 0.2
DEAD_PROBABILITY = 0.01
MASK_REDUCTION = 0.9
VACCINE_REDUCTION = 0.5


class individual:
    def __init__(self, state):
        self.x = np.random.rand() * GRID_AREA
        self.y = np.random.rand() * GRID_AREA
        self.mov_dir = np.random.rand() * 2 * np.pi
        self.state = state
        #  mask and vaccine randomly
        self.mask = False
        self.vaccine = False

    def move(self):
        next_x = self.x + np.cos(self.mov_dir)
        next_y = self.y + np.sin(self.mov_dir)
        # if the next position is in the grid
        if next_x >= 0 and next_x <= GRID_AREA and next_y >= 0 and next_y <= GRID_AREA:
            self.x = next_x
            self.y = next_y
        # else bouce off the wall
        # bounce right
        elif next_x >= GRID_AREA:
            self.x = GRID_AREA
            self.mov_dir = np.pi - self.mov_dir
        # bounce left
        elif next_x <= 0:
            self.x = 0
            self.mov_dir = np.pi - self.mov_dir
        # bounce bottom
        elif next_y >= GRID_AREA:
            self.y = GRID_AREA
            self.mov_dir = 2 * np.pi - self.mov_dir
        # bounce top
        elif next_y <= 0:
            self.y = 0
            self.mov_dir = 2 * np.pi - self.mov_dir
        else:
            pass

    # infect the individual
    def infect(self):
        # wearing mask reduces the probability of infection
        # check state only is healthy
        if self.state == 'healthy':
            if self.mask:
                # try probability of infection
                if np.random.rand() < INFECTION_PROBABILITY * (1-MASK_REDUCTION):
                    self.state = 'infected'
                    self.infection_time = 0
                    # print('infected')
            else:
                # try probability of infection
                if np.random.rand() < INFECTION_PROBABILITY:
                    self.state = 'infected'
                    self.infection_time = 0
                    # print('infected')
        else:
            pass
            # print('not infected')

    # spread the infection
    def spread(self, population):
        # if infected try to infect others
        if self.state == 'infected':
            # get all individuals in the infection radius around the infected individual in the population
            for i in population:
                if i.state == 'healthy':
                    # check if the individual is in the infection radius
                    if np.sqrt((i.x - self.x)**2 + (i.y - self.y)**2) < INFECTION_RADIUS:
                        # if this individual is using the mask reduce the probability of infection
                        if self.mask:
                            if np.random.rand() < INFECTION_PROBABILITY * (1-MASK_REDUCTION):
                                i.infect()
                                # print('spread')
                        else:
                            if np.random.rand() < INFECTION_PROBABILITY:
                                i.infect()
                                # print('spread')
                    else:
                        pass
                        # print('not in radius')
        else:
            pass
            # print('not infected')

    # update the state of the individual
    def update(self, population):
        # move the individual
        self.move()
        # if infected update the infection time and spread the infection
        if self.state == 'infected':
            self.infection_time += 1
            if self.infection_time >= INFECTION_DURATION:
                self.state = 'healthy'
                self.infection_time = 0
            else:
                # try to infect others
                self.spread(population)

                # try to die
                # reduction if vaccine
                if self.vaccine:
                    if np.random.rand() < DEAD_PROBABILITY * (1-VACCINE_REDUCTION):
                        self.state = 'dead'
                        self.dead_time = 0
                        # print('dead')
                else:
                    if np.random.rand() < DEAD_PROBABILITY:
                        self.state = 'dead'
                        self.dead_time = 0
                        # print('dead')

        # if dead update the dead time
        elif self.state == 'dead':
            self.dead_time += 1
            if self.dead_time >= INFECTION_DURATION:
                return 'dead'
                # print('destroyed')
        else:
            pass
            # print('not infected')

    # draw the individual
    def draw(self):
        # if infected draw the infected individual
        if self.state == 'infected':
            plt.plot(self.x, self.y, 'ro')
        # if healthy draw the healthy individual
        elif self.state == 'healthy':
            plt.plot(self.x, self.y, 'bo')
        # if dead draw the dead individual
        elif self.state == 'dead':
            plt.plot(self.x, self.y, 'ko')
        else:
            pass


class population:
    def __init__(self, N, INFECTED):
        self.population = []
        self.statistics = {
            'infected': [],
            'dead': [],
            'infected_masked': [],
            'dead_vaccinated': [],
        }
        self.gen_statistics = {
            'infected': 0,
            'dead': 0,
            'infected_masked': 0,
            'dead_vaccinated': 0,
        }
        self.total_per_day_statistics = {
            'infected': [],
            'dead': [],
            'healthy': [],
        }

        # create the population
        for i in range(N):
            # create a random individual
            self.population.append(individual('healthy'))
        # infect the first INFECTED individuals
        for i in range(INFECTED):
            self.population[i].state = 'infected'
            self.population[i].infection_time = 0

        self.mask_measure = False
        self.vaccine_measure = False

    def update(self):
        # update the state of the population
        for i in range(N):
            individual = self.population[i]
            individual.update(self.population)
            state = individual.state
            if state == 'infected':
                if individual.infection_time == 1:
                    self.gen_statistics['infected'] += 1
                    if individual.mask:
                        self.gen_statistics['infected_masked'] += 1
            elif state == 'dead':
                if individual.dead_time == 0:
                    self.gen_statistics['dead'] += 1
                    if individual.vaccine:
                        self.gen_statistics['dead_vaccinated'] += 1
                elif individual.dead_time >= INFECTION_DURATION:
                    # remove the individual from the population
                    # self.population.pop(i)
                    individual.state = 'destroyed'
            else:
                pass

        self.statistics['infected'].append(self.gen_statistics['infected'])
        self.statistics['dead'].append(self.gen_statistics['dead'])
        self.statistics['infected_masked'].append(self.gen_statistics['infected_masked'])
        self.statistics['dead_vaccinated'].append(self.gen_statistics['dead_vaccinated'])
        per_day_infected = self.get_infected()
        per_day_dead = self.get_dead()
        self.total_per_day_statistics['infected'].append(per_day_infected)
        self.total_per_day_statistics['dead'].append(per_day_dead)
        self.total_per_day_statistics['healthy'].append(N - per_day_infected - per_day_dead)

        # Preventive measures
        if PREV_MEASURE and self.gen_statistics['infected'] > INF_THRESHOLD and not self.mask_measure:
            self.mask_measure = True
            for i in range(N):
                individual = self.population[i]
                # use choice
                individual.mask = np.random.choice([True, False], p=[MASK_USE, 1-MASK_USE])
            print(f'mask prevention measure started at gen {GEN}')

        if PREV_MEASURE and self.gen_statistics['dead'] > DEAD_THRESHOLD and not self.vaccine_measure:
            self.vaccine_measure = True
            for i in range(N):
                individual = self.population[i]
                individual.vaccine = np.random.choice([True, False], p=[VACCINE_USE, 1-VACCINE_USE])
            print(f'vaccine prevention measure started at gen {GEN}')

    def get_infected(self):
        # get the number of infected individuals
        infected = 0
        for i in range(N):
            if self.population[i].state == 'infected':
                infected += 1
        return infected

    def get_dead(self):
        # get the number of dead individuals
        dead = 0
        for i in range(N):
            if self.population[i].state == 'dead' or self.population[i].state == 'destroyed':
                dead += 1

        return dead

    def draw(self):
        # draw the population
        for i in range(N):
            self.population[i].draw()


def export_data():
    # export data to csv
    with open('data.csv', 'w') as f:
        # write array of infected separated by comma
        f.write(','.join(str(x) for x in pop.total_per_day_statistics['infected']))
        f.write('\n')
        # write array of dead separated by comma
        f.write(','.join(str(x) for x in pop.total_per_day_statistics['dead']))
        f.write('\n')


# Give Resume
print('Starting simulation...')
print(f'Population size: {N}')
print(f'Starting infected: {INFECTED}')

print('Using' if PREV_MEASURE else 'No', 'preventive measures')

# Create the population
pop = population(N, INFECTED)
# possibility for 6 subplots
fig, ax = plt.subplots(3, 2)
# Loop 10 generations animation plot is 10x10 grid
# Generation by generation use matplotlib animation
plt.ion()
if plt.waitforbuttonpress():
    pass
# When user presses a key, stop the animation
GEN = 0
while True:
    GEN += 1

    plt.clf()
    # update the population
    pop.update()
    # draw the population first subplot
    plt.subplot(3, 2, 1)
    plt.title(f'Generation: {GEN}')
    # Restrict plot area to 10x10
    plt.xlim(0, GRID_AREA)
    plt.ylim(0, GRID_AREA)
    pop.draw()
    # Subplot total population stack healthy infected and dead
    plt.subplot(3, 2, 2)
    plt.title('Total population')
    plt.stackplot(range(len(pop.total_per_day_statistics['healthy'])),
                  pop.total_per_day_statistics['infected'],
                  pop.total_per_day_statistics['healthy'],
                  pop.total_per_day_statistics['dead'],
                  colors=['red', 'blue', 'black'])
    plt.legend(['Infected', 'Healthy', 'Dead'])

    # subplot for mask vs no mask 3rd subplot
    plt.subplot(3, 2, 3)
    plt.title('Infections: ' + str(pop.gen_statistics['infected']))
    # plot as stacked ploto
    no_mask = np.array(pop.statistics['infected']) - np.array(pop.statistics['infected_masked'])
    plt.stackplot(range(len(pop.statistics['infected'])),
                  pop.statistics['infected_masked'],
                  no_mask, labels=['masked: ' + str(pop.gen_statistics['infected_masked']),
                                   'no mask: ' + str(no_mask[-1])])
    plt.legend()
    # subplot for vaccine vs no vaccine
    plt.subplot(3, 2, 4)
    plt.title('Deads: ' + str(pop.gen_statistics['dead']))
    # no vaccine is dead - vaccine
    no_vaccine = np.array(pop.statistics['dead']) - np.array(pop.statistics['dead_vaccinated'])
    plt.stackplot(range(len(pop.statistics['dead'])),
                  pop.statistics['dead_vaccinated'],
                  no_vaccine, labels=['vaccine: ' + str(pop.gen_statistics['dead_vaccinated']),
                                      'no vaccine: ' + str(no_vaccine[-1])])

    plt.legend()

    # Plot infected per generation
    plt.subplot(3, 2, 5)
    plt.title('Infected per generation')
    infected_per_gen = [j - i for i, j in zip(pop.statistics['infected'], pop.statistics['infected'][1:])]
    plt.plot(infected_per_gen, label='infected')

    # Plot dead per generation
    plt.subplot(3, 2, 6)
    plt.title('Dead per generation')
    dead_per_gen = [j - i for i, j in zip(pop.statistics['dead'], pop.statistics['dead'][1:])]
    plt.plot(dead_per_gen, label='dead')

    plt.show()
    plt.pause(0.0001)

    if pop.total_per_day_statistics['infected'][-1] == 0:
        break

    # if GEN % 50 == 0:
    #     # calculate infection, dead and healthy rates using SIR
    #     # infection rate
    #     infected_rate = pop.total_per_day_statistics['infected'][-1] / N
    #     # dead rate
    #     dead_rate = pop.total_per_day_statistics['dead'][-1] / N
    #     # healthy rate
    #     healthy_rate = 1 - infected_rate - dead_rate
    #     # print the rates
    #     print('Rates:')
    #     print(f'\tinfected rate: {infected_rate}')
    #     print(f'\tdead rate: {dead_rate}')
    #     print(f'\thealthy rate: {healthy_rate}')
    #     print()

    if GEN == 200:
        export_data()
        data_analisis(250)
    elif GEN == 250:
        # print data infected in gen 250
        print(f'Infected in gen 250: {pop.total_per_day_statistics["infected"][-1]}')
        # print data dead in gen 250
        print(f'Dead in gen 250: {pop.total_per_day_statistics["dead"][-1]}')


# # Calculate masck effectiveness
# mask_effectiveness = pop.gen_statistics['infected_masked'] / pop.gen_statistics['infected']
# print(f'Mask effectiveness: {mask_effectiveness}')

# # Calculate vaccine effectiveness
# vaccine_effectiveness = pop.gen_statistics['dead_vaccinated'] / pop.gen_statistics['dead']
# print(f'Vaccine effectiveness: {vaccine_effectiveness}')

# analise data
export_data()
data_analisis_graph()

# Pause until user presses a key
plt.pause(0)
plt.close()
