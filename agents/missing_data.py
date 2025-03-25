# datacopilot/agents/missing_data.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class MissingDataAgent:
    def __init__(self, df: pd.DataFrame, threshold: float = 0.3):
        self.df = df
        self.threshold = threshold
        self.report = {}

    def analyze(self):
        missing_counts = self.df.isna().sum()
        missing_pct = missing_counts / len(self.df)
        self.report['missing_pct'] = missing_pct.to_dict()
        self.report['columns_to_drop'] = missing_pct[missing_pct > self.threshold].index.tolist()

    def suggest_strategies(self):
        suggestions = {}
        for col, pct in self.report['missing_pct'].items():
            if pct == 0:
                continue
            elif pct < 0.05:
                suggestions[col] = "Imputar com média ou mediana"
            elif pct < self.threshold:
                suggestions[col] = "Imputação contextual sugerida"
            else:
                suggestions[col] = "Considerar exclusão da coluna"
        self.report['suggestions'] = suggestions

    def visualize(self):
        sns.heatmap(self.df.isna(), cbar=False)
        plt.title("Mapa de Dados Ausentes")
        plt.show()

    def run(self):
        self.analyze()
        self.suggest_strategies()
        return self.report
