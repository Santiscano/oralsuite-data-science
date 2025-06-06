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
def preparar_datos_ordenes_trabajo(periodo='M'):
    # Asegurar que la columna es datetime
    dataFrameOralsuite['finalDeliveryDate'] = pd.to_datetime(dataFrameOralsuite['finalDeliveryDate'], errors='coerce')
    
    # Agrupar por periodo
    dataFrameOralsuite['periodo'] = dataFrameOralsuite['finalDeliveryDate'].dt.to_period(periodo)
    ordenes_por_periodo = dataFrameOralsuite.groupby('periodo').size().reset_index(name='numero_ordenes')
    
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
colors = ['#005f73','#0a9396','#94d2bd','#e9d8a6','#66b3ff']
def graficar_clases_trabajo_mas_solicitadas(dataFrame):
    clases_trabajo = dataFrame['workClass'].value_counts().head(5).reset_index()
    clases_trabajo.columns = ['workClass', 'numero_ordenes']
    
    plt.figure(figsize=(12, 6))
    sns.barplot(y='workClass', x='numero_ordenes', data=clases_trabajo, palette=colors)
    plt.title('5 Clases de trabajo más solicitadas')
    plt.ylabel('Clase de trabajo')
    plt.xlabel('Número de órdenes')
    plt.tight_layout()
    plt.show()
# if __name__ == "__main__":
#     graficar_clases_trabajo_mas_solicitadas(dataFrameOralsuite)


#3 ¿Cuál es el tiempo promedio de entrega (desde la fecha de entrada hasta la fecha de entrega final) para cada clase de trabajo?
def graficar_tiempo_entrega_por_clase_trabajo(dataFrame):
    dataFrame['finalDeliveryDate'] = pd.to_datetime(dataFrame['finalDeliveryDate'], errors='coerce')
    dataFrame['entryDate'] = pd.to_datetime(dataFrame['entryDate'], errors='coerce')
    dataFrame['tiempo_entrega'] = (dataFrame['finalDeliveryDate'] - dataFrame['entryDate']).dt.days
    
    tiempo_entrega_por_clase = dataFrame.groupby('workClass')['tiempo_entrega'].mean().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x='workClass', y='tiempo_entrega', data=tiempo_entrega_por_clase)
    plt.title('Tiempo promedio de entrega por clase de trabajo')
    plt.xlabel('Clase de trabajo')
    plt.ylabel('Días de entrega promedio')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
# if __name__ == "__main__":
#     graficar_tiempo_entrega_por_clase_trabajo(dataFrameOralsuite)


#4. ¿Qué porcentaje de órdenes no tiene una fecha de entrega final especificada (noDeliveryDate es True) torta de con fecha vs sin fecha?
colors = ['#ff9999','#66b3ff']
def graficar_porcentaje_entrega_final(dataFrame):
    dataFrame['noDeliveryDate'] = dataFrame['noDeliveryDate'].astype(bool)
    porcentaje_entrega = dataFrame['noDeliveryDate'].value_counts(normalize=True) * 100
    
    plt.figure(figsize=(8, 6))
    plt.pie(porcentaje_entrega, labels=porcentaje_entrega.index, autopct='%1.1f%%', startangle=140)
    plt.title('Porcentaje de órdenes sin fecha de entrega')
    plt.show()
# if __name__ == "__main__":
#     graficar_porcentaje_entrega_final(dataFrameOralsuite)


#5. ¿Cuáles son las 10 clínicas (companyNameId) que generan el mayor volumen de trabajo?
def graficar_clinicas_mayor_volumen(dataFrame):
    clinicas_volumen = dataFrame['companyNameId'].value_counts().head(10).reset_index()
    clinicas_volumen.columns = ['companyNameId', 'numero_ordenes']
    plt.figure(figsize=(12, 6))
    plt.plot(clinicas_volumen['companyNameId'], clinicas_volumen['numero_ordenes'], marker='o', color='#005f73')
    plt.title('10 Clínicas con mayor volumen de trabajo')
    plt.xlabel('Clínica')
    plt.ylabel('Número de órdenes')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
# if __name__ == "__main__":
#     graficar_clinicas_mayor_volumen(dataFrameOralsuite)


#6. ¿Cuáles son los 10 odontólogos (dentistNameId) que envían la mayor cantidad de órdenes?
def graficar_odontologos_mayor_volumen(dataFrame):
    odontologos_volumen = dataFrame['dentistNameId'].value_counts().head(10).reset_index()
    odontologos_volumen.columns = ['dentistNameId', 'numero_ordenes']
    plt.figure(figsize=(12, 6))
    plt.plot(odontologos_volumen['dentistNameId'], odontologos_volumen['numero_ordenes'], marker='o', color='#0a9396')
    plt.title('10 Odontólogos con mayor cantidad de órdenes')
    plt.xlabel('Odontólogo')
    plt.ylabel('Número de órdenes')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# if __name__ == "__main__":
#     graficar_odontologos_mayor_volumen(dataFrameOralsuite)


#7. ¿Cuál es la distribución de las 5 mayores clases de trabajo por las 5 clínicas principal?
colors = ['#005f73', '#0a9396', '#94d2bd', '#e9d8a6', '#66b3ff']
def graficar_clases_trabajo_por_clinica(dataFrame):
    top_clinicas = dataFrame['companyNameId'].value_counts().head(5).index
    top_clases = dataFrame['workClass'].value_counts().head(5).index
    
    df_filtrado = dataFrame[dataFrame['companyNameId'].isin(top_clinicas) & dataFrame['workClass'].isin(top_clases)]
    
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df_filtrado, x='companyNameId', hue='workClass', palette=colors)
    plt.title('Distribución de las 5 mayores clases de trabajo por las 5 clínicas principales')
    plt.xlabel('Clínica')
    plt.ylabel('Número de órdenes')
    plt.xticks(rotation=90)
    plt.legend(title='Clase de trabajo')
    plt.tight_layout()
    plt.show()

# if __name__ == "__main__":
#     graficar_clases_trabajo_por_clinica(dataFrameOralsuite)




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



