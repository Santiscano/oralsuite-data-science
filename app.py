from flask import Flask, request, jsonify
from flask_cors import CORS

from noteBook.generadorGraficas import view_path, ordenes_trabajo_por_periodo, trabajos_mas_solicitados, tiempo_entrega_por_clase_trabajo, porcentaje_entrega_final, clinicas_mayor_volumen, odontologos_mayor_volumen, clases_trabajo_por_clinica

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})


@app.route('/api/csv', methods=['GET'])
def hello():
    path = view_path()
    return jsonify(message=f'Ruta del archivo CSV: {path}')


@app.route('/api/orders')
def get_orders():
    """
    Endpoint to get the number of work orders received in a specified period.
    The period can be specified as a query parameter (e.g., ?period=M for monthly).
    Default is monthly ('M').
    Example usage: /api/orders?period=M
    """
    period = request.args.get('period', 'M')
    json_data = ordenes_trabajo_por_periodo(periodo=period)
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})

@app.route('/api/most-requested-jobs')
def get_most_requested_jobs():
    """
    Endpoint to get the 5 most requested job classes by volume.
    Example usage: /api/most-requested-jobs
    """
    json_data = trabajos_mas_solicitados()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})

@app.route('/api/average-delivery-time')
def get_average_delivery_time():
    """
    Endpoint to get the average delivery time for each job class.
    Example usage: /api/average-delivery-time
    """
    json_data = tiempo_entrega_por_clase_trabajo()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})

@app.route('/api/final-delivery-percentage')
def get_final_delivery_percentage():
    """
    Endpoint to get the percentage of final deliveries for each job class.
    Example usage: /api/final-delivery-percentage
    """
    json_data = porcentaje_entrega_final()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})


@app.route('/api/clinics-by-volume')
def get_clinics_by_volume():
    """
    Endpoint to get the clinics with the highest volume of work orders.
    Example usage: /api/clinics-by-volume
    """
    json_data = clinicas_mayor_volumen()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})


@app.route('/api/dentists-by-volume')
def get_dentists_by_volume():
    """
    Endpoint to get the dentists with the highest volume of work orders.
    Example usage: /api/dentists-by-volume
    """
    json_data = odontologos_mayor_volumen()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})


@app.route('/api/work-classes-by-clinic')
def get_work_classes_by_clinic():
    """
    Endpoint to get the work classes by clinic.
    Example usage: /api/work-classes-by-clinic
    """
    json_data = clases_trabajo_por_clinica()
    return jsonify({'data': json_data, 'message': 'Data prepared successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)