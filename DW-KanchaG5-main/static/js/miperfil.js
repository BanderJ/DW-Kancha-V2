const fields = ['nom', 'ape', 'email', 'doc', 'fechan', 'genero', 'movil'];

document.addEventListener("DOMContentLoaded", () => {
    loadProfile();
});

function toggleEditSave() {
    const isEditing = document.getElementById('edit-save-btn').innerText === 'Guardar cambios';

    if (isEditing) {
        if (validateForm()) {
            saveChanges();
        }
    } else {
        enableEditing();
    }
}

function enableEditing() {
    fields.forEach(field => {
        document.getElementById(field).disabled = false;
    });
    document.getElementById('page-title').innerText = 'Editar mi perfil';
    document.getElementById('edit-save-btn').innerText = 'Guardar cambios';
}

function saveChanges() {
    const userData = {};

    fields.forEach(field => {
        userData[field] = document.getElementById(field).value;
        document.getElementById(field).disabled = true;
        document.getElementById(field).classList.remove('invalid-field');
    });

    localStorage.setItem('userProfile', JSON.stringify(userData));

    document.getElementById('page-title').innerText = 'Mi perfil';
    document.getElementById('edit-save-btn').innerText = 'Editar perfil';
}

function loadProfile() {
    const userData = JSON.parse(localStorage.getItem('userProfile'));

    if (userData) {
        fields.forEach(field => {
            document.getElementById(field).value = userData[field];
        });
    } else {
        const defaultData = {
            nom: "Usuario",
            ape: "lastUsuario",
            email: "usuario@gmail.com",
            doc: "87654321",
            fechan: "2004-08-11",
            genero: "masculino",
            movil: "971133030"
        };
        
        fields.forEach(field => {
            document.getElementById(field).value = defaultData[field];
        });

        localStorage.setItem('userProfile', JSON.stringify(defaultData));
    }
}

function validateForm() {
    let isValid = true;

    fields.forEach(field => {
        const inputElement = document.getElementById(field);
        const fieldValue = inputElement.value.trim();

        if (field === 'email') {
            if (!validateEmail(fieldValue)) {
                isValid = false;
                inputElement.classList.add('invalid-field');
            } else {
                inputElement.classList.remove('invalid-field');
            }
        } else if (field === 'movil') {
            if (!validatePhoneNumber(fieldValue)) {
                isValid = false;
                inputElement.classList.add('invalid-field');
            } else {
                inputElement.classList.remove('invalid-field');
            }
        } else {
            if (fieldValue === '') {
                isValid = false;
                inputElement.classList.add('invalid-field');
            } else {
                inputElement.classList.remove('invalid-field');
            }
        }
    });

    return isValid;
}

function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

function validatePhoneNumber(phoneNumber) {
    const phonePattern = /^[0-9]{9}$/;
    return phonePattern.test(phoneNumber);
}
