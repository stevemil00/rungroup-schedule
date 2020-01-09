#!/usr/bin/env python

from itertools import permutations
from collections import Counter
import sys

"""
MARRS 1: 9 groups
big-ita becomes 2 groups
    'bigbore': set(['as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'gtx']),
    'itaplus': set(['ita', 'itr', 'sm5', 't3', 't4', 'stu'])

MARRS 5: 9 groups
normal 8 groups + enduro
must end with enduro
wings must be just before
bracket should be 2, 4, 6
"""

default_rungroups = {
    'wings': set(['cf', 'f5', 'fa', 'fb', 'fc', 'fe', 'fe2', 'ff', 'fm', 'fs', 'fst', 'fv', 'p1', 'p2']),
    'sm': set(['sm']),
    'it': set(['itb', 'itc', 'its', 'bspec']),
    'ssm': set(['ssm']),
    'srf': set(['srf', 'srf3']),
    'big-ita': set(['ita', 'itr', 'sm5', 't3', 't4', 'as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'stu', 'gtx']),
    'smallbore': set(['ep', 'fp', 'gtl', 'gtp', 'hp', 'lc', 'spu', 'stl', 'srx7']),
    'bracket': set(['srf3', 'ita', 'ssm', 'stl', 'stu', 'itb', 'sm', 'srf', 'srx7'])
}

marrs1_rungroups = {
    'wings': set(['cf', 'f5', 'fa', 'fb', 'fc', 'fe', 'fe2', 'ff', 'fm', 'fs', 'fst', 'fv', 'p1', 'p2']),
    'sm': set(['sm']),
    'it': set(['itb', 'itc', 'its', 'bspec']),
    'ssm': set(['ssm']),
    'srf': set(['srf', 'srf3']),
    'bigbore': set(['as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'gtx']),
    'itaplus': set(['ita', 'itr', 'sm5', 't3', 't4', 'stu']),
    'smallbore': set(['ep', 'fp', 'gtl', 'gtp', 'hp', 'lc', 'spu', 'stl', 'srx7']),
    'bracket': set(['srf3', 'ita', 'ssm', 'stl', 'stu', 'itb', 'sm', 'srf', 'srx7'])
}

marrs5_rungroups = {
    'wings': set(['cf', 'f5', 'fa', 'fb', 'fc', 'fe', 'fe2', 'ff', 'fm', 'fs', 'fst', 'fv', 'p1', 'p2']),
    'sm': set(['sm']),
    'it': set(['itb', 'itc', 'its', 'bspec']),
    'ssm': set(['ssm']),
    'srf': set(['srf', 'srf3']),
    'big-ita': set(['ita', 'itr', 'sm5', 't3', 't4', 'as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'stu', 'gtx']),
    'smallbore': set(['ep', 'fp', 'gtl', 'gtp', 'hp', 'lc', 'spu', 'stl', 'srx7']),
    'bracket': set(['srf3', 'ita', 'ssm', 'stl', 'stu', 'itb', 'sm', 'srf', 'srx7']),
    # unknown overlap so it is what it is
    'enduro': set(['enduro'])
}

def findclass(car_class, rungroups):
    stuff = [group for group, car_classes in rungroups.items() if car_class in car_classes and group != 'bracket']
    if stuff:
        return stuff[0]
    elif car_class == 'bracket':
        return car_class
    else:
        print 'no group found for class', car_class
        sys.exit(1)

def default_permutation_selector(permutation):
    return True

def marrs1_permutation_selector(permutation):
    good_bigbore_positions = set([2])
    return any(permutation[position - 1] == 'bigbore'
      for position in good_bigbore_positions)

def marrs5_permutation_selector(permutation):
    good_bracket_positions = set([2, 4, 6])
    good_wings_position = set([8])
    return (any(permutation[position - 1] == 'bracket'
      for position in good_bracket_positions)
      and any(permutation[position - 1] == 'wings' for position in good_wings_position)
      and permutation[-1] == 'enduro')

raw_double_dippers = {
    ('sm', 'stl'): 20,
    ('ssm', 'ita'): 15,
    ('ssm', 'sm'): 10,
    ('its', 'stl'): 3,
    ('t3', 'stl'): 2,
    ('ssm', 'stl'): 2,
    ('sm', 'ita'): 1,
    ('srf3', 'bracket'): 11,
    ('ita', 'bracket'): 9,
    ('ssm', 'bracket'): 7,
    ('stl', 'bracket'): 6,
    ('stu', 'bracket'): 4,
    ('itb', 'bracket'): 2,
    ('sm', 'bracket'): 2,
    ('srf', 'bracket'): 2,
    ('srx7', 'bracket'): 1
}

def compute_choices(rungroups, permutation_selector=default_permutation_selector):
    double_dippers = Counter()
    double_dippers.update(dict(((findclass(class1, rungroups), findclass(class2, rungroups)), count) for ((class1, class2), count) in raw_double_dippers.items()))
    double_dippers.update(dict(((findclass(class2, rungroups), findclass(class1, rungroups)), count) for ((class1, class2), count) in raw_double_dippers.items()))

    permutations_and_scores = []
    for permutation in list(permutations(rungroups)):
        if not permutation_selector(permutation):
            continue
        pairs = [(permutation[i], permutation[i + 1]) for i in range(0, len(permutation) - 1)]
        pairs += [(permutation[-1], permutation[0])]
        overlap = [pair for pair in pairs if pair in double_dippers]
        score = sum(double_dippers.get(pair, 0) for pair in overlap)
        #print pairs, overlap, score
        permutations_and_scores += [(permutation, score, overlap)]
        if len(overlap) == 0:
    	    print 'satisifies?', permutation, 'overlap', overlap
    
    min_score = min(score for permutation, score, overlap in permutations_and_scores)
    return [(permutation, score, overlap) for permutation, score, overlap in permutations_and_scores if score == min_score]

def print_results(rungroups, good_permutations):
    print 'rungroups:'
    print '\t', '\n\t'.join('%s: %s' % (name, ', '.join(sorted(classes))) for name, classes in rungroups.items())
    print '\n'.join('order: %s; # double-dippers: %d; double-dipper groups: %s' % (', '.join('%d: %s' % (pos + 1, grp) for pos, grp in enumerate(permutation)), score, ', '.join('%s+%s' % (sorted((x, y))[0], sorted((x, y))[1]) for x, y in sorted(overlap))) for permutation, score, overlap in good_permutations)

marrs1 = compute_choices(marrs1_rungroups, marrs1_permutation_selector)
print "### MARRS 1 rungroup choices: (%d)" % len(marrs1)
print_results(marrs1_rungroups, marrs1)

marrs5 = compute_choices(marrs5_rungroups, marrs5_permutation_selector)
print "### MARRS 5 rungroup choices: (%d)" % len(marrs5)
print_results(marrs5_rungroups, marrs5)

default_marrs = compute_choices(default_rungroups)
print "### MARRS default rungroup choices (%d):" % len(default_marrs)
print_results(default_rungroups, default_marrs)
