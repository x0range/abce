# Copyright 2012 Davoud Taghawi-Nejad
#
# Module Author: Davoud Taghawi-Nejad
#
# ABCE is open-source software. If you are using ABCE for your research you are
# requested the quote the use of this software.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License and quotation of the
# author. You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
from __future__ import division
from builtins import str
from builtins import object
from collections import defaultdict
from random import shuffle

class Quotation(object):
    def __init__(self, msg):
        self.__dict__ = msg

    def __get__(self):
        return self.__dict__

    def __str__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return str(self.__dict__)


class Quote(object):
    """ Quotes as opposed to trades are uncommitted offers. They can be made
    even if they agent can not fullfill them. With
    :meth:`~abceagent.Trade.accept_quote` and :meth:`~abceagent.Trade.accept_quote_partial`,
    the receiver of a quote can transform them into a trade.
    """
    def get_quotes(self, good, descending=False):
        """ self.get_quotes() returns all new quotes and removes them. The order
        is randomized.

        Args:
            good:
                the good which should be retrieved
            descending(bool,default=False):
                False for descending True for ascending by price

        Returns:
         list of quotes ordered by price

        Example::

         quotes = self.get_quotes()
        """
        ret = []
        for offer_id in list(self._quotes.keys()):
            if self._quotes[offer_id]['good'] == good:
                ret.append(self._quotes[offer_id])
                del self._quotes[offer_id]
        ret.sort(key=lambda objects: objects['price'], reverse=descending)
        return ret

    def get_quotes_all(self, descending=False):
        """ self.get_quotes_all() returns a dictionary with all now new quotes ordered
        by the good type and removes them. The order is randomized.

        Args:
            descending(bool,default=False):
                False for descending True for ascending by price

        Returns:
            dictionary of list of quotes ordered by price. The dictionary
            itself is ordered by price.

        Example::

            quotes = self.get_quotes()
        """
        ret = defaultdict(list)

        for quote in self._quotes:
            key = self._quotes[quote]['good']
            ret[key].append(self._quotes[quote])
        for key in list(ret.keys()):
            shuffle(ret[key])
            ret[key].sort(key=lambda objects: objects['price'],
                          reverse=descending)
        self._quotes = {}
        return ret

    def accept_quote(self, quote):
        """ makes a commited buy or sell out of the counterparties quote. For
        example, if you receive a buy quote you can accept it and a sell
        offer is send to the offering party.

        Args::
         quote: buy or sell quote that is accepted

        """
        if quote['buysell'] == 'qs':
            self.buy(quote['sender_group'], quote['sender_id'], quote['good'], quote['quantity'], quote['price'])
        else:
            self.sell(quote['sender_group'], quote['sender_id'], quote['good'], quote['quantity'], quote['price'])

    def accept_quote_partial(self, quote, quantity):
        """ makes a commited buy or sell out of the counterparties quote

        Args::
         quote: buy or sell quote that is accepted
         quantity: the quantity that is offered/requested
         it should be less than propsed in the quote, but this is not enforced.

        """
        if quote['buysell'] == 'qs':
            self.buy(quote['sender_group'], quote['sender_id'], quote['good'], quantity, quote['price'])
        else:
            self.sell(quote['sender_group'], quote['sender_id'], quote['good'], quantity, quote['price'])

    def quote_sell(self, receiver_group, receiver_id, good=None, quantity=None, price=None):
        """ quotes a price to sell quantity of 'good' to a receiver. Use None,
        if you do not want to specify a value.

        price (money) per unit
        offers a deal without checking or committing resources

        Args:
            receiver_group:
                agent group name of the agent
            receiver_id:
                the agent's id number
            'good':
                name of the good
            quantity:
                maximum units disposed to sell at this price
            price:
                price per unit
        """
        offer = Quotation({'sender_group': self.group,
                 'sender_id': self.id,
                 'receiver_group': receiver_group,
                 'receiver_id': receiver_id,
                 'good': good,
                 'quantity': quantity,
                 'price': price,
                 'buysell': 'qs',
                 'id': self._offer_counter()})
        self._send(receiver_group, receiver_id, '_q', offer)
        return offer

    def quote_buy(self, receiver_group, receiver_id, good=None, quantity=None, price=None):
        """ quotes a price to buy quantity of 'good' a receiver. Use None,
        if you do not want to specify a value.

        price (money) per unit
        offers a deal without checking or committing resources

        Args:
            receiver_group:
                agent group name of the agent
            receiver_id:
                the agent's id number
            'good':
                name of the good
            quantity:
                maximum units disposed to buy at this price
            price:
                price per unit
        """
        offer = Quotation({'sender_group': self.group,
                 'sender_id': self.id,
                 'receiver_group': receiver_group,
                 'receiver_id': receiver_id,
                 'good': good,
                 'quantity': quantity,
                 'price': price,
                 'buysell': 'qb',
                 'id': self._offer_counter()})
        self._send(receiver_group, receiver_id, '_q', offer)
        return offer
