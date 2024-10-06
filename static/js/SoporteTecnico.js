let btn_chatbot = document.getElementById("chatbot");
let elemento_chat = document.getElementById("chat");
let mensajes = document.getElementById("ctn_conversacion");

function crearMensaje(contenido) {
    let msg = document.createElement("li");
    msg.innerHTML = contenido;
    msg.classList.add("mensaje");
    mensajes.appendChild(msg);
}

let cont = 0;

function consultarDeNuevo(content, numer) {
    let msg = document.createElement("button");
    msg.innerHTML = content;
    msg.classList.add("repetir_nuevamente");
    msg.dataset.id = numer;
    mensajes.appendChild(msg);

    msg.addEventListener('click', () => {
        msg.disabled = false
        console.log("habilitado")
        let msgs = document.querySelectorAll(".mensaje")
        msgs.forEach(element => {
            mensajes.removeChild(element)
        });

        let user_responses = document.querySelectorAll(".eleccion_usuario")
        user_responses.forEach(elem => {
            mensajes.removeChild(elem)
        });

        msg.style.display="none"

        cont = 0
        while (cont % 2 === 0) {
            ejecutarChatBot()
            cont++
        }
    })
}

function crearOpciones(contenido, num) {
    let msg = document.createElement("button");
    msg.innerHTML = contenido;
    msg.classList.add("eleccion_usuario");
    msg.dataset.id = num;
    mensajes.appendChild(msg);

    msg.addEventListener('click', () => {
        let id_mensaje = msg.dataset.id;
        let botones = document.querySelectorAll(".eleccion_usuario")
        botones.forEach(btn => {
            btn.disabled = true
        });
        console.log(id_mensaje);

        switch (id_mensaje) {
            case '1':
                crearMensaje("1) Ve al menu principal </br> 2) Dirijase al final de la página</br> 3) Ubique la opcion kancha club dentro del apartado productos</br> 4) Presione en unirme </br> 5) Completelos datos </br> 6)Listo")
                consultarDeNuevo("Preguntar de nuevo", 4)
                break;
            case '2':
                crearMensaje("1) Ve al menu principal </br> 2) Dirijase al final de la página </br> 3) Ubique la opcion Devoluciones dentro del apartado de asistencia</br> 4) Continue con los pasos que se brinda en esa pagina")
                consultarDeNuevo("Preguntar de nuevo", 4)
                break;
            case '3':
                crearMensaje("Para poder ponerse en contacto con nuestro personal de soporte por favor llame al siguiente número: +51 987 654 321")
                consultarDeNuevo("Preguntar de nuevo", 4)
                break;
            default:
                crearMensaje("Ha ocurrido un error :(")
        }
    });
}

function ejecutarChatBot() {
    if (cont % 2 === 0) {
        elemento_chat.style.display = "flex";

        setTimeout(() => {
            crearMensaje("Hola Soy KanchaBot ¿En qué puedo ayudarte?");
        }, 1000);

        setTimeout(() => {
            crearOpciones("Unirse a Kancha Club", 1);
            crearOpciones("Hacer reembolso", 2);
            crearOpciones("Realizar consulta vía telefónica", 3);
        }, 2000);
    } else {
        window.location.reload();
    }
}

btn_chatbot.addEventListener('click', () => {
    ejecutarChatBot()
    cont++;
});