import os
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    def __init__(self, template_dir="reports/templates"):
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, report_data: dict, output_path: str):
        template = self.env.get_template("report_template.html")
        html = template.render(report=report_data)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Relatório HTML gerado em: {output_path}")
