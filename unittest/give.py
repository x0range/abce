from __future__ import division
from __future__ import print_function
import abce
from tools import *
import random


class Give(abce.Agent):
    def init(self, simulation_parameters, agent_parameters):
        self.last_round = simulation_parameters['rounds'] - 1
        if self.id == 1:
            self.tests = {'all': False, 'topic': False}
        else:
            self.tests = {}

    def one(self):
        if self.id == 0:
            self.create('cookies', random.uniform(0, 10000))
            self.cookies = self.possession('cookies')
            quantity = random.uniform(0, self.possession('cookies'))
            self.give('give', 1, 'cookies', quantity)
            assert self.possession('cookies') == self.cookies - quantity
            self.message('give', 1, topic='tpc', content=quantity)

    def two(self):
        if self.id == 1:
            rnd = random.randint(0, 1)
            if rnd == 0:
                msg = self.get_messages_all()
                msg = msg['tpc']
                self.tests['all'] = True
                assert len(msg) == 1, len(msg)
            elif rnd == 1:
                msg = self.get_messages('tpc')
                self.tests['topic'] = True
                assert len(msg) == 1, len(msg)
            msg = msg[0]
            assert msg.content == self.possession('cookies')
            assert msg.sender_group == 'give'
            assert msg.sender_id == 0
            assert msg.topic == 'tpc'
            assert msg.receiver_id == 1
            assert msg.receiver_group == 'give'

    def three(self):
        pass

    def clean_up(self):
        self.destroy('cookies')

    def all_tests_completed(self):
        if self.round == self.last_round and self.id == 0:
            assert all(self.tests.values()), 'not all tests have been run; ABCE workes correctly, restart the unittesting to do all tests %s' % self.tests
            print('Test abce.give:\t\t\t\t\tOK')
            print('Test abce.message:\t\t\t\tOK')
            print('Test abce.get_messages:\t\t\t\tOK')
            print('Test abce.get_messages_all:\t\t\tOK')


