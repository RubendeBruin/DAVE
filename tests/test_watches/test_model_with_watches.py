from DAVE import *

def test_watches():

    s = Scene()
    s.new_point('Point')
    s['Point'].watches['new watch 1'] = Watch(evaluate = 'self.name',
          condition = '',
          decimals = 2)


    s['Point'].watches['elevation'] = Watch(evaluate = 'self.gz',
          condition = '',
          decimals = 2)

    s['Point'].watches['elevation above 1'] = Watch(evaluate = 'self.gz',
          condition = 'value > 1',
          decimals = 2)


    R = s['Point'].run_watches()

    print(R)

    assert R == ([('new watch 1', 'Point'), ('elevation', 0.0)], [('elevation above 1', 0.0)])