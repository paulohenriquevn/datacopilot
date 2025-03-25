from core.copilot import DataCopilot

# Inicializar o copiloto com um dataset CSV
dcop = DataCopilot("data/train.csv")

# Etapa 1: Perfilamento inicial dos dados
dcop.profile()

# Etapa 2: Execução dos agentes de limpeza automática
dcop.run_agents()

# Etapa 3: Visualização dos dados ausentes e outliers
dcop.visualize("missing")
dcop.visualize("outliers")

# Etapa 4: Comando interativo (placeholder para LLM)
dcop.ask("Remova colunas com mais de 30% de valores ausentes")

# Etapa 5: Geração de relatório com os resultados
dcop.generate_report("output/report.html")