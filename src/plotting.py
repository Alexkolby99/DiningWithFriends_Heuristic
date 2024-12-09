import matplotlib.pyplot as plt
import pandas as pd
import gurobipy as gp

def optimize_groups(N, u, l, c_u, c_l):
    max_objective = None
    best_solution = None

    max_g_u = N // u  # Start with maximum feasible g_u

    for g_u in range(max_g_u, -1, -1):  # Iterate from max_g_u down to 0
        if (N - g_u * u) % l == 0:
            g_l = (N - g_u * u) // l
            if g_l >= 0:
                objective_value = c_u * g_u + c_l * g_l
                if max_objective is None or objective_value > max_objective:
                    max_objective = objective_value
                    best_solution = (g_u, g_l)

    return best_solution, max_objective


table = pd.DataFrame(index=[('Heuristic','RunTime'),('Heuristic','ObjValue'),('Heuristic','OptimalityGap'),('Solver','RunTime'),('Solver','ObjValue'),('Solver','OptimalityGap')])
table.index = pd.MultiIndex.from_tuples(table.index)

colors = [
    "#1f77b4",  # Blue
    "#ff7f0e",  # Orange
    "#2ca02c",  # Green
    "#d62728",  # Red
    "#9467bd",  # Purple
    "#8c564b",  # Brown
    "#e377c2",  # Pink
    "#7f7f7f",  # Gray
    "#bcbd22",  # Yellow-green
    "#17becf"   # Cyan
]


fig, axes = plt.subplots(3, 5, figsize=(10, 10))  # Adjust figsize as needed
files = [16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
idx = 0



for i in range(3):
    for j in range(5):

        e = 6
        l = 4
        u = 5
        N = files[idx]

        solution,obj = optimize_groups(N,u,l,sum([i for i in range(u)]),sum([i for i in range(l)]))

        bound = min(obj*e,((files[idx]-1)*((files[idx]-1)+1))/2)
        


        df = pd.read_csv(f'results/mainResults/MeetsAtEInG_changing/Tracking_size{files[idx]}.csv',index_col=0)
        df2 = pd.read_csv(f'results/mainResults/PureSolveSolutions/Tracking_size{files[idx]}.csv',index_col=0)
        df3 = pd.read_csv(f'results/mainResults/MeetsAtE_changing/Tracking_size{files[idx]}.csv',index_col=0)
        df4 = pd.read_csv(f'results/mainResults/Meets_changing/Tracking_size{files[idx]}.csv',index_col=0)
        df5 = pd.read_csv(f'results/mainResults/Cycling/Tracking_size{files[idx]}.csv',index_col=0)
        df6 = pd.read_csv(f'results/mainResults/Changing/Tracking_size{files[idx]}.csv',index_col=0)

        df['OptimalityGap'] =  (bound- df['Value'])/bound
        df2['OptimalityGap'] = (bound - df2['Value'])/bound
        df3['OptimalityGap'] = (bound - df3['Value'])/bound
        df4['OptimalityGap'] = (bound - df4['Value'])/bound
        df5['OptimalityGap'] = (bound - df5['Value'])/bound
        df6['OptimalityGap'] = (bound - df6['Value'])/bound

        ax = axes[i, j]  # Get the specific subplot
        ax.plot(df2['runTime'],df2['OptimalityGap'],'o',label='PureSolve',alpha=1,markersize=5,color='black')
        ax.hlines(df2['OptimalityGap'].min(),-100,2000,color='black',linestyle = 'dashed',alpha = 0.7,label='Best pure solve solution')
        ax.plot(df['runTime'],df['OptimalityGap'],'o',label='MeetsAtEinG',alpha=0.5,markersize=3)
        ax.plot(df3['runTime'],df3['OptimalityGap'],'o',label='MeetsAtE',alpha=0.5,markersize=3)
        ax.plot(df4['runTime'],df4['OptimalityGap'],'o',label='Meets',alpha=0.5,markersize=3)
        ax.plot(df5['runTime'],df5['OptimalityGap'],'o',label='Cycling',alpha=0.5,markersize=3)
        ax.plot(df6['runTime'],df6['OptimalityGap'],'o',label='Changing',alpha=0.5,markersize=3)
        ax.set_title(f"problem of size {files[idx]}")
        ax.set_xlim(-50,1850)
        ax.set_ylim(0,1)
        ax.grid(True)
        ax.set_ylabel('')
        ax.set_xlabel('')
        if i == 1 and j == 0:
            ax.set_ylabel('OptimalityGap %')

        if i == 2 and j == 2:
            ax.set_xlabel('Time in seconds')

        if j % 5 != 0:
            ax.set_yticklabels([])

        if i != 2:
            ax.set_xticklabels([])

        # table.loc[('Bound'),f'size_{files[idx]}'] = bound
        # table.loc[('Heuristic','RunTime'),f'size_{files[idx]}'] = df['runTime'].max().item()
        # table.loc[('Heuristic','ObjValue'),f'size_{files[idx]}'] = df['Value'].max().item()
        # table.loc[('Heuristic','OptimalityGap'),f'size_{files[idx]}'] = df['OptimalityGap'].min().item()
        # # table.loc[('Fixed Heuristic','RunTime'),f'size_{files[idx]}'] = df3['runTime'].max().item()
        # # table.loc[('Fixed Heuristic','ObjValue'),f'size_{files[idx]}'] = df3['Value'].max().item()
        # # table.loc[('Fixed Heuristic','OptimalityGap'),f'size_{files[idx]}'] = df['OptimalityGap'].min().item()
        # table.loc[('Solver','RunTime'),f'size_{files[idx]}'] = df2['runTime'].max().item()
        # table.loc[('Solver','ObjValue'),f'size_{files[idx]}'] = df2['Value'].max().item()
        # table.loc[('Solver','OptimalityGap'),f'size_{files[idx]}'] = df2['OptimalityGap'].min().item()

        idx += 1

handles, labels = axes[0,0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0.92))

plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.show()


print(table.transpose())
