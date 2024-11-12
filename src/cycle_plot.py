from matplotlib import pyplot as plt
import pandas as pd

df = pd.read_csv('results/15PercentageK_initPureSolve_Cycling_1hour/HeuristicSolution_size26.csv',index_col=0)
df2 = pd.read_csv(f'results/15PercentageK_initPureSolve_meetsAtEinG_1hour/HeuristicSolution_size26.csv',index_col=0)
df3 = pd.read_csv(f'results/baseModelResults/SolverSolution_size26.csv',index_col=0)
df4 = pd.read_csv(f'results/baseModelResults/15PercentageK_initPureSolve_meetsAtEInG/HeuristicSolution_size26.csv',index_col=0)


plt.plot(df['runTime'],df['Value'], label='Cycle')
plt.plot(df2['runTime'],df2['Value'], label='2% Improvements')
plt.plot(df3['runTime'],df3['Value'], label='Pure Solve')
plt.plot(df4['runTime'],df4['Value'], label = '10min per branch')
plt.legend()
plt.show()