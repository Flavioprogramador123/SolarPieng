import pdfplumber
import re
import random
from typing import Dict, List, Optional  # <--- ADICIONE Optional AQUI
import os
from PIL import Image
import pytesseract
import warnings

warnings.filterwarnings('ignore')


class DataExtractor:
    def __init__(self):
        # Padrões para PDFs (mantidos do seu APIFornecedores original)
        self.pdf_patterns = {
            'fortlev': {
                'potencia_regex': r'(?:Gerador FV|Potência total)\s*([\d\.,]+)\s*kWp',
                'valor_regex': r'R\$\s*([\d\.,]+)',
                'modulos_qty_regex': r'Quantidade:\s*(\d+)',
                'painel_regex': r'PAINEL\s+([^\n]+)',
                'inversor_regex': r'(FOXESS[^\n]+)',
                'frete_pattern': 'CIF'
            },
            'belenergy': {
                'potencia_regex': r'Potência do sistema:\s*([\d\.,]+)\s*kWp',
                'valor_regex': r'R\$\s*([\d\.,]+)',
                'modulos_qty_regex': r'(\d+)\s*PC',
                'painel_regex': r'MODULO\s+([^\n]+?)(?:Cód:|$)',
                'inversor_regex': r'INVERSOR[^\n]+',
                'frete_pattern': 'CIF'
            },
            'soollar': {
                'potencia_regex': r'(?:Potência|Geração)\s*(?:total|FV)?:?\s*([\d\.,]+)\s*kWp',
                'valor_regex': r'(?:Total|Valor).*?R\$\s*([\d\.,]+)',
                'modulos_qty_regex': r'(?:Quantidade|Qtd).*?(\d+)',
                'painel_regex': r'(?:PAINEL|MÓDULO|MODULO)\s+([^\n]+)',
                'inversor_regex': r'(?:INVERSOR|MICRO)\s+([^\n]+)',
                'frete_pattern': 'CIF'
            }
        }
        # Adicione padrões específicos para imagens se necessário
        self.image_patterns = {
            # Por enquanto, usaremos padrões genéricos para imagem.
            # A segmentação de múltiplos cards será o desafio aqui.
            'generico': {
                'potencia_regex': r'([\d\.,]+)\s*kWp',
                'valor_regex': r'R\$\s*([\d\.,]+)',
                # Ex: 84x Painel
                'modulos_qty_regex': r'(\d+)\s*x\s*(?:Painel|Módulo|MODULO)\b',
                # Ex: Painel XXX Wp
                'painel_regex': r'(?:Painel|Módulo|MODULO)\s+([^\n]+?\d+Wp)',
                'inversor_regex': r'(?:Inversor|Inversor String|Microinversor|FOXESS|SOLIS)[^\n]+',
            }
        }

    def detect_supplier_from_text(self, text: str) -> str:
        """Detecta o fornecedor baseado no texto."""
        text_lower = text.lower()
        if 'fortlev' in text_lower or 'dah solar' in text_lower:
            return 'fortlev'
        elif 'belenergy' in text_lower or 'bel energy' in text_lower:
            return 'belenergy'
        elif 'soollar' in text_lower:
            return 'soollar'
        else:
            return 'generico'

    def _extract_from_pdf(self, filepath: str) -> List[Dict]:
        """Extrai dados de um PDF."""
        print(f"📤 Extraindo dados do PDF: {os.path.basename(filepath)}")
        extracted_systems = []
        try:
            with pdfplumber.open(filepath) as pdf:
                text_full = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_full += page_text + "\n"

            if not text_full.strip():
                print("❌ Não foi possível extrair texto do PDF")
                return [self._generate_generic_system(os.path.basename(filepath))]

            supplier = self.detect_supplier_from_text(text_full)
            print(f"🏢 Fornecedor detectado (PDF): {supplier}")

            # Reusa a lógica de extração baseada em padrões
            data = self._parse_text_with_patterns(
                text_full, self.pdf_patterns.get(supplier, {}), supplier)
            if data:
                extracted_systems.append(data)
            else:  # Fallback para genérico se a extração específica falhar
                extracted_systems.append(
                    self._generate_generic_system(os.path.basename(filepath)))

        except Exception as e:
            print(f"❌ Erro na extração de PDF: {str(e)}")
            extracted_systems.append(
                self._generate_generic_system(os.path.basename(filepath)))

        return extracted_systems

    def _extract_from_image(self, filepath: str) -> List[Dict]:
        """Extrai dados de uma imagem usando OCR.
           Esta é a parte que precisa de desenvolvimento robusto para MÚLTIPLOS CARDS.
           Por enquanto, fará um OCR simples na imagem toda ou simulará.
        """
        print(
            f"📤 Extraindo dados da imagem (OCR): {os.path.basename(filepath)}")
        extracted_systems = []
        try:
            image = Image.open(filepath)

            # --- Pré-processamento de imagem (Básico) ---
            # Pode ser necessário mais pré-processamento aqui para melhorar o OCR
            # ex: image = image.convert('L') # Convert to grayscale
            #     image = image.point(lambda x: 0 if x < 128 else 255) # Binarize

            # --- Lógica de Segmentação (PROVISÓRIO / SIMULADO) ---
            # Esta é a parte mais complexa. Para 'fortlev02.jpg' que é um grid,
            # precisaríamos de visão computacional para detectar cada card.
            # Por agora, faremos OCR na imagem inteira e tentaremos extrair UM sistema
            # ou simularemos múltiplos sistemas para demonstração da estrutura.

            text_full = pytesseract.image_to_string(
                image, lang='por')  # OCR em português
            # Print dos primeiros 500 chars
            print(f"Texto extraído da imagem:\n{text_full[:500]}...")

            # Simulação de extração de múltiplos sistemas (se o layout permitir um padrão)
            # Para o layout de cards da Fortlev (fortlev02.jpg), podemos buscar por "Gerador FV"
            # e tentar segmentar o texto em blocos. Esta é uma implementação SIMPLIFICADA.

            # Dividir o texto em blocos baseados em um marcador comum para cada card
            # Exemplo de regex para dividir o texto pelos títulos dos geradores
            card_texts = re.split(
                r'(Gerador FV [\d\.,]+\s*kWp)', text_full, flags=re.IGNORECASE)

            # O primeiro elemento de card_texts pode ser lixo antes do primeiro card
            # Os elementos pares (1, 3, 5...) são os títulos, os ímpares (2, 4, 6...) são o conteúdo

            # Filtrar e reassociar título com conteúdo
            parsed_card_texts = []
            for i in range(1, len(card_texts), 2):
                if i + 1 < len(card_texts):
                    # Combine o título do card com seu conteúdo associado
                    parsed_card_texts.append(card_texts[i] + card_texts[i+1])
                else:
                    # Último card pode não ter conteúdo subsequente se for o final
                    parsed_card_texts.append(card_texts[i])

            if not parsed_card_texts:  # Se não encontrou múltiplos cards, tenta extrair da imagem toda como um único sistema
                print(
                    "Não foram detectados múltiplos cards, tentando extração única da imagem.")
                data = self._parse_text_with_patterns(
                    text_full, self.image_patterns['generico'], 'generico_imagem')
                if data:
                    extracted_systems.append(data)
                else:
                    extracted_systems.append(
                        self._generate_generic_system(os.path.basename(filepath)))
            else:
                print(
                    f"Detectados {len(parsed_card_texts)} potenciais cards na imagem.")
                for i, card_text in enumerate(parsed_card_texts):
                    print(f"Processando Card {i+1}...")
                    data = self._parse_text_with_patterns(
                        card_text, self.image_patterns['generico'], f'generico_imagem_card_{i+1}')
                    if data:
                        # Adicionar um nome mais descritivo se possível
                        if "Fortlev" in card_text:
                            data['name'] = f"Fortlev Imagem Sistema {i+1}"
                        elif "Soollar" in card_text:
                            data['name'] = f"Soollar Imagem Sistema {i+1}"
                        # ... outros fornecedores de imagem
                        else:
                            data['name'] = f"Imagem Sistema {i+1}"

                        extracted_systems.append(data)
                    else:
                        print(
                            f"❌ Falha na extração do Card {i+1}, gerando sistema genérico.")
                        extracted_systems.append(self._generate_generic_system(
                            f"{os.path.basename(filepath)}_card_{i+1}"))

        except pytesseract.TesseractNotFoundError:
            print("❌ Tesseract OCR não encontrado. Por favor, instale-o no seu sistema.")
            extracted_systems.append(self._generate_generic_system(
                os.path.basename(filepath), error="Tesseract não instalado"))
        except Exception as e:
            print(f"❌ Erro na extração de imagem: {str(e)}")
            extracted_systems.append(self._generate_generic_system(
                os.path.basename(filepath), error=str(e)))

        return extracted_systems

    def _parse_text_with_patterns(self, text: str, patterns: Dict, default_name: str) -> Optional[Dict]:
        """Tenta extrair dados usando um conjunto de padrões."""
        data = {"name": default_name, "freight_included": True,
                "freight_value": 0}  # Default

        # Potência
        match_potencia = re.search(patterns.get(
            'potencia_regex', ''), text, re.IGNORECASE)
        if match_potencia:
            potencia_str = match_potencia.group(
                1).replace('.', '').replace(',', '.')
            data['power'] = float(potencia_str)

        # Valor total
        match_valor = re.search(patterns.get(
            'valor_regex', ''), text, re.IGNORECASE)
        if match_valor:
            valor_str = match_valor.group(1).replace('.', '').replace(',', '.')
            data['vcusto_raw'] = float(valor_str)

        # Quantidade de módulos (pode precisar de ajuste fino para diferentes layouts)
        match_modulos = re.search(patterns.get(
            'modulos_qty_regex', ''), text, re.IGNORECASE)
        if match_modulos:
            data['modules_count'] = int(match_modulos.group(1))
        else:  # Tentar inferir de 600Wp se potência e custo existem
            if 'power' in data and 'vcusto_raw' in data:
                # Estimativa baseada em um painel de 600Wp
                estimated_modules = int(data['power'] * 1000 / 600)
                data['modules_count'] = estimated_modules

        # Descrição do painel
        match_painel = re.search(patterns.get(
            'painel_regex', ''), text, re.IGNORECASE)
        if match_painel:
            data['modules_desc'] = match_painel.group(
                0).strip()  # Pegar a string completa
        elif 'modules_count' in data:
            # Default
            data['modules_desc'] = f"{data['modules_count']}x Painel Solar 600Wp (Estimado)"

        # Inversor
        match_inversor = re.search(patterns.get(
            'inverter_regex', ''), text, re.IGNORECASE)
        if match_inversor:
            data['inverter_desc'] = match_inversor.group(0).strip()
            # Tipo de inversor
            inv_desc_lower = data['inverter_desc'].lower()
            data['inverter_type'] = 'micro' if 'micro' in inv_desc_lower else 'string'
        else:
            data['inverter_desc'] = "Inversor String (Não Identificado)"
            data['inverter_type'] = 'string'

        # Frete (apenas para PDFs por enquanto, em imagens é mais difícil detectar)
        if 'frete_pattern' in patterns:
            data['freight_included'] = patterns['frete_pattern'] in text
            # FIXED_ADDITIONAL_COST_PER_MODULE não está acessível aqui
            data['freight_value'] = 0 if data['freight_included'] else 0

        # Validação mínima
        if 'power' not in data or 'vcusto_raw' not in data:
            print(
                f"❌ Falha na extração de dados essenciais para {default_name}")
            return None  # Retorna None se não conseguir extrair o mínimo

        return data

    def _generate_generic_system(self, filename: str, error: str = "") -> Dict:
        """Gera um sistema genérico em caso de falha na extração."""
        base_power = random.uniform(50.0, 120.0)
        base_vcusto = base_power * random.uniform(900, 1200)
        # Supondo painéis de 600Wp para estimativa
        base_modules = int(base_power / 0.6)

        name = f"Fornecedor Genérico ({filename.split('.')[0]})"
        if error:
            name += f" - ERRO: {error}"

        return {
            "name": name,
            "vcusto_raw": round(base_vcusto, 2),
            "power": round(base_power, 2),
            "modules_count": base_modules,
            "modules_desc": f"{base_modules}x Painel Solar 600Wp (Simulado)",
            "inverter_desc": "Inversor String Trifásico (Simulado)",
            "inverter_type": "string",
            "freight_included": True,
            "freight_value": 0
        }

    def extract_systems_from_file(self, filepath: str) -> List[Dict]:
        """Função principal para extrair dados de PDF ou imagem."""
        file_extension = os.path.splitext(filepath)[1].lower()

        if file_extension == '.pdf':
            return self._extract_from_pdf(filepath)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return self._extract_from_image(filepath)
        else:
            print(
                f"🚫 Tipo de arquivo não suportado para extração: {file_extension}")
            return [self._generate_generic_system(os.path.basename(filepath), error="Tipo de arquivo não suportado")]
