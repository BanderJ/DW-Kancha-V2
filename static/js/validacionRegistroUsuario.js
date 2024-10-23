document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const nombre = document.getElementById("nombre");
    const nroDoc = document.getElementById("numerodocumento");
    const apePat = document.getElementById("apePat");
    const apeMat = document.getElementById("apeMat");
    const correo = document.getElementById("correo");
    const password = document.getElementById("password");
    const confirmarPassword = document.getElementById("confirmar_password"); // Nuevo campo
    const telefono = document.getElementById("telefono");
    const fechaNacimiento = document.getElementById("fechaNacimiento");
    const sexo = document.getElementById("sexo");
    const tipo_usuario = document.getElementById("tipo_usuario");
    const nivel_usuario = document.getElementById("nivel_usuario");

    const nombreError = document.getElementById("nombreError");
    const nroDocError = document.getElementById("nroDocError");
    const apePatError = document.getElementById("apePatError");
    const apeMatError = document.getElementById("apeMatError");
    const correoError = document.getElementById("correoError");
    const passwordError = document.getElementById("passwordError");
    const confirmarPasswordError = document.getElementById("confirmarPasswordError"); // Nuevo mensaje de error
    const telefonoError = document.getElementById("telefonoError");
    const fechaError = document.getElementById("fechaError");
    const sexoError = document.getElementById("sexoError");
    const tipoUsuError = document.getElementById("tipoUsuError");
    const nivelUsuError = document.getElementById("nivelUsuError");

    const politicas = document.getElementById("politicas");
    const cookies = document.getElementById("cookies");
    const datos = document.getElementById("datos");
    const condiciones = document.getElementById("condiciones");

    // Validaciones al escribir
    nombre.addEventListener("input", () => validateField(nombre, /^[A-Za-z\s]+$/, nombreError, "El nombre solo debe contener letras."));
    nroDoc.addEventListener("input", () => validateDocumentNumber());
    apePat.addEventListener("input", () => validateField(apePat, /^[A-Za-z\s]+$/, apePatError, "El apellido paterno solo debe contener letras."));
    apeMat.addEventListener("input", () => validateField(apeMat, /^[A-Za-z\s]*$/, apeMatError, "El apellido materno solo debe contener letras."));
    correo.addEventListener("input", () => validateField(correo, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, correoError, "Ingrese un correo electrónico válido."));
    password.addEventListener("input", () => validateField(password, /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, passwordError, "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números."));
    confirmarPassword.addEventListener("input", () => validateConfirmPassword());
    telefono.addEventListener("input", () => validatePhone());
    fechaNacimiento.addEventListener("input", () => validateDate());
    sexo.addEventListener("change", () => validateSelect(sexo, sexoError, "Seleccione un sexo."));
    tipo_usuario.addEventListener("change", () => validateSelect(tipo_usuario, tipoUsuError, "Seleccione un tipo de usuario."));
    nivel_usuario.addEventListener("change", () => validateSelect(nivel_usuario, nivelUsuError, "Seleccione un nivel de usuario."));

    // Funciones de validación
    function validateField(field, regex, errorMessageElement, errorMessage) {
        if (regex.test(field.value)) {
            field.classList.remove("error");
            field.classList.add("success");
            errorMessageElement.textContent = "";
            errorMessageElement.style.display = "none";
        } else {
            field.classList.remove("success");
            field.classList.add("error");
            errorMessageElement.textContent = errorMessage;
            errorMessageElement.style.display = "block";
        }
    }

    function validateDocumentNumber() {
        const value = nroDoc.value;
        if (value.length === 8 && /^\d+$/.test(value)) {
            nroDoc.classList.remove("error");
            nroDoc.classList.add("success");
            nroDocError.textContent = "";
            nroDocError.style.display = "none";
        } else {
            nroDoc.classList.remove("success");
            nroDoc.classList.add("error");
            nroDocError.textContent = "El número de documento debe tener 8 dígitos.";
            nroDocError.style.display = "block";
        }
    }

    function validatePhone() {
        const value = telefono.value;
        if (value.length === 9 && /^\d+$/.test(value)) {
            telefono.classList.remove("error");
            telefono.classList.add("success");
            telefonoError.textContent = "";
            telefonoError.style.display = "none";
        } else {
            telefono.classList.remove("success");
            telefono.classList.add("error");
            telefonoError.textContent = "El número de teléfono debe tener 9 dígitos.";
            telefonoError.style.display = "block";
        }
    }

    function validateDate() {
        const selectedDate = new Date(fechaNacimiento.value);
        const today = new Date();
        const age = today.getFullYear() - selectedDate.getFullYear();
        const monthDiff = today.getMonth() - selectedDate.getMonth();
        const isMinor = age < 18 || (age === 18 && monthDiff < 0);
        
        if (isMinor) {
            fechaNacimiento.classList.remove("success");
            fechaNacimiento.classList.add("error");
            fechaError.textContent = "Debes ser mayor de edad.";
            fechaError.style.display = "block";
        } else {
            fechaNacimiento.classList.remove("error");
            fechaNacimiento.classList.add("success");
            fechaError.textContent = "";
            fechaError.style.display = "none";
        }
    }

    function validateSelect(select, errorMessageElement, errorMessage) {
        if (select.value) {
            select.classList.remove("error");
            select.classList.add("success");
            errorMessageElement.textContent = "";
            errorMessageElement.style.display = "none";
        } else {
            select.classList.remove("success");
            select.classList.add("error");
            errorMessageElement.textContent = errorMessage;
            errorMessageElement.style.display = "block";
        }
    }

    function validateConfirmPassword() {
        if (password.value === confirmarPassword.value) {
            confirmarPassword.classList.remove("error");
            confirmarPassword.classList.add("success");
            confirmarPasswordError.textContent = "";
            confirmarPasswordError.style.display = "none";
        } else {
            confirmarPassword.classList.remove("success");
            confirmarPassword.classList.add("error");
            confirmarPasswordError.textContent = "Las contraseñas no coinciden.";
            confirmarPasswordError.style.display = "block";
        }
    }

    function checkCheckButtons() {
        const allChecked = politicas.checked && cookies.checked && datos.checked && condiciones.checked;
        if (allChecked) {
            politicas.classList.remove("error");
            cookies.classList.remove("error");
            datos.classList.remove("error");
            condiciones.classList.remove("error");
        } else {
            politicas.classList.add("error");
            cookies.classList.add("error");
            datos.classList.add("error");
            condiciones.classList.add("error");
        }
        return allChecked;
    }

    // Validar todos los campos antes de enviar
    form.addEventListener("submit", (event) => {
        validateField(nombre, /^[A-Za-z\s]+$/, nombreError, "El nombre solo debe contener letras.");
        validateDocumentNumber();
        validateField(apePat, /^[A-Za-z\s]+$/, apePatError, "El apellido paterno solo debe contener letras.");
        validateField(apeMat, /^[A-Za-z\s]*$/, apeMatError, "El apellido materno solo debe contener letras.");
        validateField(correo, /^[^\s@]+@[^\s@]+\.[^\s@]+$/, correoError, "Ingrese un correo electrónico válido.");
        validateField(password, /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, passwordError, "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números.");
        validateConfirmPassword();
        validatePhone();
        validateDate();
        validateSelect(sexo, sexoError, "Seleccione un sexo.");
        validateSelect(tipo_usuario, tipoUsuError, "Seleccione un tipo de usuario.");
        validateSelect(nivel_usuario, nivelUsuError, "Seleccione un nivel de usuario.");
        
        // Verificar si los checkbuttons están seleccionados
        if (!checkCheckButtons()) {
            event.preventDefault(); // Evitar el envío del formulario si no están todos seleccionados
        }
        
        // Si hay algún error, evitar que se envíe el formulario
        if (form.querySelector(".error")) {
            event.preventDefault();
        }
    });
});
