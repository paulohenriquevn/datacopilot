# datacopilot/core/copilot.py

import pandas as pd
from agents.missing_data import MissingDataAgent
from agents.outliers import OutlierDetectionAgent
from agents.inconsistencies import InconsistencyAgent

class DataCopilot:
    def __init__(self, source):
        self.source = source
        self.df = self._load_data()
        self.reports = {}

    def _load_data(self):
        if isinstance(self.source, pd.DataFrame):
            return self.source.copy()
        elif self.source.endswith('.csv'):
            return pd.read_csv(self.source)
        elif self.source.endswith('.parquet'):
            return pd.read_parquet(self.source)
        else:
            raise ValueError("Formato de dados não suportado")

    def profile(self):
        print("\n🔍 Perfilando os dados...")
        print(self.df.info())
        print("\nResumo estatístico:")
        print(self.df.describe(include='all'))

    def run_agents(self):
        print("\n🤖 Rodando agentes de análise de qualidade...")

        agent_missing = MissingDataAgent(self.df)
        self.reports['missing_data'] = agent_missing.run()

        agent_outliers = OutlierDetectionAgent(self.df)
        self.reports['outliers'] = agent_outliers.run()

        agent_inconsistency = InconsistencyAgent(self.df)
        self.reports['inconsistencies'] = agent_inconsistency.run()

        print("\n✅ Agentes executados com sucesso.")

    def ask(self, instruction):
        print(f"\n💬 Interpretação da instrução: '{instruction}'")
        # Placeholder para integração futura com LLM/chatbot
        print("(Funcionalidade de linguagem natural em desenvolvimento)")

    def visualize(self, target):
        print(f"\n📊 Gerando visualização: {target}")
        if target == "missing":
            agent = MissingDataAgent(self.df)
            agent.visualize()
        elif target == "outliers":
            agent = OutlierDetectionAgent(self.df)
            for col in self.df.select_dtypes(include='number').columns[:3]:
                agent.visualize_boxplot(col)
        else:
            print("Tipo de visualização não suportado")

    def generate_report(self, output_path):
        print(f"\n📝 Gerando relatório em: {output_path}")
        with open(output_path, 'w') as f:
            for key, report in self.reports.items():
                f.write(f"\n--- {key.upper()} ---\n")
                f.write(str(report))
