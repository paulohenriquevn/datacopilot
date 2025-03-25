# datacopilot/agents/outliers.py

import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go

class OutlierDetectionAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.report = {}

    def detect_iqr(self):
        iqr_outliers = {}
        for col in self.df.select_dtypes(include=np.number).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            mask = (self.df[col] < lower) | (self.df[col] > upper)
            iqr_outliers[col] = {
                'method': 'IQR',
                'outliers': int(mask.sum()),
                'percent': round(100 * mask.sum() / len(self.df), 2),
                'lower_bound': lower,
                'upper_bound': upper
            }
        self.report['iqr'] = iqr_outliers

    def detect_zscore(self):
        zscore_outliers = {}
        numeric_df = self.df.select_dtypes(include=np.number)
        z_scores = np.abs(stats.zscore(numeric_df, nan_policy='omit'))
        for idx, col in enumerate(numeric_df.columns):
            outliers = (z_scores[:, idx] > 3).sum()
            zscore_outliers[col] = {
                'method': 'Z-Score',
                'outliers': int(outliers),
                'percent': round(100 * outliers / len(self.df), 2)
            }
        self.report['zscore'] = zscore_outliers

    def visualize_boxplot(self, col):
        fig = go.Figure()
        fig.add_trace(go.Box(y=self.df[col], name=col))
        fig.update_layout(title=f'Boxplot de {col}')
        fig.show()

    def run(self):
        self.detect_iqr()
        self.detect_zscore()
        return self.report
