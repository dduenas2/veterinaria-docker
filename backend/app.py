"""
Backend API - Sistema de Gestión Veterinaria
Flask REST API con PostgreSQL
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)
CORS(app)

# Configuración de base de datos desde variables de entorno
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'database'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'veterinaria'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}


def get_db_connection():
    """Establece conexión con PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None


# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    try:
        conn = get_db_connection()
        if conn:
            conn.close()
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            }), 200
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


# ============================================
# CLIENTES - CRUD COMPLETO
# ============================================

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """Obtener todos los clientes"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes ORDER BY id')
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clientes/<int:id>', methods=['GET'])
def get_cliente(id):
    """Obtener un cliente específico por ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('SELECT * FROM clientes WHERE id = %s', (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        
        if cliente:
            return jsonify(cliente), 200
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    """Crear un nuevo cliente"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre', 'apellido', 'telefono', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO clientes (nombre, apellido, telefono, email, direccion) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (data['nombre'], data['apellido'], data['telefono'], 
             data['email'], data.get('direccion', ''))
        )
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Cliente creado exitosamente',
            'id': new_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    """Actualizar un cliente existente"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        # Construir query dinámicamente solo con campos proporcionados
        update_fields = []
        values = []
        
        if 'nombre' in data:
            update_fields.append('nombre = %s')
            values.append(data['nombre'])
        if 'apellido' in data:
            update_fields.append('apellido = %s')
            values.append(data['apellido'])
        if 'telefono' in data:
            update_fields.append('telefono = %s')
            values.append(data['telefono'])
        if 'email' in data:
            update_fields.append('email = %s')
            values.append(data['email'])
        if 'direccion' in data:
            update_fields.append('direccion = %s')
            values.append(data['direccion'])
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        values.append(id)
        query = f"UPDATE clientes SET {', '.join(update_fields)} WHERE id = %s"
        
        cur = conn.cursor()
        cur.execute(query, values)
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Cliente actualizado exitosamente'}), 200
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    """Eliminar un cliente"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('DELETE FROM clientes WHERE id = %s', (id,))
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
        else:
            return jsonify({'error': 'Cliente no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# MASCOTAS - CRUD COMPLETO
# ============================================

@app.route('/api/mascotas', methods=['GET'])
def get_mascotas():
    """Obtener todas las mascotas"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            SELECT m.*, c.nombre as cliente_nombre, c.apellido as cliente_apellido
            FROM mascotas m
            LEFT JOIN clientes c ON m.cliente_id = c.id
            ORDER BY m.id
        ''')
        mascotas = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(mascotas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['GET'])
def get_mascota(id):
    """Obtener una mascota específica por ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            SELECT m.*, c.nombre as cliente_nombre, c.apellido as cliente_apellido
            FROM mascotas m
            LEFT JOIN clientes c ON m.cliente_id = c.id
            WHERE m.id = %s
        ''', (id,))
        mascota = cur.fetchone()
        cur.close()
        conn.close()
        
        if mascota:
            return jsonify(mascota), 200
        else:
            return jsonify({'error': 'Mascota no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mascotas', methods=['POST'])
def create_mascota():
    """Crear una nueva mascota"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre', 'especie', 'cliente_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO mascotas (nombre, especie, raza, edad, peso, cliente_id) 
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id''',
            (data['nombre'], data['especie'], data.get('raza', ''),
             data.get('edad', None), data.get('peso', None), data['cliente_id'])
        )
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Mascota creada exitosamente',
            'id': new_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['PUT'])
def update_mascota(id):
    """Actualizar una mascota existente"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        update_fields = []
        values = []
        
        if 'nombre' in data:
            update_fields.append('nombre = %s')
            values.append(data['nombre'])
        if 'especie' in data:
            update_fields.append('especie = %s')
            values.append(data['especie'])
        if 'raza' in data:
            update_fields.append('raza = %s')
            values.append(data['raza'])
        if 'edad' in data:
            update_fields.append('edad = %s')
            values.append(data['edad'])
        if 'peso' in data:
            update_fields.append('peso = %s')
            values.append(data['peso'])
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        values.append(id)
        query = f"UPDATE mascotas SET {', '.join(update_fields)} WHERE id = %s"
        
        cur = conn.cursor()
        cur.execute(query, values)
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Mascota actualizada exitosamente'}), 200
        else:
            return jsonify({'error': 'Mascota no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/mascotas/<int:id>', methods=['DELETE'])
def delete_mascota(id):
    """Eliminar una mascota"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('DELETE FROM mascotas WHERE id = %s', (id,))
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Mascota eliminada exitosamente'}), 200
        else:
            return jsonify({'error': 'Mascota no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# CITAS - CRUD COMPLETO
# ============================================

@app.route('/api/citas', methods=['GET'])
def get_citas():
    """Obtener todas las citas"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            SELECT ci.*, m.nombre as mascota_nombre, 
                   c.nombre as cliente_nombre, c.apellido as cliente_apellido
            FROM citas ci
            LEFT JOIN mascotas m ON ci.mascota_id = m.id
            LEFT JOIN clientes c ON m.cliente_id = c.id
            ORDER BY ci.fecha DESC, ci.hora DESC
        ''')
        citas = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify(citas), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/citas/<int:id>', methods=['GET'])
def get_cita(id):
    """Obtener una cita específica por ID"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('''
            SELECT ci.*, m.nombre as mascota_nombre,
                   c.nombre as cliente_nombre, c.apellido as cliente_apellido
            FROM citas ci
            LEFT JOIN mascotas m ON ci.mascota_id = m.id
            LEFT JOIN clientes c ON m.cliente_id = c.id
            WHERE ci.id = %s
        ''', (id,))
        cita = cur.fetchone()
        cur.close()
        conn.close()
        
        if cita:
            return jsonify(cita), 200
        else:
            return jsonify({'error': 'Cita no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/citas', methods=['POST'])
def create_cita():
    """Crear una nueva cita"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['mascota_id', 'fecha', 'hora', 'motivo']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute(
            '''INSERT INTO citas (mascota_id, fecha, hora, motivo, estado) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id''',
            (data['mascota_id'], data['fecha'], data['hora'], 
             data['motivo'], data.get('estado', 'Programada'))
        )
        new_id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': 'Cita creada exitosamente',
            'id': new_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/citas/<int:id>', methods=['PUT'])
def update_cita(id):
    """Actualizar una cita existente"""
    try:
        data = request.get_json()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        update_fields = []
        values = []
        
        if 'fecha' in data:
            update_fields.append('fecha = %s')
            values.append(data['fecha'])
        if 'hora' in data:
            update_fields.append('hora = %s')
            values.append(data['hora'])
        if 'motivo' in data:
            update_fields.append('motivo = %s')
            values.append(data['motivo'])
        if 'estado' in data:
            update_fields.append('estado = %s')
            values.append(data['estado'])
        
        if not update_fields:
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        values.append(id)
        query = f"UPDATE citas SET {', '.join(update_fields)} WHERE id = %s"
        
        cur = conn.cursor()
        cur.execute(query, values)
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Cita actualizada exitosamente'}), 200
        else:
            return jsonify({'error': 'Cita no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/citas/<int:id>', methods=['DELETE'])
def delete_cita(id):
    """Eliminar una cita"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a base de datos'}), 500
        
        cur = conn.cursor()
        cur.execute('DELETE FROM citas WHERE id = %s', (id,))
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if affected_rows > 0:
            return jsonify({'message': 'Cita eliminada exitosamente'}), 200
        else:
            return jsonify({'error': 'Cita no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================
# MANEJO DE ERRORES
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================
# INICIAR SERVIDOR
# ============================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
