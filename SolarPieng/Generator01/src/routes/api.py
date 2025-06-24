from flask import Blueprint, request, jsonify, send_file
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from src.utils.calculator import SolarCalculator, QuickQuoteGenerator
from src.utils.data_extractor import DataExtractor
from src.utils.html_generator import ProposalHTMLGenerator

# Criar blueprint para as rotas da API
api_bp = Blueprint('api', __name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Garantir que as pastas existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@api_bp.route('/upload-ocr', methods=['POST'])
def upload_and_extract():
    """
    Endpoint para upload de arquivo e extração de dados via OCR.
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            # Extrair dados usando o DataExtractor
            extractor = DataExtractor()
            extracted_systems = extractor.extract_systems_from_file(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'systems_extracted': len(extracted_systems),
                'systems_data': extracted_systems
            })
        
        return jsonify({'error': 'Tipo de arquivo não permitido'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Erro no processamento: {str(e)}'}), 500

@api_bp.route('/calculate-proposal', methods=['POST'])
def calculate_proposal():
    """
    Endpoint para calcular proposta baseada nos dados dos kits.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Extrair dados do request
        client_data = data.get('client_data', {})
        systems_data = data.get('systems_data', [])
        parameters = data.get('parameters', {})
        
        if not systems_data:
            return jsonify({'error': 'Nenhum sistema fornecido'}), 400
        
        # Inicializar calculadora
        calculator = SolarCalculator()
        
        # Calcular propostas para todos os sistemas
        proposals = calculator.compare_systems(systems_data, parameters)
        
        return jsonify({
            'success': True,
            'client_data': client_data,
            'proposals': proposals,
            'parameters_used': parameters
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no cálculo: {str(e)}'}), 500

@api_bp.route('/quick-quote', methods=['POST'])
def generate_quick_quote():
    """
    Endpoint para gerar orçamento rápido baseado no consumo.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Extrair parâmetros
        monthly_consumption = data.get('monthly_consumption_kwh')
        bill_value = data.get('bill_value')
        hsp = data.get('hsp', 5.25)
        tariff = data.get('tariff', 1.10)
        simultaneity_factor = data.get('simultaneity_factor', 30)
        
        if not monthly_consumption and not bill_value:
            return jsonify({'error': 'Deve fornecer consumo mensal ou valor da conta'}), 400
        
        # Inicializar gerador de orçamento rápido
        quick_generator = QuickQuoteGenerator('data/components_db.json')
        
        # Gerar orçamento
        proposal = quick_generator.generate_quick_quote(
            monthly_consumption_kwh=monthly_consumption,
            bill_value=bill_value,
            hsp=hsp,
            tariff=tariff,
            simultaneity_factor=simultaneity_factor
        )
        
        return jsonify({
            'success': True,
            'proposal': proposal
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no orçamento rápido: {str(e)}'}), 500

@api_bp.route('/generate-html', methods=['POST'])
def generate_html_proposal():
    """
    Endpoint para gerar proposta HTML.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Extrair dados
        proposals = data.get('proposals', [])
        client_data = data.get('client_data', {})
        format_type = data.get('format', 'standard')  # 'standard' ou 'analytical'
        
        if not proposals:
            return jsonify({'error': 'Nenhuma proposta fornecida'}), 400
        
        # Inicializar gerador HTML
        html_generator = ProposalHTMLGenerator(
            branding_path='data/branding.json'
        )
        
        # Gerar nome do arquivo
        client_name = client_data.get('name', 'Cliente')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proposta_{client_name.replace(' ', '_')}_{format_type}_{timestamp}.html"
        output_path = os.path.join(OUTPUT_FOLDER, filename)
        
        # Gerar HTML baseado no formato
        if format_type == 'analytical':
            html_content = html_generator.generate_analytical_proposal(
                proposals, client_data, output_path
            )
        else:
            html_content = html_generator.generate_standard_proposal(
                proposals, client_data, output_path
            )
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_path': output_path,
            'download_url': f'/api/download/{filename}'
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro na geração HTML: {str(e)}'}), 500

@api_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Endpoint para download de arquivos gerados.
    """
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/html'
        )
    
    except Exception as e:
        return jsonify({'error': f'Erro no download: {str(e)}'}), 500

@api_bp.route('/components', methods=['GET'])
def get_components():
    """
    Endpoint para obter lista de componentes disponíveis.
    """
    try:
        with open('data/components_db.json', 'r', encoding='utf-8') as f:
            components = json.load(f)
        
        return jsonify({
            'success': True,
            'components': components
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao carregar componentes: {str(e)}'}), 500

@api_bp.route('/config', methods=['GET'])
def get_config():
    """
    Endpoint para obter configurações da aplicação.
    """
    try:
        config = {}
        
        # Carregar configurações principais
        if os.path.exists('data/config.json'):
            with open('data/config.json', 'r', encoding='utf-8') as f:
                config.update(json.load(f))
        
        # Carregar branding
        if os.path.exists('data/branding.json'):
            with open('data/branding.json', 'r', encoding='utf-8') as f:
                config['branding'] = json.load(f)
        
        return jsonify({
            'success': True,
            'config': config
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro ao carregar configurações: {str(e)}'}), 500

@api_bp.route('/test-calculation', methods=['POST'])
def test_calculation():
    """
    Endpoint para testar cálculos com dados de exemplo.
    """
    try:
        # Dados de teste
        test_system = {
            'name': 'Sistema Teste',
            'vcusto_raw': 50000.00,
            'power': 50.0,
            'modules_count': 84,
            'modules_desc': '84x Painel Solar 600Wp',
            'inverter_desc': 'Inversor String 50kW',
            'inverter_type': 'string',
            'freight_included': True,
            'freight_value': 0
        }
        
        calculator = SolarCalculator()
        proposal = calculator.calculate_system_proposal(test_system)
        
        return jsonify({
            'success': True,
            'test_proposal': proposal
        })
    
    except Exception as e:
        return jsonify({'error': f'Erro no teste: {str(e)}'}), 500

