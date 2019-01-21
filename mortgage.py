#!/usr/bin/env python
import math
from decimal import Decimal
from datetime import datetime, timedelta

class Mortage(object):

    def __init__(self,
                 total='600000',
                 rate='3.95',
                 years=30,
                 frequency=7,
                 start_date=None,):

        if start_date:
            self.start_date = datetime.strptime(start_date, '%Y%m%d').date()
        else:
            self.start_date = datetime.today()

        self.total = Decimal(str(total))
        self.rate = Decimal(str(rate)) / 100
        self.rate_daily = self.rate / 365
        self.years = int(years)
        # TODO: leap years
        self.days = self.years * 365

        self.frequency = frequency
        # TODO: floor or ceil?
        # total term count
        N = math.ceil(self.days / self.frequency)
        r = self.rate_daily * self.frequency
        q = 1 + r
        qN = Decimal(str(math.pow(q, N)))

        # A = T x q**N * (q - 1) / (q**N - 1)
        A = self.total * qN * r / (qN - 1)

        self.A = int(A)  # real num to pay
        total_paid = int(A * N)

        principal = self.total
        _date = self.start_date
        total_interest = Decimal('0.0')

        for i in range(1, N+1):
            interest = principal * r
            term_principal = self.A - int(interest)
            total_interest += interest
            _total = principal + interest
            principal = _total - self.A
            _date = _date + timedelta(days=self.frequency)
            print('%4d %s %6d(%s) %3d %3d(%s) %3d(%s)' % (
                i, _date.strftime('%Y-%m-%d'),
                int(principal),
                '{:.2%}'.format(principal/self.total),
                self.A,
                term_principal,
                '{:.1%}'.format(term_principal/self.A),
                int(interest),
                '{:.1%}'.format(interest/self.A),
            ))

        print('mortgage: T: {} R: {} Y: {}'.format(total, rate, years))
        print('F: {} N: {} A: {}'.format(frequency, N, self.A))
        print('TP: {} TI: {}'.format(total_paid, int(total_interest)))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Mortgage breakdown')
    parser.add_argument(
        '-T', '--total', type=int, default=700000,
        help='Total amount to borrow, default: %(default)s')
    parser.add_argument(
        '-Y', '--years', type=int, default=30,
        help='Years to pay, default: %(default)s')
    parser.add_argument(
        '-R', '--rate', type=str, default='3.99',
        help='Interest rate percent, default: %(default)s')
    parser.add_argument(
        '-F', '--frequency', type=int, default=7,
        help='Frequency of days to pay, default: %(default)s')

    args = parser.parse_args()
    m = Mortage(
        total=args.total,
        years=args.years,
        rate=args.rate,
        frequency=args.frequency,
    )
