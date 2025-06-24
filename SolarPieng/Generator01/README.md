# PIENG Solar Generator

Sistema completo para geração de propostas de energia solar fotovoltaica.

## 🚀 Instalação Rápida

1. **Execute o instalador:**
   ```
   scripts\instalador.bat
   ```

2. **Teste a instalação:**
   ```
   scripts\teste.bat
   ```

3. **Inicie a aplicação:**
   ```
   scripts\iniciar.bat
   ```

## 📋 Scripts Disponíveis

- **`instalador.bat`** - Instala todas as dependências e configura o ambiente
- **`iniciar.bat`** - Inicia a aplicação PIENG Solar Generator
- **`diagnostico.bat`** - Executa diagnóstico completo do sistema
- **`teste.bat`** - Testa todas as funcionalidades da aplicação

## 🌐 Acesso à Aplicação

Após iniciar com `iniciar.bat`, acesse:
- **Interface Web:** http://localhost:5000
- **API:** http://localhost:5000/api

## 📱 Funcionalidades

### 1. Dados do Cliente
- Nome obrigatório
- Dados opcionais (email, telefone, endereço)
- Parâmetros de simulação configuráveis

### 2. Kits de Fornecedores
- Entrada manual de dados
- Upload de PDFs/imagens com OCR
- Comparação automática de múltiplos kits

### 3. Orçamento Rápido
- Baseado apenas no consumo mensal
- Seleção automática de componentes
- Ideal para atendimento residencial

### 4. Geração de Propostas
- Formato Padrão (enxuto)
- Formato Analítico (detalhado com IA)
- HTML responsivo para WhatsApp

## 🔧 Lógica de Precificação

- **Margem inicial:** 40% sobre o custo
- **Payback alvo:** 16-20 meses
- **Ajuste automático** de preços
- **Engenharia de preços** para diferentes modalidades

## 📊 Estrutura de Preços

- **À vista/PIX:** Com desconto
- **12x sem juros:** Preço sem desconto
- **18x cartão:** Com taxa de financiamento
- **Preço riscado:** "INVESTIMENTO" para estratégia de vendas

## 🛡️ Garantias Incluídas

- **Equipamentos:** 12 anos (fabricante)
- **Instalação:** 12 meses (PiEng Solar)

## 📁 Estrutura do Projeto

```
pieng_solar_generator/
├── scripts/           # Scripts .bat para facilitar uso
├── src/              # Código fonte da aplicação
│   ├── main.py       # Aplicação Flask principal
│   ├── routes/       # Rotas da API
│   ├── utils/        # Módulos de cálculo e geração
│   └── static/       # Interface web
├── data/             # Configurações e banco de dados
├── uploads/          # Arquivos enviados para OCR
├── output/           # Propostas HTML geradas
└── venv/             # Ambiente virtual Python
```

## 🔍 Solução de Problemas

1. **Erro de Python não encontrado:**
   - Instale Python 3.8+ de https://python.org

2. **OCR não funciona:**
   - Instale Tesseract OCR
   - A aplicação funciona sem OCR, mas com funcionalidade limitada

3. **Erro de dependências:**
   - Execute `instalador.bat` novamente

4. **Problemas de conexão:**
   - Verifique se a porta 5000 está livre
   - Execute `diagnostico.bat` para análise completa

## 📞 Suporte

Para suporte técnico, execute `diagnostico.bat` e envie o resultado junto com a descrição do problema.

---

**PiEng Soluções Energéticas**  
*Transformando energia em oportunidades*

