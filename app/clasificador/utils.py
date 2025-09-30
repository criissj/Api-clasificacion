import os, logging
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from openai import OpenAI

# ====== Excel Utils ======
EXCEL_FILE = "consultas_chatbot.xlsx"

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "Consultas"
        ws.append([
            "Fecha", "Correo", "Pregunta", "Respuesta",
            "Tokens Entrada", "Tokens Salida", "Tokens Totales", "Asistente"
        ])
        wb.save(EXCEL_FILE)


def save_to_excel(email, pregunta, respuesta, input_tokens, output_tokens, assistant_name):
    try:
        init_excel()
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb["Consultas"]

        logging.info(f"Guardando en Excel -> Input: {input_tokens}, Output: {output_tokens}, Total: {input_tokens + output_tokens}")

        ws.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            email,
            pregunta,
            respuesta,
            input_tokens,
            output_tokens,
            input_tokens + output_tokens,
            assistant_name
        ])
        wb.save(EXCEL_FILE)
    except Exception as e:
        logging.error(f"Error guardando en Excel: {e}")


# ====== Assistant Utils ======
def get_valid_assistant(client: OpenAI, assistant_id_env, vector_store_id, nombre, instrucciones, model_name):
    """Crea o recupera un asistente"""
    if assistant_id_env:
        try:
            assistant = client.beta.assistants.retrieve(assistant_id_env)
            logging.info(f"✅ Usando assistant existente: {assistant_id_env}")
            return assistant.id
        except Exception as e:
            logging.warning(f"⚠️ No se pudo usar {assistant_id_env}: {e}. Creando uno nuevo...")

    assistant = client.beta.assistants.create(
        name=nombre,
        instructions=instrucciones,
        tools=[{"type": "file_search"}],
        model=model_name,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    logging.info(f"✨ Nuevo assistant creado: {assistant.id}")
    return assistant.id
