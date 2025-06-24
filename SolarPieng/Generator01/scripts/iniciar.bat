@echo off
chcp 65001 >nul
title PIENG Solar Generator - Iniciar
color 0B

echo.
echo ========================================
echo      PIENG SOLAR GENERATOR v1.0
echo ========================================
echo.
echo    π  PiEng Soluções Energéticas
echo    Gerador de Propostas Solar
echo.
echo ========================================
echo.

echo [INFO] Verificando instalação...

if not exist venv (
    echo [ERRO] Ambiente virtual não encontrado!
    echo.
    echo Execute primeiro: instalador.bat
    echo.
    pause
    exit /b 1
)

if not exist src\main.py (
    echo [ERRO] Aplicação não encontrada!
    echo.
    echo Verifique se todos os arquivos estão presentes.
    echo.
    pause
    exit /b 1
)

echo [OK] Instalação verificada!

echo.
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [INFO] Iniciando PIENG Solar Generator...
echo.
echo ========================================
echo  APLICAÇÃO INICIADA COM SUCESSO!
echo ========================================
echo.
echo Interface Web: http://localhost:5000
echo API: http://localhost:5000/api
echo.
echo Para parar a aplicação: Ctrl+C
echo.
echo ========================================
echo.

python src\main.py

echo.
echo [INFO] Aplicação encerrada.
pause

