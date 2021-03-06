from __future__ import division
from __future__ import print_function
import abce
from tools import *
import time


class LoggerTest(abce.Agent):
    def init(self, simulation_parameters, agent_parameters):
        self.last_round = simulation_parameters['rounds'] - 1
        self.create('money', 50)
        self.create('cookies', 3)

    def one(self):
        self.log('possessions', self.possessions())
        self.log_value('round_log', self.round)
        pass

    def two(self):
        pass

    def three(self):
        pass

    def clean_up(self):
        pass

    def all_tests_completed(self):
        if self.round == self.last_round:
            time.sleep(0.5)
            print('Check database whether logging succeeded')



