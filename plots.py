import matplotlib.pyplot as plt
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



def plotDescent(paths,N,u,l,c_u,c_l,e):
    bound = findBound(N,u,l,c_u,c_l,e)
    fig = plt.figure()
    for path in paths:
        df = pd.read_csv(path)
        plt.scatter(df['runTime'],1 - df['Value']/bound)

    plt.ylim(-0.05,1.05)
    plt.xlim(-20,3620)
    plt.hlines(0,-20,3620,linestyles='dashed',colors='black')
    plt.xlabel('Time in seconds')
    plt.ylabel('Optimality Gap %')
    fig.savefig(f'results/figures/baseModel_{N}')

u = 5
l = 4
e = 6
for size in [16,21,22,23,24,25,26,27,28]:
    paths = [f'results/properResults/PureSolveSolutions/Tracking_size{size}.csv',
        f'results/properResults/15PercentageK_Meets/Tracking_size{size}.csv',
         f'results/properResults/15PercentageK_MeetsAtE/Tracking_size{size}.csv',
         f'results/properResults/15PercentageK_MeetsAtEInG/Tracking_size{size}.csv']
    plotDescent(paths,size,u,l,sum([i for i in range(u)]),sum([i for i in range(l)]),e)