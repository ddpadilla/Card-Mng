const API_BASE_URL = 'https://servertest1.me/api';
const elements = {
  tabs: document.querySelectorAll('.tab-button'),
  panels: document.querySelectorAll('.tab-panel'),
  loading: document.getElementById('loading'),
  message: document.getElementById('message'),
  searchType: document.getElementById('searchType'),
  searchInput: document.getElementById('searchInput'),
  resultadoConsulta: document.getElementById('resultadoConsulta'),
  updateSearchType: document.getElementById('updateSearchType'),
  updateSearchInput: document.getElementById('updateSearchInput'),
  formularioActualizar: document.getElementById('formularioActualizar'),
  registroForm: document.getElementById('registroForm')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeTabs();
  initializeEventListeners();
});

// Functions of TABS and Listeners
function initializeTabs() {
  elements.tabs.forEach(tab => {
    tab.addEventListener('click', () => switchTab(tab.dataset.tab));
  });
}

function switchTab(targetTab) {
  elements.tabs.forEach(tab => tab.classList.toggle('active', tab.dataset.tab === targetTab));
  elements.panels.forEach(panel => panel.classList.toggle('active', panel.id === targetTab));
  hideMessage();
}

function initializeEventListeners() {
  elements.registroForm.addEventListener('submit', handleRegistro);
  elements.searchInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') buscarInformacion(); });
  elements.updateSearchInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') buscarParaActualizar(); });
}

// Functions of Utilities
function showLoading() { elements.loading.classList.remove('hidden'); }
function hideLoading() { elements.loading.classList.add('hidden'); }
function showMessage(text, type = 'success') {
  elements.message.textContent = text;
  elements.message.className = `message ${type}`;
  elements.message.classList.remove('hidden');
  setTimeout(() => hideMessage(), 5000);
}
function hideMessage() { elements.message.classList.add('hidden'); }

// ============== API CALLS ==============
async function apiCall(endpoint, options = {}) {
  try {
    showLoading();
    // No set Content-Type if the body is FormData
    const headers = { 'Accept': 'application/json', ...options.headers };
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: options.method || 'GET',
      headers: headers,
      ...options
    });

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch {
        errorData = { detail: `Error HTTP ${response.status}: ${response.statusText}` };
      }
      const errorMessage = Object.values(errorData).join(' ');
      throw new Error(errorMessage);
    }

    if (response.status === 204) return null;

    return await response.json();

  } catch (error) {
    console.error('API Error:', error);
    showMessage(error.message, 'error');
    throw error;
  } finally {
    hideLoading();
  }
}

// ============== FUNCTIONS OF CONSULTATION ==============
window.buscarInformacion = async function() {
  const searchType = elements.searchType.value;
  const searchValue = elements.searchInput.value.trim();
  if (!searchValue) {
    showMessage('Please enter a value to search', 'error');
    return;
  }
  try {
    const endpoint = searchType === 'user' ? `/user/${searchValue}/` : `/card/${searchValue}/`;
    const data = await apiCall(endpoint);
    mostrarResultado(data);
  } catch (error) {
    elements.resultadoConsulta.classList.add('hidden');
  }
};

function formatDate(isoString) {
  if (!isoString) {
    return 'N/A';
  }
  const date = new Date(isoString);
  // Options for a specific format: Day/Month/Year, Hour:Minutes
  const options = {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  };
  return date.toLocaleString('es-HN', options);
}


function mostrarResultado(data) {
  const html = `
    <div class="info-grid">
      <div class="info-item"><label>ID de Usuario</label><div class="value">${data.id_user || 'N/A'}</div></div>
      <div class="info-item"><label>Nombre Completo</label><div class="value">${data.full_name || 'N/A'}</div></div>
      <div class="info-item"><label>Número de Tarjeta</label><div class="value">${data.card_number || 'N/A'}</div></div>
      <div class="info-item"><label>Estado</label><div class="value state-${data.state || 'inactive'}">${getStateText(data.state)}</div></div>
      <div class="info-item"><label>Placa del Vehículo</label><div class="value">${data.car_plate || 'N/A'}</div></div>
      <div class="info-item"><label>Marca del Vehículo</label><div class="value">${data.brand || 'N/A'}</div></div>
      <div class="info-item"><label>Fecha de Creación</label><div class="value">${formatDate(data.created)}</div></div>
      <div class="info-item"><label>Fecha de Actualización</label><div class="value">${formatDate(data.updated)}</div></div>
      <div class="info-item"><label>Documento</label><div class="value">${data.authorization_document ? `<a href="https://servertest1.me/${data.authorization_document}" target="_blank" class="document-link">📄 Ver Documento</a>` : 'N/A'}</div></div>
    </div>`;
  elements.resultadoConsulta.innerHTML = html;
  elements.resultadoConsulta.classList.remove('hidden');
}

// ============== FUNCTIONS OF UPDATE ==============
window.buscarParaActualizar = async function() {
  const searchType = elements.updateSearchType.value;
  const searchValue = elements.updateSearchInput.value.trim();
  if (!searchValue) {
    showMessage('Please enter a value to search', 'error');
    return;
  }
  try {
    // Use the endpoints of consultation to get the initial data
    const endpoint = searchType === 'user' ? `/user/${searchValue}/` : `/card/${searchValue}/`;
    const data = await apiCall(endpoint);
    mostrarFormularioActualizar(data, searchType, searchValue);
  } catch (error) {
    elements.formularioActualizar.classList.add('hidden');
  }
};

// The function mostrarFormularioActualizar now can have all the fields enabled
function mostrarFormularioActualizar(data, searchType, searchValue) {
  const html = `
    <h3>Actualizar Información para: ${searchValue}</h3>
    <form id="updateForm" class="registro-form">
      
      <div class="form-row">
        <div class="form-group">
          <label for="update_full_name">Nombre Completo</label>
          <input type="text" id="update_full_name" name="full_name" value="${data.full_name || ''}">
        </div>
        
        <div class="form-group">
          <label for="update_state">Estado</label>
          <select id="update_state" name="state">
            <option value="active" ${data.state === 'active' ? 'selected' : ''}>Activa</option>
            <option value="inactive" ${data.state === 'inactive' ? 'selected' : ''}>Inactiva</option>
            <option value="expired" ${data.state === 'expired' ? 'selected' : ''}>Expirada</option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="update_car_plate">Placa del Vehículo</label>
          <input type="text" id="update_car_plate" name="car_plate" value="${data.car_plate || ''}">
        </div>
        
        <div class="form-group">
          <label for="update_brand">Marca del Vehículo</label>
          <input type="text" id="update_brand" name="brand" value="${data.brand || ''}">
        </div>
      </div>

      <button type="button" onclick="actualizarInformacion('${searchType}', '${searchValue}')" class="submit-btn">💾 Guardar Cambios</button>
    </form>`;
  
  elements.formularioActualizar.innerHTML = html;
  elements.formularioActualizar.classList.remove('hidden');
}


window.actualizarInformacion = async function(searchType, searchValue) {
  const endpoint = searchType === 'user' 
    ? `/update/user/${searchValue}/` 
    : `/update/card/${searchValue}/`;
  
  // Collect all the data from the form
  const payload = {
    full_name: document.getElementById('update_full_name').value,
    state: document.getElementById('update_state').value,
    car_plate: document.getElementById('update_car_plate').value,
    brand: document.getElementById('update_brand').value,
  };
  
  console.log(`Sending PUT to ${endpoint} with unified payload:`, payload);

  try {
    // Send the request. The backend will take care of the rest.
    const updatedData = await apiCall(endpoint, {
      method: 'PUT',
      body: JSON.stringify(payload)
    });
    
    showMessage('Success! The information has been updated completely.', 'success');
    
    // Refresh the form with the updated data that the API returns
    mostrarFormularioActualizar(updatedData, searchType, searchValue);
    
  } catch (error) {
    // The error message is already shown in apiCall
    console.error(' Error en actualizarInformacion:', error);
  }
};

// ============== FUNCTIONS OF REGISTRATION ==============
async function handleRegistro(e) {
  e.preventDefault();
  
  // FormData automatically captures all form fields with their names
  const formData = new FormData(elements.registroForm);

  try {
    // Use the improved apiCall helper for consistency
    const data = await apiCall('/register/', {
      method: 'POST',
      body: formData // apiCall sabrá cómo manejar FormData
    });
    
    showMessage('Registro creado exitosamente. ID de Usuario: ' + data.id_user, 'success');
    elements.registroForm.reset();
    
  } catch (error) {
    // The error message is already shown in the apiCall function
    console.error('Registration Error:', error);
  }
}

// ============== UTILITIES ==============
function getStateText(state) {
  const states = { 'active': 'Activa', 'inactive': 'Inactiva', 'expired': 'Expirada' };
  return states[state] || 'Desconocido';
}
