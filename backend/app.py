from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'database'),
    'database': os.getenv('DB_NAME', 'veterinaria'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    """Crear conexión a la base de datos"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

# ==================== RUTAS DE CLIENTES ====================

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM clientes ORDER BY id DESC')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(clientes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    """Crear nuevo cliente"""
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            '''INSERT INTO clientes (nombre, apellido, telefono, email, direccion)
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['nombre'], data['apellido'], data.get('telefono'), 
             data.get('email'), data.get('direccion'))
        )
        nuevo_cliente = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(nuevo_cliente), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE MASCOTAS ====================

@app.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    """Obtener todas las mascotas con información del dueño"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT m.*, 
                   c.nombre as cliente_nombre, 
                   c.apellido as cliente_apellido,
                   c.telefono as cliente_telefono
            FROM mascotas m
            JOIN clientes c ON m.cliente_id = c.id
            ORDER BY m.id DESC
        ''')
        mascotas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(mascotas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mascotas', methods=['POST'])
def create_mascota():
    """Crear nueva mascota"""
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            '''INSERT INTO mascotas (nombre, especie, raza, edad, peso, cliente_id)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING *''',
            (data['nombre'], data['especie'], data.get('raza'), 
             data.get('edad'), data.get('peso'), data['cliente_id'])
        )
        nueva_mascota = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(nueva_mascota), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTAS DE CITAS ====================

@app.route('/api/citas', methods=['GET'])
def get_citas():
    """Obtener todas las citas con información completa"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('''
            SELECT cit.*, 
                   m.nombre as mascota_nombre,
                   m.especie as mascota_especie,
                   c.nombre as cliente_nombre,
                   c.apellido as cliente_apellido,
                   c.telefono as cliente_telefono
            FROM citas cit
            JOIN mascotas m ON cit.mascota_id = m.id
            JOIN clientes c ON m.cliente_id = c.id
            ORDER BY cit.fecha_cita DESC
        ''')
        citas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(citas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/citas', methods=['POST'])
def create_cita():
    """Crear nueva cita"""
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            '''INSERT INTO citas (mascota_id, fecha_cita, motivo, estado, observaciones)
               VALUES (%s, %s, %s, %s, %s) RETURNING *''',
            (data['mascota_id'], data['fecha_cita'], data['motivo'],
             data.get('estado', 'Pendiente'), data.get('observaciones'))
        )
        nueva_cita = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(nueva_cita), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/citas/<int:cita_id>', methods=['PUT'])
def update_cita(cita_id):
    """Actualizar estado de cita"""
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Error de conexión a la base de datos'}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            '''UPDATE citas SET estado = %s, observaciones = %s
               WHERE id = %s RETURNING *''',
            (data.get('estado'), data.get('observaciones'), cita_id)
        )
        cita_actualizada = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(cita_actualizada)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RUTA DE SALUD ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del servicio"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 500

@app.route('/')
def home():
    """Ruta principal"""
    return jsonify({
        'message': 'API Veterinaria - Sistema de Gestión',
        'version': '1.0.0',
        'endpoints': {
            'clientes': '/api/clientes',
            'mascotas': '/api/mascotas',
            'citas': '/api/citas',
            'health': '/api/health'
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
