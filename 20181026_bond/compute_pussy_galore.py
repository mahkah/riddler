
# File pussy_galore.py
# Author(s): Mahkah Wu
# Purpose: Explore possibile answers for the October 26th Riddler Express
# Bonus: https://www.youtube.com/watch?v=71zxjU-SC3Q

import pandas as pd
import numpy as np

# We'll be Pussy Galore ("pg"), our roomates will be Oddjob ("oj") and Goldfinger ("gf").
# We can pick any integer trap effectivness from 0 to 100, 0 being trivially non-optimal.
df_pg = pd.DataFrame(list(range(1,101)), columns=['pg_trap'])

# From our perspective, the values of Oddjob and Goldfinger are interchangeable, so
# we'll only consider order independent unique combinations of their trap values.
# This will decrease the number of trials we do by about half (5050 versus 10000
# roomate combinations) and will save us sorting the roomates' traps (gf<=oj).
dict = {'oj_trap': [], 'gf_trap': []}
for i in range(1,101):
    for j in range(1, i+1):
        dict['oj_trap'].append(i)
        dict['gf_trap'].append(j)

df_roomate = pd.DataFrame(data=dict)

# Cross join possible roomate traps with the set of our possible traps
df = df_pg.assign(foo=1).merge(df_roomate.assign(foo=1)).drop('foo', 1)


def trap_order(us, them):
    if us == them:
        return np.random.randint(0,2)
    elif us < them:
        return 1
    else:
        return 0

# Run n trials for each combination that we've come up with
n = 100
rows = 505000
pg_caps = [0] * rows

for i in range(rows):
    for j in range(n):
        # If we set a low success rate trap, we'll see if our trap would work,
        # then figure out whether we would have a shot at Bond only only if neccessary.
        if df['pg_trap'][i] > np.random.randint(0,100):
            # Our trap worked, would it be placed first?
            pg_first = trap_order(df['pg_trap'][i], df['gf_trap'][i])
            if pg_first == 1:
                pg_caps[i] += 1
            elif df['gf_trap'][i] <= np.random.randint(0,100):
                # Our trap worked, Goldfinger's didn't. Would our trap be second?
                pg_second = trap_order(df['pg_trap'][i], df['oj_trap'][i])
                if pg_second == 1:
                    pg_caps[i] += 1
                elif df['oj_trap'][i] <= np.random.randint(0,100):
                    # Our trap is third, but the other two have failed
                    pg_caps[i] += 1
    print("Row {}; {}/{}/{}".format(i, df['pg_trap'][i], df['gf_trap'][i], df['oj_trap'][i]))

df['pg_caps'] = pg_caps
df.to_csv("pussy_galore.csv")
