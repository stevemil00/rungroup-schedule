# rungroup-schedule
Create rungroup schedules for the DC Region SCCA.

The idea here is to figure out, based on double-dipper numbers from last year, the minimum number of back-to-back
double-dippers possible for all possible rungroup orders.

Then, once we figure that out, we say which possible rungroup orders would produce that minimum number of back-to-back
double-dippers, so we have the minimum number of people who have to drive from the checker straight back to the grid.

## Requirements
Running this requires python, and that's about it.

## How To Run

```
./rungroup-schedule-2020.py
```

## Interpreting The Results
The results will look something like:

```
### MARRS default rungroup choices (48):
rungroups:
        rungroup "ssm": ssm
        rungroup "bracket": ita, itb, sm, srf, srf3, srx7, ssm, stl, stu
        rungroup "srf": srf, srf3
        rungroup "sm": sm
        rungroup "smallbore": ep, fp, gtl, gtp, hp, lc, spu, srx7, stl
        rungroup "bigbore": as, gt1, gt2, gt3, gta, gtx, it7, ita, ite, itr, sm5, spo, stu, t1, t2, t3, t4
        rungroup "wings": cf, f5, fa, fb, fc, fe, fe2, ff, fm, fs, fst, fv, p1, p2
        rungroup "it": bspec, itb, itc, its
rungroup order: 1: ssm, 2: srf, 3: smallbore, 4: bracket, 5: wings, 6: sm, 7: bigbore, 8: it
        # back-to-back double-dippers: 2
        groups with back-to-back double-dippers: it+ssm, bracket+smallbore
rungroup order: 1: ssm, 2: srf, 3: smallbore, 4: bracket, 5: it, 6: bigbore, 7: sm, 8: wings
        # back-to-back double-dippers: 2
        groups with back-to-back double-dippers: bracket+it, bracket+smallbore
rungroup order: 1: ssm, 2: srf, 3: it, 4: bigbore, 5: sm, 6: wings, 7: bracket, 8: smallbore
        # back-to-back double-dippers: 2
        groups with back-to-back double-dippers: bracket+smallbore, smallbore+ssm
```
(etc.)

The first part says how many different rungroup orders produce the same minimum number of back-to-back double-dippers.

The next part, under `rungroups`, is the list of rungroups, and the classes in that rungroup.

The rest of the output is a list of possible rungroup orders, giving all the possible orders that result
in the minimum possible back-to-back double-dippers.

For each possible rungroup order, we give:
   * the proposed rungroup order itself
   * the number of back-to-back double-dippers we'd have if we use that order
   * the groups that have back-to-back double-dippers

## How The Code Works
At a high level, what we're doing here is:

   * defining rungroups and the classes in those rungroups
   * detailing how many cars double-dipped between two classes

In an ideal world, we'd just define this outside of the code somehow, but this is not that world.

### Defining Rungroups
You define rungroups as a map from a rungroup name to a set of all the classes in that rungroup.

The names for the rungroups or for the classes don't matter, but you need to be consistent: you couldn't call
something `sm` in one place and `spec-miata` in another, because then the code won't be able to find the info
it needs.

For example:

```
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
```

defines eight rungroups, plus their members.

You can have more than one rungroup definition in here, too, of course.  Let's say you had a special format for
one particular race weekend (e.g., you need to throw in an enduro, or you have out-of-region classes that you
need to slot into our existing rungroups).  You can just define that in here, separately.  For example:

```
marrs1_rungroups = {
    'wings': {'cf', 'f5', 'fa', 'fb', 'fc', 'fe', 'fe2', 'ff', 'fm', 'fs', 'fst', 'fv', 'p1', 'p2'},
    'sm': {'sm'},
    'it': {'itb', 'itc', 'its', 'bspec'},
    'ssm': {'ssm'},
    'srf': {'srf', 'srf3'},
    'bigbore': {'as', 'gta', 'gt1', 'gt2', 'gt3', 'ite', 'spo', 't1', 't2', 'gtx'},
    'itaplus': {'ita', 'itr', 'sm5', 't3', 't4', 'stu'},
    'smallbore': {'ep', 'fp', 'gtl', 'gtp', 'hp', 'lc', 'spu', 'stl', 'srx7'},
    'bracket': {'srf3', 'ita', 'ssm', 'stl', 'stu', 'itb', 'sm', 'srf', 'srx7'}
}
```

### Defining Double-Dipper Counts
You define double-dipper counts for each pair of classes in which you had double dippers.  Note that you *don't*
add things in in both directions: that is, if you have `sm` and `stl` double-dippers, you don't want to say,
"10 sm double-dipped in stl" and "10 stl double-dipped in sm".  Just pick one, the code will figure out what
to do.

But you define that as:

```
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
```

where each pair of classes is expressed as a Python tuple, and that tuple is given the number of cars that double-dipped
between that pair of classes.

### Defining Rungroup Selectors
The code works by generating all possible combinations of rungroups, assigning each of those a score based on how
many double-dippers there are in back-to-back groups, figuring out the lowest count, then showing all the choices
that achieve that lowest count.

But sometimes, there are other constraints that you want to enforce.  For example, maybe you want to say that for
one event, Wings And Things is the last rungroup.

You can use a selector to toss any rungroup that doesn't meet your criteria, and the code will then pick the best
double-dipper choices with your criteria in mind.

The code will pass in a list of rungroups, and you can then pick and choose based on what you see.
For example, if we look at `default_rungroups` above, you might be passed a list like:

```
[
    'wings',
    'bracket',
    'bigbore',
    'smallbore',
    'sm',
    'it',
    'ssm',
    'srf'
]
```

and if you want to reject anything except choices that have `wings` last, you can do:

```
def wings_is_last_selector(permutation):
    return permutation[-1] == 'wings'
```

(that is, if the rungroup in the last spot in the array is named `wings`, that's an acceptable order for further
analysis, and if not, toss it and don't even bother doing the math on that combination).

### Tying It Together
In general, in `main()`, you'll have at least one section:

   * something that calls `compute_choices` with the right selector (or none, to use the default that says
     anything goes)
   * something that prints a header and the number of choices available
   * something that prints the results

So to continue our example, if we have a default rungroup order that we use for all but one event, and then our
one special-case order to force `wings` to be last, that might look like:

```
def main():
    default_marrs = compute_choices(default_rungroups)
    print "### MARRS default rungroup choices (%d):" % len(default_marrs)
    print_results(default_rungroups, default_marrs)

    wings_last_marrs = compute_choices(default_rungroups, wings_is_last_selector)
    print "### MARRS wings-as-last-group rungroup choices (%d):" % len(wings_last_marrs)
    print_results(default_rungroups, wings_last_marrs)
```
