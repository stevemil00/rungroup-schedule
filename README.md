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
FIXME write this!

