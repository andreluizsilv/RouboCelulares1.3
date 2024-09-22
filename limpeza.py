import os
import django
import pandas as pd

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celulares_subtraidos.settings')
django.setup()

# Importar os modelos necessários
from roubo_celulares.models import Roubo, Bairro


def processar_hora(hora):
    if pd.isna(hora) or hora == 'Hora desconhecida':
        return pd.to_datetime('00:00:00').time()  # Preencher com horário padrão
    try:
        # Tenta converter para hora no formato '%H:%M:%S'
        hora_convertida = pd.to_datetime(hora, format='%H:%M:%S', errors='coerce')
        if pd.isna(hora_convertida):
            # Se falhar, tenta converter no formato '%H:%M'
            hora_convertida = pd.to_datetime(hora, format='%H:%M', errors='coerce')
        return hora_convertida.time() if not pd.isna(hora_convertida) else pd.to_datetime('00:00:00').time()
    except (ValueError, TypeError):
        return pd.to_datetime('00:00:00').time()  # Preencher com horário padrão


def limpar_e_salvar_bairros():
    try:
        # Ler o arquivo Excel de bairros
        bairros_df = pd.read_excel('bairros_lat_log.xlsx')

        # Converter LATITUDE e LONGITUDE para strings e substituir vírgula por ponto
        bairros_df['LATITUDE'] = bairros_df['LATITUDE'].astype(str).str.replace(',', '.')
        bairros_df['LONGITUDE'] = bairros_df['LONGITUDE'].astype(str).str.replace(',', '.')

        # Tratar valores ausentes e duplicidades
        bairros_df = bairros_df.dropna(
            subset=['LATITUDE', 'LONGITUDE', 'BAIRRO'])  # Remove linhas sem latitude, longitude ou bairro
        bairros_df = bairros_df.drop_duplicates(subset=['BAIRRO', 'LATITUDE', 'LONGITUDE'])

        # Verificação de ausência de valores nulos após tratamento
        if bairros_df[['LATITUDE', 'LONGITUDE', 'BAIRRO']].isnull().any().any():
            raise ValueError(
                "Os dados de LATITUDE, LONGITUDE ou BAIRRO contêm valores nulos após o tratamento inicial.")

        # Agrupar por bairro e fixar coordenadas (por exemplo, a primeira encontrada)
        bairros_agrupados_df = bairros_df.groupby('BAIRRO').agg({
            'LATITUDE': 'first',  # Ou use 'mean' para média se preferir
            'LONGITUDE': 'first'  # Ou use 'mean' para média se preferir
        }).reset_index()

        # Criar ou atualizar os bairros no banco de dados
        for index, row in bairros_agrupados_df.iterrows():
            if pd.isna(row['LATITUDE']) or pd.isna(row['LONGITUDE']):
                print(f"Bairro {row['BAIRRO']} possui coordenadas nulas e será ignorado.")
                continue

            obj, created = Bairro.objects.update_or_create(
                nome=row['BAIRRO'],
                defaults={'latitude': row['LATITUDE'], 'longitude': row['LONGITUDE']}
            )
            if created:
                print(f"Bairro {row['BAIRRO']} criado com sucesso!")
            else:
                print(f"Bairro {row['BAIRRO']} atualizado com sucesso!")

        print("Dados de bairros salvos no banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar os dados de bairros: {str(e)}")


def limpar_e_salvar_roubos():
    try:
        # Ler o arquivo Excel de roubos
        celulares_df = pd.read_excel('celulares_df.xlsx')

        # Tratar os dados de roubo
        celulares_df['HORA_OCORRENCIA'] = celulares_df['HORA_OCORRENCIA'].apply(processar_hora)
        celulares_df['DESCR_TIPOLOCAL'] = celulares_df['DESCR_TIPOLOCAL'].fillna('Tipo local desconhecido')
        celulares_df['LOGRADOURO'] = celulares_df['LOGRADOURO'].fillna('Logradouro desconhecido')
        celulares_df['NUMERO_LOGRADOURO'] = celulares_df['NUMERO_LOGRADOURO'].astype(str).fillna('Número desconhecido')
        celulares_df['BAIRRO'] = celulares_df['BAIRRO'].fillna('Bairro desconhecido')
        celulares_df['CEP'] = celulares_df['CEP'].astype(str).replace('nan', 'CEP desconhecido')

        # Criar uma lista de objetos Roubo usando compreensão de lista
        roubos = []
        for index, row in celulares_df.iterrows():
            try:
                # Busca o bairro correspondente
                bairro_obj = Bairro.objects.filter(nome=row['BAIRRO']).first()

                # Verifica se o bairro tem latitude e longitude válidas
                if not bairro_obj or bairro_obj.latitude is None or bairro_obj.longitude is None:
                    print(f"Bairro '{row['BAIRRO']}' não possui coordenadas válidas. Ignorando roubo na linha {index}.")
                    continue  # Ignora este roubo

                # Cria o objeto Roubo
                roubo = Roubo(
                    id_delegacia=row['ID_DELEGACIA'],
                    data_ocorrencia_bo=row['DATA_OCORRENCIA_BO'],
                    hora_ocorrencia=row['HORA_OCORRENCIA'],
                    descr_tipolocal=row['DESCR_TIPOLOCAL'],
                    logradouro=row['LOGRADOURO'],
                    numero_logradouro=row['NUMERO_LOGRADOURO'],
                    bairro=bairro_obj,  # Atribui o objeto bairro
                    cidade=row['CIDADE'],
                    cep=row['CEP']
                )
                roubos.append(roubo)
            except Exception as e:
                print(f"Erro ao processar o roubo na linha {index}: {str(e)}")

        # Inserir os objetos no banco de dados
        if roubos:
            Roubo.objects.bulk_create(roubos)
            print("Dados de roubos salvos no banco de dados com sucesso!")
        else:
            print("Nenhum roubo foi salvo, todos os registros foram ignorados devido a erros.")
    except Exception as e:
        print(f"Erro ao salvar os dados de roubos: {str(e)}")


if __name__ == "__main__":
    limpar_e_salvar_bairros()  # Primeiro, salva os bairros
    limpar_e_salvar_roubos()  # Depois, salva os roubos
