@echo off
chcp 65001 >nul
title PIENG Solar Generator - Diagnóstico
color 0E

echo.
echo ========================================
echo   PIENG SOLAR GENERATOR - DIAGNÓSTICO
echo ========================================
echo.

echo [INFO] Executando diagnóstico do sistema...
echo.

echo ========================================
echo 1. VERIFICAÇÃO DO SISTEMA
echo ========================================

echo [INFO] Sistema Operacional:
ver

echo.
echo [INFO] Data e Hora:
date /t
time /t

echo.
echo ========================================
echo 2. VERIFICAÇÃO DO PYTHON
echo ========================================

echo [INFO] Versão do Python:
python --version 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
) else (
    echo [OK] Python instalado!
)

echo.
echo [INFO] Versão do pip:
pip --version 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] pip não encontrado!
) else (
    echo [OK] pip instalado!
)

echo.
echo ========================================
echo 3. VERIFICAÇÃO DO AMBIENTE VIRTUAL
echo ========================================

if exist venv (
    echo [OK] Ambiente virtual encontrado!
    
    echo.
    echo [INFO] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    
    echo.
    echo [INFO] Pacotes instalados:
    pip list
    
) else (
    echo [ERRO] Ambiente virtual não encontrado!
    echo Execute: instalador.bat
)

echo.
echo ========================================
echo 4. VERIFICAÇÃO DE DEPENDÊNCIAS
echo ========================================

echo [INFO] Tesseract OCR:
tesseract --version 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Tesseract não encontrado - OCR não funcionará
) else (
    echo [OK] Tesseract instalado!
)

echo.
echo ========================================
echo 5. VERIFICAÇÃO DE ARQUIVOS
echo ========================================

echo [INFO] Estrutura de arquivos:

if exist src\main.py (
    echo [OK] src\main.py
) else (
    echo [ERRO] src\main.py não encontrado!
)

if exist src\routes\api.py (
    echo [OK] src\routes\api.py
) else (
    echo [ERRO] src\routes\api.py não encontrado!
)

if exist src\utils\calculator.py (
    echo [OK] src\utils\calculator.py
) else (
    echo [ERRO] src\utils\calculator.py não encontrado!
)

if exist src\static\index.html (
    echo [OK] src\static\index.html
) else (
    echo [ERRO] src\static\index.html não encontrado!
)

if exist data\components_db.json (
    echo [OK] data\components_db.json
) else (
    echo [ERRO] data\components_db.json não encontrado!
)

if exist requirements.txt (
    echo [OK] requirements.txt
) else (
    echo [ERRO] requirements.txt não encontrado!
)

echo.
echo ========================================
echo 6. VERIFICAÇÃO DE PASTAS
echo ========================================

if exist uploads (
    echo [OK] pasta uploads
) else (
    echo [AVISO] pasta uploads não encontrada
    mkdir uploads
    echo [INFO] pasta uploads criada
)

if exist output (
    echo [OK] pasta output
) else (
    echo [AVISO] pasta output não encontrada
    mkdir output
    echo [INFO] pasta output criada
)

if exist data (
    echo [OK] pasta data
) else (
    echo [ERRO] pasta data não encontrada!
)

echo.
echo ========================================
echo 7. TESTE DE CONECTIVIDADE
echo ========================================

echo [INFO] Testando conectividade com a internet...
ping -n 1 google.com >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Sem conexão com a internet
    echo Algumas funcionalidades podem não funcionar
) else (
    echo [OK] Conexão com a internet ativa
)

echo.
echo ========================================
echo        DIAGNÓSTICO CONCLUÍDO
echo ========================================
echo.
echo Se houver erros críticos, execute: instalador.bat
echo Para testar a aplicação, execute: teste.bat
echo Para iniciar a aplicação, execute: iniciar.bat
echo.
pause

