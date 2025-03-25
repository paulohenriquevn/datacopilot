# datacopilot/core/copilot.py

import pandas as pd
from agents.missing_data import MissingDataAgent
from agents.outliers import OutlierDetectionAgent
from agents.inconsistencies import InconsistencyAgent
from reports.report_generator import ReportGenerator

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
        print(f"\n💬 Instrução recebida: '{instruction}'")
        instruction = instruction.lower()

        if "remova colunas com mais de" in instruction and "% de nas" in instruction:
            try:
                import re
                match = re.search(r"(\d+)% de nas", instruction)
                if match:
                    threshold = int(match.group(1)) / 100
                    missing_pct = self.df.isna().sum() / len(self.df)
                    cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
                    self.df.drop(columns=cols_to_drop, inplace=True)
                    print(f"🧹 Colunas removidas por excesso de NAs (> {threshold*100}%): {cols_to_drop}")
            except Exception as e:
                print(f"⚠️ Erro ao interpretar comando: {e}")

        elif "padronize formato de telefone" in instruction:
            import re
            if 'phone' in self.df.columns:
                self.df['phone'] = self.df['phone'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
                print("📞 Telefones padronizados: apenas dígitos mantidos")
            else:
                print("📞 Coluna 'phone' não encontrada no dataset")

        elif "mostre boxplot da coluna" in instruction:
            import re
            match = re.search(r"boxplot da coluna ([\w_]+)", instruction)
            if match:
                col = match.group(1)
                if col in self.df.columns:
                    agent = OutlierDetectionAgent(self.df)
                    agent.visualize_boxplot(col)
                else:
                    print(f"📊 Coluna '{col}' não encontrada no dataset")

        else:
            print("❓ Instrução não reconhecida. Tente comandos como:\n - Remova colunas com mais de 30% de NAs\n - Padronize formato de telefone\n - Mostre boxplot da coluna preco")

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
        generator = ReportGenerator()
        generator.generate(self.reports, output_path)
