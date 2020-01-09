#!/usr/bin/env python

from itertools import permutations
from collections import Counter
import sys

"""
Ignores MARRS1 rungroup generation, which is odd because of the other big-bore group.  Easy enough to
add again here, though, if there's interest.
"""

default_rungroups = {
    'wings': {'cf', 'f5', 'fa', 'fb', 'fc', 'fe', 'fe2', 'ff', 'fm', 'fs', 'fst', 'fv', 'p1', 'p2'},
    'sm': {'sm'},
    'it': {'itb', 'itc', 'its', 'bspec'},
    'ssm': {'ssm'},
    'srf': {'srf', 'srf3'},
    'bigbore': {'ita', 'itr', 'sm5', 't3', 't4', 'as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'stu',
                'gtx', 'it7'},
    'smallbore': {'ep', 'fp', 'gtl', 'gtp', 'hp', 'lc', 'spu', 'stl', 'srx7'},
    'bracket': {'srf3', 'ita', 'ssm', 'stl', 'stu', 'itb', 'sm', 'srf', 'srx7'}
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


# noinspection PyUnusedLocal
def default_permutation_selector(permutation):
    return True


def marrs1_permutation_selector(permutation):
    good_bigbore_positions = {2}
    return any(permutation[position - 1] == 'bigbore'
               for position in good_bigbore_positions)


def marrs5_permutation_selector(permutation):
    good_bracket_positions = {2, 4, 6}
    good_wings_position = {8}
    return (any(permutation[position - 1] == 'bracket'
                for position in good_bracket_positions)
            and any(permutation[position - 1] == 'wings' for position in good_wings_position)
            and permutation[-1] == 'enduro')


raw_double_dippers = {
    ('sm', 'stl'): 35,
    ('stl', 'bracket'): 17,
    ('fp', 'bracket'): 1,
    ('srf3', 'bracket'): 16,
    ('sm', 'ssm'): 10,
    ('ssm', 'bracket'): 8,
    ('stu', 'bracket'): 3,
    ('ite', 'bracket'): 3,
    ('gt1', 'bracket'): 2,
    ('ssm', 'ita'): 7,
    ('fp', 'ita'): 1,
    ('ep', 'it7'): 1,
    ('ita', 'stl'): 1,
    ('t3', 'ep'): 1,
    ('gtp', 'bspec'): 2,
    ('itb', 'hp'): 1,
    ('sm', 'bracket'): 2,
    ('sm', 'srf3'): 1,
    ('ssm', 'fp'): 1,
    ('ssm', 'its'): 1,
    ('itb', 'bracket'): 1,
    ('sm', 'its'): 1,
}


def compute_choices(rungroups, permutation_selector=default_permutation_selector):
    double_dippers = Counter()
    double_dippers.update(dict(
        ((findclass(class1, rungroups), findclass(class2, rungroups)), count) for ((class1, class2), count) in
        raw_double_dippers.items()))
    double_dippers.update(dict(
        ((findclass(class2, rungroups), findclass(class1, rungroups)), count) for ((class1, class2), count) in
        raw_double_dippers.items()))

    permutations_and_scores = []
    for permutation in list(permutations(rungroups)):
        if not permutation_selector(permutation):
            continue
        pairs = [(permutation[i], permutation[i + 1]) for i in range(0, len(permutation) - 1)]
        pairs += [(permutation[-1], permutation[0])]
        overlap = [pair for pair in pairs if pair in double_dippers]
        score = sum(double_dippers.get(pair, 0) for pair in overlap)
        permutations_and_scores += [(permutation, score, overlap)]
        if len(overlap) == 0:
            print 'satisifies?', permutation, 'overlap', overlap

    min_score = min(score for permutation, score, overlap in permutations_and_scores)
    return [(permutation, score, overlap) for permutation, score, overlap in permutations_and_scores if
            score == min_score]


def print_results(rungroups, good_permutations):
    print 'rungroups:'
    print '\t', '\n\t'.join('rungroup "{name}": {members}'.format(name=name, members=', '.join(sorted(classes)))
                            for name, classes in rungroups.items())

    print '\n'.join('rungroup order: %s\n\t# back-to-back double-dippers: %d\n\tgroups with back-to-back double-dippers: %s' % (
        ', '.join('{pos}: {grp}'.format(pos=pos+1, grp=grp) for pos, grp in enumerate(permutation)), score,
        ', '.join('{btob1}+{btob2}'.format(btob1=sorted((x, y))[0], btob2=sorted((x, y))[1])
            for x, y in sorted(overlap))) for permutation, score, overlap in good_permutations)


default_marrs = compute_choices(default_rungroups)
print "### MARRS default rungroup choices (%d):" % len(default_marrs)
print_results(default_rungroups, default_marrs)
