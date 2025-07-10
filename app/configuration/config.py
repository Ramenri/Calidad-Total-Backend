import os 

class Config:
    DOCUMENTS_PATH = os.environ.get("DOCUMENTOS_PATH", os.path.join(os.getcwd(), "archivos"))