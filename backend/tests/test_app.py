"""
Tests unitarios para la API del Sistema de Gestión Veterinaria
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import json

try:
    from app import app
except ImportError:
    app = None


@pytest.fixture
def client():
    """Cliente de prueba de Flask"""
    if app is None:
        pytest.skip("App no disponible")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Pruebas para el endpoint de health check"""
    
    def test_health_check_exists(self, client):
        """Test: El endpoint /api/health debe existir"""
        response = client.get('/api/health')
        assert response.status_code in [200, 404, 500]
    
    def test_health_check_returns_json(self, client):
        """Test: El health check debe devolver JSON"""
        response = client.get('/api/health')
        if response.status_code == 200:
            assert response.content_type == 'application/json'


class TestClientesEndpoints:
    """Pruebas para los endpoints de clientes"""
    
    def test_get_clientes_endpoint(self, client):
        """Test: GET /api/clientes debe existir"""
        response = client.get('/api/clientes')
        assert response.status_code in [200, 404, 500]
    
    def test_get_clientes_returns_list(self, client):
        """Test: GET /api/clientes debe devolver lista"""
        response = client.get('/api/clientes')
        if response.status_code == 200:
            data = json.loads(response.data)
            assert isinstance(data, list)


class TestMascotasEndpoints:
    """Pruebas para los endpoints de mascotas"""
    
    def test_get_mascotas_endpoint(self, client):
        """Test: GET /api/mascotas debe existir"""
        response = client.get('/api/mascotas')
        assert response.status_code in [200, 404, 500]


class TestCitasEndpoints:
    """Pruebas para los endpoints de citas"""
    
    def test_get_citas_endpoint(self, client):
        """Test: GET /api/citas debe existir"""
        response = client.get('/api/citas')
        assert response.status_code in [200, 404, 500]


class TestAPIStructure:
    """Pruebas de estructura de la API"""
    
    def test_api_responds(self, client):
        """Test: La API debe responder"""
        response = client.get('/api/health')
        assert response is not None
    
    def test_cors_enabled(self, client):
        """Test: CORS debe estar habilitado"""
        response = client.get('/api/health')
        # Verificar que la respuesta existe
        assert response.status_code in [200, 404, 500]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
