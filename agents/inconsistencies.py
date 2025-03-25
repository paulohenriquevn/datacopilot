# datacopilot/agents/inconsistencies.py

import pandas as pd
import re

class InconsistencyAgent:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.report = {}

    def detect_duplicates(self):
        duplicates = self.df.duplicated()
        count = duplicates.sum()
        self.report['duplicates'] = {
            'count': int(count),
            'percent': round(100 * count / len(self.df), 2)
        }

    def validate_formats(self):
        corrections = {}

        if 'date' in self.df.columns:
            try:
                self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
                corrections['date'] = 'Convertido para datetime (YYYY-MM-DD)'
            except Exception as e:
                corrections['date'] = f'Erro ao converter: {str(e)}'

        if 'phone' in self.df.columns:
            self.df['phone'] = self.df['phone'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
            corrections['phone'] = 'Mantido apenas dígitos (regex aplicado)'

        if 'email' in self.df.columns:
            self.df['email_valid'] = self.df['email'].astype(str).apply(
                lambda x: bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", x))
            )
            invalid_count = (~self.df['email_valid']).sum()
            corrections['email'] = f'{invalid_count} e-mails inválidos identificados'

        self.report['format_corrections'] = corrections

    def run(self):
        self.detect_duplicates()
        self.validate_formats()
        return self.report