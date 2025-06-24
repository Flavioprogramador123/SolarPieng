@echo off
chcp 65001 >nul
title PIENG Solar Generator - Teste
color 0D

echo.
echo ========================================
echo    PIENG SOLAR GENERATOR - TESTE
echo ========================================
echo.

echo [INFO] Iniciando testes da aplicação...
echo.

echo ========================================
echo 1. TESTE DE INSTALAÇÃO
echo ========================================

if not exist venv (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Execute: instalador.bat
    pause
    exit /b 1
)

if not exist src\main.py (
    echo [ERRO] Aplicação não encontrada!
    pause
    exit /b 1
)

echo [OK] Instalação verificada!

echo.
echo ========================================
echo 2. TESTE DO AMBIENTE VIRTUAL
echo ========================================

echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [INFO] Verificando dependências críticas...

python -c "import flask; print('[OK] Flask:', flask.__version__)" 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Flask não encontrado!
    echo Execute: instalador.bat
    pause
    exit /b 1
)

python -c "import json; print('[OK] JSON nativo')" 2>&1
python -c "import os; print('[OK] OS nativo')" 2>&1

echo.
echo ========================================
echo 3. TESTE DOS MÓDULOS PRINCIPAIS
echo ========================================

echo [INFO] Testando módulo de cálculo...
python -c "from src.utils.calculator import SolarCalculator; calc = SolarCalculator(); print('[OK] Calculator carregado')" 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Módulo de cálculo com problemas!
)

echo [INFO] Testando gerador HTML...
python -c "from src.utils.html_generator import ProposalHTMLGenerator; gen = ProposalHTMLGenerator(); print('[OK] HTML Generator carregado')" 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Gerador HTML com problemas!
)

echo [INFO] Testando extrator de dados...
python -c "from src.utils.data_extractor import DataExtractor; ext = DataExtractor(); print('[OK] Data Extractor carregado')" 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Data Extractor com problemas - OCR pode não funcionar
)

echo.
echo ========================================
echo 4. TESTE DE CÁLCULO
echo ========================================

echo [INFO] Executando teste de cálculo...
python -c "
from src.utils.calculator import SolarCalculator
calc = SolarCalculator()
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
result = calc.calculate_system_proposal(test_system)
print('[OK] Cálculo executado com sucesso!')
print(f'Preço final: R$ {result[\"pricing\"][\"final_price\"]:,.2f}')
print(f'Payback: {result[\"calculations\"][\"final_payback_months\"]:.1f} meses')
" 2>&1

if %errorlevel% neq 0 (
    echo [ERRO] Teste de cálculo falhou!
)

echo.
echo ========================================
echo 5. TESTE DE ORÇAMENTO RÁPIDO
echo ========================================

echo [INFO] Testando orçamento rápido...
python -c "
from src.utils.calculator import QuickQuoteGenerator
try:
    quick_gen = QuickQuoteGenerator('data/components_db.json')
    result = quick_gen.generate_quick_quote(monthly_consumption_kwh=500)
    print('[OK] Orçamento rápido executado!')
    print(f'Potência calculada: {result[\"kit_info\"][\"power\"]:.2f} kWp')
    print(f'Preço: R$ {result[\"pricing\"][\"final_price\"]:,.2f}')
except Exception as e:
    print(f'[ERRO] Orçamento rápido falhou: {e}')
" 2>&1

echo.
echo ========================================
echo 6. TESTE DE GERAÇÃO HTML
echo ========================================

echo [INFO] Testando geração de HTML...
python -c "
from src.utils.html_generator import ProposalHTMLGenerator
from src.utils.calculator import SolarCalculator

# Criar dados de teste
calc = SolarCalculator()
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

proposal = calc.calculate_system_proposal(test_system)
proposals = [proposal]
client_data = {'name': 'Cliente Teste'}

# Testar geração HTML
html_gen = ProposalHTMLGenerator()
html_content = html_gen.generate_standard_proposal(proposals, client_data)

if len(html_content) > 1000:
    print('[OK] HTML gerado com sucesso!')
    print(f'Tamanho do HTML: {len(html_content)} caracteres')
else:
    print('[ERRO] HTML muito pequeno ou vazio')
" 2>&1

if %errorlevel% neq 0 (
    echo [ERRO] Teste de HTML falhou!
)

echo.
echo ========================================
echo 7. TESTE DE SERVIDOR (RÁPIDO)
echo ========================================

echo [INFO] Testando inicialização do servidor...
echo [INFO] Iniciando servidor em modo teste (5 segundos)...

timeout /t 2 /nobreak >nul

start /b python src\main.py >nul 2>&1

echo [INFO] Aguardando inicialização...
timeout /t 3 /nobreak >nul

echo [INFO] Testando endpoint de saúde...
python -c "
import requests
import time
try:
    response = requests.get('http://localhost:5000/api/health', timeout=2)
    if response.status_code == 200:
        print('[OK] Servidor respondendo!')
        data = response.json()
        print(f'Status: {data.get(\"status\", \"unknown\")}')
    else:
        print(f'[AVISO] Servidor respondeu com código: {response.status_code}')
except Exception as e:
    print(f'[AVISO] Não foi possível conectar ao servidor: {e}')
" 2>&1

echo [INFO] Parando servidor de teste...
taskkill /f /im python.exe >nul 2>&1

echo.
echo ========================================
echo        TESTES CONCLUÍDOS
echo ========================================
echo.
echo Se todos os testes passaram, a aplicação está pronta para uso!
echo.
echo Para iniciar a aplicação: iniciar.bat
echo Para diagnóstico completo: diagnostico.bat
echo.
pause

