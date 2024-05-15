import os
from main import app as application

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Verifica se a variável de ambiente PORT está definida
    application.run_server(host='0.0.0.0', port=port, debug=True)
