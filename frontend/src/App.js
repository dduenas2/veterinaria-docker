import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [clientes, setClientes] = useState([]);
  const [mascotas, setMascotas] = useState([]);
  const [citas, setCitas] = useState([]);
  const [loading, setLoading] = useState(false);

  // Cargar datos al iniciar
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [clientesRes, mascotasRes, citasRes] = await Promise.all([
        axios.get(`${API_URL}/clientes`),
        axios.get(`${API_URL}/mascotas`),
        axios.get(`${API_URL}/citas`)
      ]);
      setClientes(clientesRes.data);
      setMascotas(mascotasRes.data);
      setCitas(citasRes.data);
    } catch (error) {
      console.error('Error cargando datos:', error);
      alert('Error al cargar los datos. Verifica que el backend esté corriendo.');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <span className="logo-icon">🐾</span>
            <h1>Veterinaria PetCare</h1>
          </div>
          <p className="subtitle">Sistema de Gestión Integral</p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="nav-tabs">
        <button 
          className={`nav-tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={`nav-tab ${activeTab === 'clientes' ? 'active' : ''}`}
          onClick={() => setActiveTab('clientes')}
        >
          👥 Clientes
        </button>
        <button 
          className={`nav-tab ${activeTab === 'mascotas' ? 'active' : ''}`}
          onClick={() => setActiveTab('mascotas')}
        >
          🐕 Mascotas
        </button>
        <button 
          className={`nav-tab ${activeTab === 'citas' ? 'active' : ''}`}
          onClick={() => setActiveTab('citas')}
        >
          📅 Citas
        </button>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Cargando datos...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <Dashboard 
                clientes={clientes} 
                mascotas={mascotas} 
                citas={citas} 
              />
            )}
            {activeTab === 'clientes' && (
              <Clientes 
                clientes={clientes} 
                onReload={loadData} 
              />
            )}
            {activeTab === 'mascotas' && (
              <Mascotas 
                mascotas={mascotas} 
                clientes={clientes}
                onReload={loadData} 
              />
            )}
            {activeTab === 'citas' && (
              <Citas 
                citas={citas} 
                mascotas={mascotas}
                onReload={loadData} 
              />
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>© 2025 Veterinaria PetCare - Sistema de Gestión con Docker</p>
      </footer>
    </div>
  );
}

// ==================== COMPONENTE DASHBOARD ====================
function Dashboard({ clientes, mascotas, citas }) {
  const citasPendientes = citas.filter(c => c.estado === 'Pendiente').length;
  const citasHoy = citas.filter(c => {
    const fecha = new Date(c.fecha_cita);
    const hoy = new Date();
    return fecha.toDateString() === hoy.toDateString();
  }).length;

  return (
    <div className="dashboard">
      <h2 className="section-title">📊 Panel de Control</h2>
      
      <div className="stats-grid">
        <div className="stat-card clientes-card">
          <div className="stat-icon">👥</div>
          <div className="stat-info">
            <h3>{clientes.length}</h3>
            <p>Clientes Registrados</p>
          </div>
        </div>

        <div className="stat-card mascotas-card">
          <div className="stat-icon">🐕</div>
          <div className="stat-info">
            <h3>{mascotas.length}</h3>
            <p>Mascotas Activas</p>
          </div>
        </div>

        <div className="stat-card citas-card">
          <div className="stat-icon">📅</div>
          <div className="stat-info">
            <h3>{citasPendientes}</h3>
            <p>Citas Pendientes</p>
          </div>
        </div>

        <div className="stat-card hoy-card">
          <div className="stat-icon">⏰</div>
          <div className="stat-info">
            <h3>{citasHoy}</h3>
            <p>Citas Hoy</p>
          </div>
        </div>
      </div>

      <div className="recent-section">
        <h3>📋 Próximas Citas</h3>
        <div className="recent-list">
          {citas.slice(0, 5).map(cita => (
            <div key={cita.id} className="recent-item">
              <div className="recent-icon">🐾</div>
              <div className="recent-details">
                <h4>{cita.mascota_nombre} - {cita.cliente_nombre} {cita.cliente_apellido}</h4>
                <p>{new Date(cita.fecha_cita).toLocaleString('es-ES')}</p>
                <span className="motivo">{cita.motivo}</span>
              </div>
              <span className={`status ${cita.estado.toLowerCase()}`}>
                {cita.estado}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ==================== COMPONENTE CLIENTES ====================
function Clientes({ clientes, onReload }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    telefono: '',
    email: '',
    direccion: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/clientes`, formData);
      alert('Cliente registrado exitosamente');
      setShowForm(false);
      setFormData({ nombre: '', apellido: '', telefono: '', email: '', direccion: '' });
      onReload();
    } catch (error) {
      alert('Error al registrar cliente');
    }
  };

  return (
    <div className="section">
      <div className="section-header">
        <h2 className="section-title">👥 Gestión de Clientes</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '❌ Cancelar' : '➕ Nuevo Cliente'}
        </button>
      </div>

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <h3>Registrar Nuevo Cliente</h3>
          <div className="form-grid">
            <input
              type="text"
              placeholder="Nombre *"
              required
              value={formData.nombre}
              onChange={e => setFormData({...formData, nombre: e.target.value})}
            />
            <input
              type="text"
              placeholder="Apellido *"
              required
              value={formData.apellido}
              onChange={e => setFormData({...formData, apellido: e.target.value})}
            />
            <input
              type="tel"
              placeholder="Teléfono"
              value={formData.telefono}
              onChange={e => setFormData({...formData, telefono: e.target.value})}
            />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>
          <textarea
            placeholder="Dirección"
            value={formData.direccion}
            onChange={e => setFormData({...formData, direccion: e.target.value})}
          />
          <button type="submit" className="btn-submit">Guardar Cliente</button>
        </form>
      )}

      <div className="cards-grid">
        {clientes.map(cliente => (
          <div key={cliente.id} className="info-card">
            <div className="card-header">
              <h3>{cliente.nombre} {cliente.apellido}</h3>
            </div>
            <div className="card-body">
              <p>📞 {cliente.telefono || 'No registrado'}</p>
              <p>📧 {cliente.email || 'No registrado'}</p>
              <p>📍 {cliente.direccion || 'No registrada'}</p>
              <p className="date-info">
                Registrado: {new Date(cliente.fecha_registro).toLocaleDateString('es-ES')}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ==================== COMPONENTE MASCOTAS ====================
function Mascotas({ mascotas, clientes, onReload }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nombre: '',
    especie: 'Perro',
    raza: '',
    edad: '',
    peso: '',
    cliente_id: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/mascotas`, {
        ...formData,
        edad: parseInt(formData.edad),
        peso: parseFloat(formData.peso),
        cliente_id: parseInt(formData.cliente_id)
      });
      alert('Mascota registrada exitosamente');
      setShowForm(false);
      setFormData({ nombre: '', especie: 'Perro', raza: '', edad: '', peso: '', cliente_id: '' });
      onReload();
    } catch (error) {
      alert('Error al registrar mascota');
    }
  };

  return (
    <div className="section">
      <div className="section-header">
        <h2 className="section-title">🐕 Gestión de Mascotas</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '❌ Cancelar' : '➕ Nueva Mascota'}
        </button>
      </div>

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <h3>Registrar Nueva Mascota</h3>
          <div className="form-grid">
            <input
              type="text"
              placeholder="Nombre de la mascota *"
              required
              value={formData.nombre}
              onChange={e => setFormData({...formData, nombre: e.target.value})}
            />
            <select
              required
              value={formData.especie}
              onChange={e => setFormData({...formData, especie: e.target.value})}
            >
              <option value="Perro">🐕 Perro</option>
              <option value="Gato">🐈 Gato</option>
              <option value="Ave">🦜 Ave</option>
              <option value="Conejo">🐰 Conejo</option>
              <option value="Otro">🐾 Otro</option>
            </select>
            <input
              type="text"
              placeholder="Raza"
              value={formData.raza}
              onChange={e => setFormData({...formData, raza: e.target.value})}
            />
            <input
              type="number"
              placeholder="Edad (años)"
              value={formData.edad}
              onChange={e => setFormData({...formData, edad: e.target.value})}
            />
            <input
              type="number"
              step="0.1"
              placeholder="Peso (kg)"
              value={formData.peso}
              onChange={e => setFormData({...formData, peso: e.target.value})}
            />
            <select
              required
              value={formData.cliente_id}
              onChange={e => setFormData({...formData, cliente_id: e.target.value})}
            >
              <option value="">Seleccionar Dueño *</option>
              {clientes.map(cliente => (
                <option key={cliente.id} value={cliente.id}>
                  {cliente.nombre} {cliente.apellido}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn-submit">Guardar Mascota</button>
        </form>
      )}

      <div className="cards-grid">
        {mascotas.map(mascota => (
          <div key={mascota.id} className="info-card mascota-card">
            <div className="card-header">
              <h3>
                {mascota.especie === 'Perro' ? '🐕' : 
                 mascota.especie === 'Gato' ? '🐈' : '🐾'} {mascota.nombre}
              </h3>
              <span className="badge">{mascota.especie}</span>
            </div>
            <div className="card-body">
              <p><strong>Raza:</strong> {mascota.raza || 'No especificada'}</p>
              <p><strong>Edad:</strong> {mascota.edad || 'N/A'} años</p>
              <p><strong>Peso:</strong> {mascota.peso || 'N/A'} kg</p>
              <p className="owner-info">
                👤 Dueño: {mascota.cliente_nombre} {mascota.cliente_apellido}
              </p>
              <p>📞 {mascota.cliente_telefono}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ==================== COMPONENTE CITAS ====================
function Citas({ citas, mascotas, onReload }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    mascota_id: '',
    fecha_cita: '',
    motivo: '',
    observaciones: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/citas`, {
        ...formData,
        mascota_id: parseInt(formData.mascota_id)
      });
      alert('Cita agendada exitosamente');
      setShowForm(false);
      setFormData({ mascota_id: '', fecha_cita: '', motivo: '', observaciones: '' });
      onReload();
    } catch (error) {
      alert('Error al agendar cita');
    }
  };

  const updateEstado = async (citaId, nuevoEstado) => {
    try {
      await axios.put(`${API_URL}/citas/${citaId}`, { estado: nuevoEstado });
      alert('Estado actualizado');
      onReload();
    } catch (error) {
      alert('Error al actualizar estado');
    }
  };

  return (
    <div className="section">
      <div className="section-header">
        <h2 className="section-title">📅 Gestión de Citas</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '❌ Cancelar' : '➕ Nueva Cita'}
        </button>
      </div>

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <h3>Agendar Nueva Cita</h3>
          <div className="form-grid">
            <select
              required
              value={formData.mascota_id}
              onChange={e => setFormData({...formData, mascota_id: e.target.value})}
            >
              <option value="">Seleccionar Mascota *</option>
              {mascotas.map(mascota => (
                <option key={mascota.id} value={mascota.id}>
                  {mascota.nombre} ({mascota.especie}) - {mascota.cliente_nombre} {mascota.cliente_apellido}
                </option>
              ))}
            </select>
            <input
              type="datetime-local"
              required
              value={formData.fecha_cita}
              onChange={e => setFormData({...formData, fecha_cita: e.target.value})}
            />
          </div>
          <input
            type="text"
            placeholder="Motivo de la consulta *"
            required
            value={formData.motivo}
            onChange={e => setFormData({...formData, motivo: e.target.value})}
          />
          <textarea
            placeholder="Observaciones adicionales"
            value={formData.observaciones}
            onChange={e => setFormData({...formData, observaciones: e.target.value})}
          />
          <button type="submit" className="btn-submit">Agendar Cita</button>
        </form>
      )}

      <div className="citas-list">
        {citas.map(cita => (
          <div key={cita.id} className="cita-card">
            <div className="cita-header">
              <div>
                <h3>🐾 {cita.mascota_nombre} ({cita.mascota_especie})</h3>
                <p className="cliente-name">
                  👤 {cita.cliente_nombre} {cita.cliente_apellido} | 📞 {cita.cliente_telefono}
                </p>
              </div>
              <span className={`status ${cita.estado.toLowerCase()}`}>
                {cita.estado}
              </span>
            </div>
            <div className="cita-body">
              <p><strong>📅 Fecha:</strong> {new Date(cita.fecha_cita).toLocaleString('es-ES')}</p>
              <p><strong>🩺 Motivo:</strong> {cita.motivo}</p>
              {cita.observaciones && (
                <p><strong>📝 Observaciones:</strong> {cita.observaciones}</p>
              )}
            </div>
            <div className="cita-actions">
              <button 
                className="btn-success" 
                onClick={() => updateEstado(cita.id, 'Completada')}
                disabled={cita.estado === 'Completada'}
              >
                ✅ Completar
              </button>
              <button 
                className="btn-danger" 
                onClick={() => updateEstado(cita.id, 'Cancelada')}
                disabled={cita.estado === 'Cancelada'}
              >
                ❌ Cancelar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
