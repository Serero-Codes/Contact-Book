const apiBase = '/api/contacts';
const form = document.getElementById('contactForm');
const contactsTable = document.getElementById('contactsTable');
const contactsEmpty = document.getElementById('contactsEmpty');
const contactsLoading = document.getElementById('contactsLoading');
const contactsCount = document.getElementById('contactsCount');
const formMessage = document.getElementById('formMessage');
const formTitle = document.getElementById('formTitle');
const submitButton = document.getElementById('submitButton');
const resetButton = document.getElementById('resetForm');

const MONOGRAM_COLORS = ['#2F4B3C', '#B08D3E', '#A44B3F', '#3B4A5A'];

function setMessage(text, type = 'info') {
  formMessage.textContent = text;
  formMessage.className = `message ${type}`;
}


function clearForm() {
  form.reset();
  document.getElementById('contactId').value = '';
  formTitle.textContent = 'New entry';
  submitButton.textContent = 'Save contact';
  setMessage('', 'info');
}

function getInitials(contact) {
  const first = (contact.first_name || '').trim().charAt(0);
  const last = (contact.last_name || '').trim().charAt(0);
  return (first + last).toUpperCase() || '?';
}

function getMonogramColor(contact) {
  const key = `${contact.first_name || ''}${contact.last_name || ''}`;
  let hash = 0;
  for (let i = 0; i < key.length; i++) {
    hash = key.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % MONOGRAM_COLORS.length;
  return MONOGRAM_COLORS[index];
}

async function fetchContacts() {
  contactsLoading.style.display = 'block';
  contactsTable.innerHTML = '';
  contactsEmpty.style.display = 'none';
  contactsCount.textContent = '';
  try {
    const res = await fetch(apiBase);
    const contacts = await res.json();
    contactsLoading.style.display = 'none';
    if (!contacts.length) {
      contactsEmpty.style.display = 'block';
      return;
    }
    contacts.forEach(renderContactRow);
    contactsCount.textContent = contacts.length === 1 ? '1 contact' : `${contacts.length} contacts`;
  } catch (err) {
    contactsLoading.textContent = 'Unable to load contacts.';
    console.error(err);
  }
}

function renderContactRow(contact) {
  const item = document.createElement('li');
  item.className = 'contact-card';
  item.dataset.id = contact.id;

  const email = contact.email ? contact.email : '—';

  item.innerHTML = `
    <div class="contact-tab" style="background:${getMonogramColor(contact)}">${getInitials(contact)}</div>
    <div class="contact-main">
      <p class="contact-name">${contact.first_name} ${contact.last_name}</p>
      <p class="contact-phone">${contact.phone_number}</p>
      <p class="contact-email">${email}</p>
    </div>
    <div class="contact-actions">
      <button type="button" class="text-btn edit" data-id="${contact.id}">Edit</button>
      <button type="button" class="text-btn delete" data-id="${contact.id}">Remove</button>
    </div>
  `;

  contactsTable.appendChild(item);
}

function fillForm(contact) {
  document.getElementById('contactId').value = contact.id;
  document.getElementById('firstName').value = contact.first_name;
  document.getElementById('lastName').value = contact.last_name;
  document.getElementById('phoneNumber').value = contact.phone_number;
  document.getElementById('email').value = contact.email || '';
  formTitle.textContent = 'Editing entry';
  submitButton.textContent = 'Update contact';
  setMessage('Editing contact: ' + contact.first_name + ' ' + contact.last_name, 'info');
}

async function handleSubmit(event) {
  event.preventDefault();
  const id = document.getElementById('contactId').value;
  const payload = {
    first_name: document.getElementById('firstName').value.trim(),
    last_name: document.getElementById('lastName').value.trim(),
    phone_number: document.getElementById('phoneNumber').value.trim(),
    email: document.getElementById('email').value.trim(),
  };

  const method = id ? 'PUT' : 'POST';
  const url = id ? `${apiBase}/${id}` : apiBase;

  try {
    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const result = await res.json();
    if (!res.ok) {
      setMessage(result.error || 'Unable to save contact', 'error');
      return;
    }
    setMessage(id ? 'Contact updated.' : 'Contact added.', 'success');
    clearForm();
    fetchContacts();
  } catch (err) {
    setMessage('Request failed.', 'error');
    console.error(err);
  }
}

async function handleTableClick(event) {
  const button = event.target.closest('button');
  if (!button) return;
  const id = button.dataset.id;

  if (button.classList.contains('edit')) {
    const res = await fetch(`${apiBase}/${id}`);
    if (!res.ok) {
      setMessage('Unable to load contact.', 'error');
      return;
    }
    const contact = await res.json();
    fillForm(contact);
    return;
  }

  if (button.classList.contains('delete')) {
    const row = button.closest('.contact-card');
    const name = row.querySelector('.contact-name')?.textContent || 'this contact';
    if (!confirm(`Remove ${name} from your contacts? This can't be undone.`)) return;

    const res = await fetch(`${apiBase}/${id}`, { method: 'DELETE' });
    const result = await res.json();
    if (!res.ok) {
      setMessage(result.error || 'Unable to delete contact', 'error');
      return;
    }
    setMessage('Contact deleted.', 'success');
    fetchContacts();
  }
}

form.addEventListener('submit', handleSubmit);
resetButton.addEventListener('click', clearForm);
contactsTable.addEventListener('click', handleTableClick);
fetchContacts();