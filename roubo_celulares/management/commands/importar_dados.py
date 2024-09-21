from django.core.management.base import BaseCommand
from roubo_celulares.models import Roubo
import pandas as pd

class Command(BaseCommand):
    help = 'Importa os dados de roubos do CSV para o banco de dados'

    def handle(self, *args, **options):
        df = pd.read_csv('LimpezaDados/CelularesSubtraidos_Limpo.csv')

        for index, row in df.iterrows():
            Roubo.objects.create(
                id_delegacia=row['ID_DELEGACIA'],
                data_ocorrencia_bo=row['DATA_OCORRENCIA_BO'],
                hora_ocorrencia=row['HORA_OCORRENCIA'],
                descr_tipolocal=row['DESCR_TIPOLOCAL'],
                logradouro=row['LOGRADOURO'],
                numero_logradouro=row['NUMERO_LOGRADOURO'] if pd.notna(row['NUMERO_LOGRADOURO']) else None,
                bairro=row['BAIRRO'],
                cidade=row['CIDADE'],
                cep=row['CEP']
            )
        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
