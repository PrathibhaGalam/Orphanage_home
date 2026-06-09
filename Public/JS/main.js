// Basic UI interactions for homepage
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modalContent');
const openLogin = document.getElementById('openLogin');
const openRegister = document.getElementById('openRegister');
const openHomeRegister = document.getElementById('openHomeRegister');
const closeModal = document.getElementById('closeModal');
const searchBtn = document.getElementById('searchBtn');
const searchInput = document.getElementById('searchInput');
const geoBtn = document.getElementById('geoBtn');
const cardsEl = document.getElementById('cards');
const actionsEl = document.querySelector('.actions');

// storage helpers
function getUsers(){ return JSON.parse(localStorage.getItem('hn_users')||'[]'); }
function saveUsers(u){ localStorage.setItem('hn_users', JSON.stringify(u)); }
function getHomes(){ return JSON.parse(localStorage.getItem('hn_homes')||'[]'); }
function saveHomes(h){ localStorage.setItem('hn_homes', JSON.stringify(h)); }
function setCurrentUser(email){ localStorage.setItem('hn_current', email); renderUserStatus(); }
function getCurrentUser(){ return localStorage.getItem('hn_current'); }

function renderUserStatus(){
  const email = getCurrentUser();
  if(!actionsEl) return;
  if(email){
    const users = getUsers();
    const u = users.find(x=>x.email===email);
    actionsEl.innerHTML = `<span style="margin-right:12px">Hi, ${u?u.name:email}</span><button class="btn ghost" id="logoutBtn">Logout</button>`;
    document.getElementById('logoutBtn').addEventListener('click', ()=>{ localStorage.removeItem('hn_current'); renderUserStatus(); });
  } else {
    actionsEl.innerHTML = `<button class="btn ghost" id="openLogin">Login</button><button class="btn primary" id="openRegister">Sign Up</button>`;
    // rebind
    const newOpenLogin = document.getElementById('openLogin');
    const newOpenRegister = document.getElementById('openRegister');
    if(newOpenLogin) newOpenLogin.addEventListener('click', openLoginHandler);
    if(newOpenRegister) newOpenRegister.addEventListener('click', openRegisterHandler);
  }
}

function showModal(html){ 
  if(!modal || !modalContent) { alert('Modal not available on this page'); return; }
  modalContent.innerHTML = html; 
  modal.classList.remove('hidden'); 
}
function hideModal(){ 
  if(modal) modal.classList.add('hidden'); 
}

function openLoginHandler(){
  showModal(`
    <h2>Login</h2>
    <form id="loginForm">
      <label>Email</label>
      <input type="email" id="loginEmail" required/>
      <label>Password</label>
      <input type="password" id="loginPass" required/>
      <div style="margin-top:12px;display:flex;gap:8px;justify-content:flex-end">
        <button type="button" class="btn ghost" id="cancelLogin">Cancel</button>
        <button type="submit" class="btn primary">Login</button>
      </div>
    </form>
  `);
  document.getElementById('cancelLogin').addEventListener('click', hideModal);
  document.getElementById('loginForm').addEventListener('submit', (e)=>{
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const pass = document.getElementById('loginPass').value;
    const users = getUsers();
    const u = users.find(x=>x.email.toLowerCase()===email.toLowerCase() && x.password===pass);
    if(u){ setCurrentUser(u.email); alert('Logged in as '+u.name); hideModal(); }
    else { alert('Invalid credentials. If you are new, please Sign Up.'); }
  });
}

function openRegisterHandler(){
  showModal(`
    <h2>Sign Up</h2>
    <form id="regForm">
      <label>Name</label>
      <input id="regName" required />
      <label>Email</label>
      <input type="email" id="regEmail" required />
      <label>Password</label>
      <input type="password" id="regPass" required />
      <label>Are you a helper or a home?</label>
      <select id="regType"><option>Helper</option><option>Home</option></select>
      <div style="margin-top:12px;display:flex;gap:8px;justify-content:flex-end">
        <button type="button" class="btn ghost" id="cancelReg">Cancel</button>
        <button type="submit" class="btn primary">Create account</button>
      </div>
    </form>
  `);
  document.getElementById('cancelReg').addEventListener('click', hideModal);
  document.getElementById('regForm').addEventListener('submit', (e)=>{
    e.preventDefault();
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const pass = document.getElementById('regPass').value;
    const type = document.getElementById('regType').value;
    const users = getUsers();
    if(users.find(u=>u.email.toLowerCase()===email.toLowerCase())){ alert('Email already registered'); return; }
    users.push({name, email, password: pass, type});
    saveUsers(users);
    setCurrentUser(email);
    alert('Account created — welcome, '+name);
    hideModal();
  });
}

openLogin?.addEventListener('click', openLoginHandler);
openRegister?.addEventListener('click', openRegisterHandler);
if(openHomeRegister) openHomeRegister.addEventListener('click', openHomeRegisterHandler);

if(closeModal) closeModal.addEventListener('click', hideModal);
if(modal) modal.addEventListener('click', (e)=>{ if(e.target===modal) hideModal(); });

// Ensure event listeners are re-attached after DOM ready
if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', ()=>{
    renderUserStatus();
  });
} else {
  renderUserStatus();
}

// Simple search filtering over static cards
function filterCards(query){
  if(!cardsEl) return;
  const q = query.trim().toLowerCase();
  const cards = Array.from(cardsEl.querySelectorAll('.card'));
  cards.forEach(card=>{
    const city = (card.dataset.city||'').toLowerCase();
    const needs = (card.dataset.needs||'').toLowerCase();
    const name = card.querySelector('h3').textContent.toLowerCase();
    const match = [city,needs,name].some(s=>s.includes(q));
    card.style.display = (match || q==='') ? '' : 'none';
  });
}

if(searchBtn) searchBtn.addEventListener('click', ()=>filterCards(searchInput.value));
if(searchInput) searchInput.addEventListener('keyup', (e)=>{ if(e.key === 'Enter') filterCards(searchInput.value); });

if(geoBtn) geoBtn.addEventListener('click', ()=>{
  if(!navigator.geolocation){ alert('Geolocation not supported'); return; }
  geoBtn.disabled = true;
  geoBtn.textContent = 'Locating...';
  navigator.geolocation.getCurrentPosition(pos=>{
    geoBtn.textContent = 'Use my location';
    geoBtn.disabled = false;
    // Demo: in a real app we'd call backend to find nearby homes by coords
    alert('Location found. In this demo, search will still filter by keywords.');
  }, err=>{
    geoBtn.disabled = false;geoBtn.textContent='Use my location';alert('Unable to get location');
  });
});

// initialize (show all)
filterCards('');

// render homes from storage (append to existing sample cards)
function addCard(home){
  const art = document.createElement('article'); art.className='card';
  art.dataset.city = home.city || '';
  art.dataset.needs = (home.needs||'').toString();
  art.dataset.distance = home.distance || '';
  art.innerHTML = `
    <img src="${home.images && home.images[0] ? home.images[0] : 'images/orphanimg.svg'}" alt="${home.name}" />
    <div class="card-body">
      <h3>${home.name}</h3>
      <p class="muted">${home.city}${home.country ? ', '+home.country : ''} ${home.distance? '— '+home.distance+' km':''}</p>
      <p class="needs"><strong>Needs:</strong> ${home.needs}</p>
      <div class="card-actions">
        <a class="btn ghost" href="orphanage-detail.html?id=${home.id}">View</a>
        <a class="btn primary" href="orphanage-detail.html?id=${home.id}">Donate</a>
      </div>
    </div>
  `;
  cardsEl.appendChild(art);
}

function openHomeRegisterHandler(){
  showModal(`
    <h2>Register Your Home</h2>
    <form id="homeRegForm" style="max-height:600px;overflow-y:auto;">
      <label>Home name</label>
      <input id="homeName" required />
      <label>Address</label>
      <input id="homeAddress" required />
      <label>City</label>
      <input id="homeCity" required />
      <label>Country</label>
      <input id="homeCountry" required />
      <label>Latitude</label>
      <input id="homeLat" type="number" step="any" placeholder="e.g. 40.7128" required />
      <label>Longitude</label>
      <input id="homeLng" type="number" step="any" placeholder="e.g. -74.0060" required />
      <button type="button" class="btn ghost" id="geoFindBtn" style="width:100%;margin-bottom:8px;">📍 Get My Location</button>
      <label>Phone</label>
      <input id="homePhone" required />
      
      <label style="margin-top:15px;"><strong>Add Your Needs</strong></label>
      <div id="needsContainer" style="margin-bottom:12px;"></div>
      <button type="button" class="btn ghost" id="addNeedBtn" style="width:100%;margin-bottom:12px;">+ Add Another Need</button>
      
      <label>Photos</label>
      <input id="homePhotos" type="file" accept="image/*" multiple />
      <div id="preview" style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap"></div>
      <div style="margin-top:12px;display:flex;gap:8px;justify-content:flex-end">
        <button type="button" class="btn ghost" id="cancelHomeReg">Cancel</button>
        <button type="submit" class="btn primary">Register Home</button>
      </div>
    </form>
  `);
  
  let needCount = 0;
  const needsContainer = document.getElementById('needsContainer');
  
  function addNeedField(){
    needCount++;
    const needField = document.createElement('div');
    needField.id = 'need-field-' + needCount;
    needField.style.cssText = 'border:1px solid #ccc;padding:10px;margin-bottom:10px;border-radius:6px;background:#f9f9f9;';
    needField.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
        <select class="need-type" required style="padding:8px;border:1px solid #ddd;border-radius:4px;">
          <option value="">Select Need Type</option>
          <option value="Food">🍲 Food</option>
          <option value="Clothes">👕 Clothes</option>
          <option value="Medicine">💊 Medicine</option>
          <option value="Books">📚 Books</option>
          <option value="Beds">🛏️ Beds</option>
          <option value="Water">💧 Water</option>
          <option value="Education">🎓 Education</option>
          <option value="Supplies">📦 Supplies</option>
          <option value="Other">🎁 Other</option>
        </select>
        <input type="text" class="need-unit" placeholder="Unit (kg, liters, etc)" style="padding:8px;border:1px solid #ddd;border-radius:4px;" />
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
        <input type="number" class="need-quantity" placeholder="Quantity needed" min="0" step="any" required style="padding:8px;border:1px solid #ddd;border-radius:4px;" />
        <input type="number" class="need-cost" placeholder="Cost per unit ($)" min="0" step="0.01" required style="padding:8px;border:1px solid #ddd;border-radius:4px;" />
      </div>
      <button type="button" class="btn ghost" style="width:100%;padding:6px;" onclick="document.getElementById('need-field-${needCount}').remove();">Remove</button>
    `;
    needsContainer.appendChild(needField);
  }
  
  document.getElementById('addNeedBtn').addEventListener('click', (e) => {
    e.preventDefault();
    addNeedField();
  });
  
  addNeedField(); // Start with one field
  
  document.getElementById('cancelHomeReg').addEventListener('click', hideModal);
  
  // Geolocation button
  document.getElementById('geoFindBtn').addEventListener('click', ()=>{
    if(!navigator.geolocation){ alert('Geolocation not supported'); return; }
    const btn = document.getElementById('geoFindBtn');
    btn.disabled = true; btn.textContent = '📍 Locating...';
    navigator.geolocation.getCurrentPosition(pos=>{
      document.getElementById('homeLat').value = pos.coords.latitude.toFixed(6);
      document.getElementById('homeLng').value = pos.coords.longitude.toFixed(6);
      btn.disabled = false; btn.textContent = '📍 Location Updated';
    }, err=>{
      btn.disabled = false; btn.textContent = '📍 Get My Location'; alert('Unable to get location');
    });
  });
  
  const photosInput = document.getElementById('homePhotos');
  const preview = document.getElementById('preview');
  photosInput.addEventListener('change', (e)=>{
    preview.innerHTML='';
    Array.from(e.target.files).slice(0,4).forEach(file=>{
      const r = new FileReader(); r.onload = ()=>{
        const img = document.createElement('img'); img.src = r.result; img.style.width='96px'; img.style.height='64px'; img.style.objectFit='cover'; img.style.borderRadius='6px'; preview.appendChild(img);
      }; r.readAsDataURL(file);
    });
  });
  
  document.getElementById('homeRegForm').addEventListener('submit', (e)=>{
    e.preventDefault();
    const name = document.getElementById('homeName').value.trim();
    const address = document.getElementById('homeAddress').value.trim();
    const city = document.getElementById('homeCity').value.trim();
    const country = document.getElementById('homeCountry').value.trim();
    const lat = parseFloat(document.getElementById('homeLat').value);
    const lng = parseFloat(document.getElementById('homeLng').value);
    const phone = document.getElementById('homePhone').value.trim();
    const files = Array.from(document.getElementById('homePhotos').files).slice(0,4);
    
    // Collect structured needs
    const structuredNeeds = [];
    document.querySelectorAll('#needsContainer > div').forEach((field, idx) => {
      const type = field.querySelector('.need-type').value;
      const quantity = parseFloat(field.querySelector('.need-quantity').value);
      const unit = field.querySelector('.need-unit').value;
      const costPerUnit = parseFloat(field.querySelector('.need-cost').value);
      if(type && !isNaN(quantity) && !isNaN(costPerUnit)){
        structuredNeeds.push({ id: Date.now() + idx, type, quantity, unit, costPerUnit });
      }
    });
    
    if(!name||!city||!country||isNaN(lat)||isNaN(lng)){ alert('Please provide all required fields including location'); return; }
    if(structuredNeeds.length === 0){ alert('Please add at least one need'); return; }
    
    // Create comma-separated string for backwards compatibility
    const needs = structuredNeeds.map(n => n.type).join(', ');
    
    // read files and save dataURLs
    const readers = files.map(f=>{
      return new Promise(res=>{ const r = new FileReader(); r.onload=()=>res(r.result); r.readAsDataURL(f); });
    });
    Promise.all(readers).then(images=>{
      const homes = getHomes();
      const home = { id: Date.now(), name, address, city, country, lat, lng, phone, needs, structuredNeeds, images, distance: 0 };
      homes.push(home); saveHomes(homes); addCard(home); addMarkerToMap(home); hideModal(); alert('Home registered — thank you!');
    }).catch(()=>{ alert('Error reading files'); });
  });
}

// load saved homes and render
let map; // global map instance
function initializeMap(){
  if(document.getElementById('map')){
    map = L.map('map').setView([20, 0], 2); // World view
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(map);
  }
}
function addMarkerToMap(home){
  if(!map || !home.lat || !home.lng) return;
  const marker = L.marker([home.lat, home.lng]).addTo(map);
  const popupText = `<strong>${home.name}</strong><br/>${home.city}, ${home.country}<br/><small>${home.needs}</small>`;
  marker.bindPopup(popupText);
}
let currentHomes = [];

function loadAllHomesOnMap(){
  const saved = getHomes();
  const allHomes = [
    ...currentHomes.filter(h=>h && h.lat && h.lng),
    ...(saved || []).filter(h=>h && h.lat && h.lng)
  ];
  if(allHomes.length){
    allHomes.forEach(h=> addMarkerToMap(h));
    const bounds = L.latLngBounds(allHomes.map(h=>[h.lat, h.lng]));
    if(map && bounds.isValid()) map.fitBounds(bounds.pad(0.1));
  }
}

function loadOrphanagesFromBackend(){
  fetch('/api/orphanages')
    .then(res => res.json())
    .then(result => {
      if(result.success && Array.isArray(result.data)){
        currentHomes = result.data.map(o => ({
          id: o.id,
          name: o.name,
          city: o.city || '',
          country: o.state || '',
          needs: o.needs || 'Needs available on details',
          lat: o.latitude,
          lng: o.longitude,
          distance: o.distance || '',
          images: []
        }));
        if(cardsEl) cardsEl.innerHTML = '';
        currentHomes.forEach(home => addCard(home));
        loadAllHomesOnMap();
      } else {
        console.error('API response error', result);
      }
    })
    .catch(err => console.error('Failed to load orphanages from backend', err));
}

// Initialize map when page loads
window.addEventListener('load', ()=>{
  initializeMap();
  loadOrphanagesFromBackend();
});

// show user status on load
renderUserStatus();
