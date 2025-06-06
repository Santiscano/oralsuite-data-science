import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

BASE_URL = Path(__file__).resolve().parent # ruta del archivo actual
csv_path = BASE_URL.parent / 'data' / 'json_oralsuit_csv.csv'

def view_path():
    print(f"Ruta del archivo CSV: {csv_path}")
    return csv_path

dataFrameOralsuite = pd.read_csv(csv_path)

#1. ¿Cuál es el número total de órdenes de trabajo recibidas en un período determinado (por ejemplo, mensual, trimestral, anual)?
def ordenes_trabajo_por_periodo(periodo='M'):
    dataFrame = dataFrameOralsuite.copy()
    # Asegurar que la columna es datetime
    dataFrame['finalDeliveryDate'] = pd.to_datetime(dataFrame['finalDeliveryDate'], errors='coerce')
    
    # Agrupar por periodo
    dataFrame['periodo'] = dataFrame['finalDeliveryDate'].dt.to_period(periodo)
    ordenes_por_periodo = dataFrame.groupby('periodo').size().reset_index(name='numero_ordenes')
    
    # Convertir a string para que sea serializable (Period -> str)
    ordenes_por_periodo['periodo'] = ordenes_por_periodo['periodo'].astype(str)
    
    # Preparar formato para Chart.js
    chart_data = {
        "labels": ordenes_por_periodo['periodo'].tolist(),
        "datasets": [
            {
                "label": "Número de órdenes de trabajo por período",
                "data": ordenes_por_periodo['numero_ordenes'].tolist(),
                "backgroundColor": "#36A2EB"
            }
        ]
    }
    
    return chart_data


#2. ¿Cuáles son las 5 clases de trabajo más solicitadas por volumen?
def trabajos_mas_solicitados():
    colors = ['#005f73','#0a9396','#94d2bd','#e9d8a6','#66b3ff']
    dataFrame = dataFrameOralsuite.copy()
    
    clases_trabajo = dataFrame['workClass'].value_counts().head(5).reset_index()
    clases_trabajo.columns = ['workClass', 'numero_ordenes']
    
    # Convertir a estructura para Chart.js
    chart_data = {
        "labels": clases_trabajo['workClass'].tolist(),
        "datasets": [
            {
                "label": "Número de órdenes por clase de trabajo",
                "data": clases_trabajo['numero_ordenes'].tolist(),
                "backgroundColor": colors[:len(clases_trabajo)]  # evitar overflow si hay menos de 5
            }
        ]
    }
    
    return chart_data


#3 ¿Cuál es el tiempo promedio de entrega (desde la fecha de entrada hasta la fecha de entrega final) para cada clase de trabajo?
def tiempo_entrega_por_clase_trabajo():
    dataFrame = dataFrameOralsuite.copy()
    
    dataFrame['finalDeliveryDate'] = pd.to_datetime(dataFrame['finalDeliveryDate'], errors='coerce')
    dataFrame['entryDate'] = pd.to_datetime(dataFrame['entryDate'], errors='coerce')
    
    dataFrame['tiempo_entrega'] = (dataFrame['finalDeliveryDate'] - dataFrame['entryDate']).dt.days
    
    # Agrupar por clase de trabajo y calcular el promedio
    tiempo_entrega_por_clase = (
        dataFrame.groupby('workClass')['tiempo_entrega']
        .mean()
        .reset_index()
        .dropna()
    )
    
    # Redondear los días a 2 decimales
    tiempo_entrega_por_clase['tiempo_entrega'] = tiempo_entrega_por_clase['tiempo_entrega'].round(2)

    # Preparar formato para Chart.js
    chart_data = {
        "labels": tiempo_entrega_por_clase['workClass'].tolist(),
        "datasets": [
            {
                "label": "Días de entrega promedio",
                "data": tiempo_entrega_por_clase['tiempo_entrega'].tolist(),
                "backgroundColor": "#94d2bd"
            }
        ]
    }
    
    return chart_data



#4. ¿Qué porcentaje de órdenes no tiene una fecha de entrega final especificada (noDeliveryDate es True) torta de con fecha vs sin fecha?
def porcentaje_entrega_final():
    colors = ['#ff9999','#66b3ff']
    dataFrame = dataFrameOralsuite.copy()
    
    dataFrame['noDeliveryDate'] = dataFrame['noDeliveryDate'].astype(bool)
    
    porcentaje_entrega = dataFrame['noDeliveryDate'].value_counts(normalize=True) * 100
    porcentaje_entrega = porcentaje_entrega.sort_index()  # Para que False esté antes que True
    
    # Mapeo de etiquetas
    etiquetas = ['Con fecha de entrega', 'Sin fecha de entrega']
    
    chart_data = {
        "labels": etiquetas,
        "datasets": [
            {
                "label": "Porcentaje de órdenes",
                "data": [round(porcentaje_entrega.get(False, 0.0), 2),
                        round(porcentaje_entrega.get(True, 0.0), 2)],
                "backgroundColor": colors
            }
        ]
    }
    
    return chart_data


#5. ¿Cuáles son las 10 clínicas (companyNameId) que generan el mayor volumen de trabajo?
def clinicas_mayor_volumen():
    dataFrame = dataFrameOralsuite.copy()
    # Contar órdenes por clínica y tomar las 10 principales
    clinicas_volumen = (
        dataFrame['companyNameId']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'index': 'companyNameId', 'companyNameId': 'numero_ordenes'})
    )

    # Preparar estructura para Chart.js (tipo línea)
    chart_data = {
        "labels": clinicas_volumen['companyNameId'].astype(str).tolist(),  # convertir IDs a string por compatibilidad
        "datasets": [
            {
                "label": "Número de órdenes",
                "data": clinicas_volumen['numero_ordenes'].tolist(),
                "borderColor": "#005f73",
                "backgroundColor": "#005f73",
                "fill": False,
                "tension": 0.3,
                "pointBackgroundColor": "#005f73"
            }
        ]
    }

    return chart_data


#6. ¿Cuáles son los 10 odontólogos (dentistNameId) que envían la mayor cantidad de órdenes?
def odontologos_mayor_volumen():
    dataFrame = dataFrameOralsuite.copy()
    odontologos_volumen = (
        dataFrame['dentistNameId']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'index': 'dentistNameId', 'dentistNameId': 'numero_ordenes'})
    )

    chart_data = {
        "labels": odontologos_volumen['dentistNameId'].astype(str).tolist(),
        "datasets": [
            {
                "label": "Número de órdenes",
                "data": odontologos_volumen['numero_ordenes'].tolist(),
                "borderColor": "#0a9396",
                "backgroundColor": "#0a9396",
                "fill": False,
                "tension": 0.3,
                "pointBackgroundColor": "#0a9396"
            }
        ]
    }

    return chart_data



#7. ¿Cuál es la distribución de las 5 mayores clases de trabajo por las 5 clínicas principal?
def clases_trabajo_por_clinica():
    colors = ['#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#66b3ff']
    dataFrame = dataFrameOralsuite.copy()
    # Definir los colores para las clases de trabajo

    # Top 5 clínicas y top 5 clases de trabajo
    top_clinicas = dataFrame['companyNameId'].value_counts().head(5).index.tolist()
    top_clases = dataFrame['workClass'].value_counts().head(5).index.tolist()

    # Filtrar el dataframe por estos valores
    df_filtrado = dataFrame[
        dataFrame['companyNameId'].isin(top_clinicas) & dataFrame['workClass'].isin(top_clases)
    ]

    # Contar el número de órdenes por clínica y clase de trabajo
    conteo = (
        df_filtrado
        .groupby(['companyNameId', 'workClass'])
        .size()
        .unstack(fill_value=0)
        .reindex(index=top_clinicas, columns=top_clases, fill_value=0)
    )

    # Preparar estructura para Chart.js
    datasets = []
    for i, clase in enumerate(top_clases):
        datasets.append({
            "label": clase,
            "data": conteo[clase].tolist(),
            "backgroundColor": colors[i],
        })

    chart_data = {
        "labels": top_clinicas,
        "datasets": datasets
    }

    return chart_data




#8. ¿Cuál es el color de diente más frecuentemente solicitado para coronas (metal cerámica, totalmente cerámicas) y placas estéticas?
#9. ¿Cuál es la guía de color más utilizada por los odontólogos?
#10. ¿Cuál es la proporción de trabajos que tienen un antagonista versus los que no lo tienen?
#11. ¿Cuál es el promedio de dientes trabajados por orden para las clases de trabajo que aplican (teethWork)?
#12. ¿Existen variaciones estacionales en el volumen de trabajo recibido?
#13. ¿Cuál es el número de órdenes atrasadas (donde finalDeliveryDate es posterior a la fecha actual si noDeliveryDate es False)?
#14. ¿Cómo se distribuye el volumen de trabajo entre las clínicas grandes y los odontólogos individuales con su propia clínica?
#15. ¿Qué clase de trabajo tiene la mayor  tiempo de entrega?
#16. ¿Cuántas órdenes corresponden a aparatos funcionales de odontopediatría y cuáles son los más solicitados?
#17. ¿Cuál es la frecuencia de las diferentes "observaciones" en las órdenes, y se pueden correlacionar con ciertos tipos de trabajos o retrasos?
#18.¿Qué porcentaje de las órdenes corresponde a trabajos sobre implantes, y cómo se distribuyen entre los diferentes tipos de pilares (titanio, personalizado, T-base)?
#19 ¿Cuál es el número promedio de órdenes de trabajo por paciente en un período determinado?
#20. ¿Cuántos paciente han sido atendidos por varios odontologos?



