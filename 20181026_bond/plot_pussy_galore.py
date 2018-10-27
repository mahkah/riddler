import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("pussy_galore.csv")

# Let's look for the most effective trap effectivness given a random uniform
# distribution of roomates' trap effectivness
df_uniform = df.groupby(['pg_trap'])[['pg_caps']].sum()
df_uniform['pg_caps'] = df_uniform['pg_caps'] / df_uniform['pg_caps'].sum()

# Let's now consider that Riddler Nation distributes themselves around the optimal
# value given a random uniform distribution. For this purpose, a normal distribution
# feels too focused, so we'll use the Cauchy distribution instead.
df_normed = df[['pg_trap', 'gf_trap', 'oj_trap', 'pg_caps']]
x0 = df_uniform['pg_caps'].idxmax()
gamma = 15
pi = 3.14159265359

df_normed['gf_trap_cauchy'] = (1 / (pi * gamma)) * (gamma ** 2 / ((df_normed['gf_trap'] - x0) ** 2 + gamma ** 2))
df_normed['oj_trap_cauchy'] = (1 / (pi * gamma)) * (gamma ** 2 / ((df_normed['oj_trap'] - x0) ** 2 + gamma ** 2))
df_normed['scalar'] = df_normed['gf_trap_cauchy'] * df_normed['oj_trap_cauchy']
df_normed['pg_caps_scaled'] = df_normed['pg_caps'] * df_normed['scalar']

df_normed = df_normed.groupby(['pg_trap'])[['pg_caps_scaled']].sum()
df_normed['pg_caps_scaled'] = df_normed['pg_caps_scaled'] / df_normed['pg_caps_scaled'].sum()

guess = df_normed['pg_caps_scaled'].idxmax()

# Let's graph these
df_graph = df_uniform.join(df_normed)
df_graph.reset_index(inplace=True)
df_graph = pd.melt(df_graph, 'pg_trap', var_name="Roomates' Distribution")
df_graph["Roomates' Distribution"] = df_graph["Roomates' Distribution"].map({'pg_caps': 'Uniform', 'pg_caps_scaled': 'Cauchy'})
g = sns.lmplot('pg_trap', 'value', data=df_graph, fit_reg=False, hue="Roomates' Distribution")
ax = plt.gca()
ax.set_title('Bonds Captured by Trap Effectivness for Uniform and Cauchy Distributed Roomate Traps')
ax.set_ylabel('Bonds Captured (Normalized)')
ax.set_xlabel("Pussy Galore's Trap Effectivness")
g.savefig("scatter.png")
