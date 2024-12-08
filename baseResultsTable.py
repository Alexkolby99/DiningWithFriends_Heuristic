import os
import pandas as pd


def findBound(N, u, l, c_u, c_l,e):
    max_objective = None

    max_g_u = N // u  # Start with maximum feasible g_u

    for g_u in range(max_g_u, -1, -1):  # Iterate from max_g_u down to 0
        if (N - g_u * u) % l == 0:
            g_l = (N - g_u * u) // l
            if g_l >= 0:
                objective_value = c_u * g_u + c_l * g_l
                if max_objective is None or objective_value > max_objective:
                    max_objective = objective_value

    return min(max_objective*e,((size-1)*((size-1)+1))/2)


types = ['Meets_changing','Changing','Cycling']

intervals = [1900]
sizes = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

index = [(f'size_{size}',f'{int(interval/60)}min') for size in sizes for interval in intervals]

df = pd.DataFrame(index = index)

groupSize_getter = lambda x: (4,5) if not x in (17,18,19,20) else (4,4) if x == 20 else (3,4) 
e = 3

for size in sizes:
    u,l = groupSize_getter(size)
    bound = findBound(size,u,l,sum([i for i in range(u)]),sum([i for i in range(l)]),e)
    print(bound)

    pureSolveFile = os.path.join('results','3events','PureSolveSolutions',f'Tracking_size{size}.csv')
    _df = pd.read_csv(pureSolveFile)
    
    for interval in intervals:
        minutes = int(interval/60)
        if 1 - (_df.loc[_df['runTime']<interval,'Value'].max() / bound) == 0:
            df.loc[[(f'size_{size}',f'{minutes}min')],'Pure solve'] = _df.iloc[-2]['runTime']#1 - (_df.loc[_df['runTime']<interval,'Value'].max() / bound) 
        else:
            df.loc[[(f'size_{size}',f'{minutes}min')],'Pure solve'] = None
    for type in types:
        file = os.path.join('results','3events',type,f'Tracking_size{size}.csv')
        _df = pd.read_csv(file)
        for interval in intervals:
            minutes = int(interval/60)
            if 1 - (_df.loc[_df['runTime']<interval,'Value'].max() / bound) == 0:
                df.loc[[(f'size_{size}',f'{minutes}min')],type] = _df['runTime'].max()#1 - (_df.loc[_df['runTime']<interval,'Value'].max() / bound) 
            else:
                df.loc[[(f'size_{size}',f'{minutes}min')],type] = None

df.index = pd.MultiIndex.from_tuples(df.index)

df.index = [x[0] for x in df.index]

df = df.round(1)

print(df.to_latex())

