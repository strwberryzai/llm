import os

import streamlit as st
from google import genai


st.set_page_config(
    page_title="Asistente de Escritura Automática",
    page_icon="✍️",
    layout="centered",
)

st.title("Asistente de Escritura Automática ✍️")
st.caption("Mejora textos, recibe continuaciones o genera contenido desde cero con Gemini.")

# Permite usar una API Key escrita en la interfaz o definida como variable de entorno.
api_key_entorno = os.getenv("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input(
        "API Key de Gemini",
        value=api_key_entorno,
        type="password",
        help="Puedes obtenerla desde Google AI Studio.",
    )
    st.link_button("Abrir Google AI Studio", "https://aistudio.google.com/")

if not api_key:
    st.info("Ingresa tu API Key de Gemini en la barra lateral para comenzar.")
    st.stop()

try:
    cliente = genai.Client(api_key=api_key)
except Exception as error:
    st.error("No fue posible configurar el cliente de Gemini.")
    st.exception(error)
    st.stop()

opcion = st.radio(
    "Selecciona una función:",
    [
        "Mejorar redacción y ortografía",
        "Sugerir continuación",
        "Escribir un texto desde cero",
    ],
)

prompt = ""
texto_para_validar = ""

if opcion == "Mejorar redacción y ortografía":
    st.subheader("Mejorar redacción y ortografía")

    texto = st.text_area(
        "Pega el texto que deseas mejorar:",
        height=220,
        placeholder="Ejemplo: ola profe le mando mi tarea espero ke este bien...",
    )

    texto_para_validar = texto

    prompt = f"""
Eres un asistente experto de escritura en español.

Corrige la ortografía, gramática, puntuación, claridad y fluidez del texto.
Conserva el significado, la intención y el idioma original.
No agregues explicaciones, comentarios ni títulos.
Devuelve solamente la versión corregida.

Texto:
{texto}
"""

elif opcion == "Sugerir continuación":
    st.subheader("Sugerir continuación")

    texto = st.text_area(
        "Escribe el inicio de tu texto:",
        height=220,
        placeholder="Ejemplo: Cuando abrió la puerta, encontró una carta en el suelo...",
    )

    texto_para_validar = texto

    prompt = f"""
Eres un asistente creativo de escritura.

Continúa el texto proporcionado con un único párrafo coherente.
Mantén el mismo idioma, tono, estilo narrativo, tiempo verbal y contexto.
No repitas el texto inicial.
No agregues títulos ni explicaciones.
Devuelve únicamente la continuación.

Inicio del texto:
{texto}
"""

else:
    st.subheader("Escribir un texto desde cero")

    tema = st.text_input(
        "Tema o instrucción",
        placeholder="Ejemplo: Un correo solicitando vacaciones del 10 al 14 de agosto",
    )

    tono = st.selectbox(
        "Tono",
        [
            "Profesional",
            "Formal",
            "Casual",
            "Amigable",
            "Creativo",
            "Persuasivo",
            "Académico",
        ],
    )

    extension = st.select_slider(
        "Extensión",
        options=["Corta", "Media", "Larga"],
        value="Media",
    )

    texto_para_validar = tema

    prompt = f"""
Eres un asistente experto de escritura en español.

Redacta un texto completo a partir de la siguiente solicitud:
{tema}

Usa un tono {tono.lower()}.
La extensión debe ser {extension.lower()}.
El resultado debe ser claro, coherente, bien estructurado y adecuado para la solicitud.
No agregues explicaciones acerca de cómo escribiste el texto.
Devuelve solamente el texto final.
"""

if st.button("Generar texto ✨", type="primary", use_container_width=True):
    if not texto_para_validar.strip():
        st.warning("Escribe un texto o tema antes de generar una respuesta.")
    else:
        try:
            with st.spinner("Gemini está generando la respuesta..."):
                respuesta = cliente.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )

            resultado = respuesta.text

            st.subheader("Resultado")
            st.text_area(
                "Texto generado",
                value=resultado,
                height=300,
            )

            st.download_button(
                label="Descargar como archivo .txt",
                data=resultado,
                file_name="resultado_asistente_escritura.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as error:
            st.error("Ocurrió un error al comunicarse con Gemini.")
            st.exception(error)
