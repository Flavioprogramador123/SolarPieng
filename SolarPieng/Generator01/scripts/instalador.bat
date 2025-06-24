@echo off
chcp 65001 >nul
title PIENG Solar Generator - Instalador
color 0A

echo.
echo ========================================
echo    PIENG SOLAR GENERATOR - INSTALADOR
echo ========================================
echo.

echo [INFO] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!

echo.
echo [INFO] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] pip não encontrado!
    echo.
    echo Reinstale o Python com pip incluído.
    pause
    exit /b 1
)

echo [OK] pip encontrado!

echo.
echo [INFO] Criando ambiente virtual...
if exist venv (
    echo [INFO] Ambiente virtual já existe, removendo...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar ambiente virtual!
    pause
    exit /b 1
)

echo [OK] Ambiente virtual criado!

echo.
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [INFO] Atualizando pip...
python -m pip install --upgrade pip

echo.
echo [INFO] Instalando dependências...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependências!
    echo.
    echo Verifique sua conexão com a internet e tente novamente.
    pause
    exit /b 1
)

echo.
echo [INFO] Verificando Tesseract OCR...
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [AVISO] Tesseract OCR não encontrado!
    echo.
    echo Para usar a funcionalidade de OCR, instale o Tesseract:
    echo https://github.com/UB-Mannheim/tesseract/wiki
    echo.
    echo A aplicação funcionará sem OCR, mas com funcionalidade limitada.
    echo.
)

echo.
echo [INFO] Criando pastas necessárias...
if not exist uploads mkdir uploads
if not exist output mkdir output
if not exist data mkdir data

echo.
echo ========================================
echo        INSTALAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo A aplicação PIENG Solar Generator foi instalada com sucesso!
echo.
echo Para iniciar a aplicação, execute: iniciar.bat
echo Para testar a instalação, execute: teste.bat
echo Para diagnóstico, execute: diagnostico.bat
echo.
pause

