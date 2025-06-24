import json
import os
from datetime import datetime
from typing import Dict, List
from jinja2 import Template


class ProposalHTMLGenerator:
    """
    Gerador de propostas HTML responsivas para energia solar.
    Suporta dois formatos: Padrão (enxuto) e Analítico (detalhado).
    """
    
    def __init__(self, templates_path: str = None, branding_path: str = None):
        self.templates_path = templates_path or "src/templates"
        
        # Carregar configurações de branding
        if branding_path and os.path.exists(branding_path):
            with open(branding_path, 'r', encoding='utf-8') as f:
                self.branding = json.load(f)
        else:
            self.branding = self._default_branding()
    
    def _default_branding(self) -> Dict:
        """Configurações padrão de branding da PiEng."""
        return {
            "company_name": "PiEng Solar",
            "company_full_name": "PiEng Soluções Energéticas",
            "logo_symbol": "π",
            "primary_color": "#3366CC",
            "secondary_color": "#FF6B35",
            "gradient": "linear-gradient(135deg, #3366CC 0%, #FF6B35 100%)",
            "warranty_equipment": "12 anos",
            "warranty_installation": "12 meses",
            "contact_phone": "(62) 99999-9999",
            "contact_email": "contato@pieng.com.br",
            "website": "www.pieng.com.br"
        }
    
    def _generate_ai_analysis(self, proposals: List[Dict], client_name: str) -> str:
        """
        Gera análise persuasiva com IA para a proposta analítica.
        """
        best_proposal = proposals[0] if proposals else None
        if not best_proposal:
            return ""
        
        power = best_proposal['kit_info']['power']
        monthly_savings = best_proposal['calculations']['monthly_savings']
        payback = best_proposal['calculations']['final_payback_months']
        final_price = best_proposal['pricing']['final_price']
        
        analysis = f"""
        <div class="ai-analysis">
            <h3>🤖 Análise Inteligente do Investimento</h3>
            
            <div class="analysis-section">
                <h4>💰 Viabilidade Financeira Excepcional</h4>
                <p>Caro(a) {client_name}, nossa análise técnica revela que este investimento em energia solar 
                apresenta características financeiras extraordinárias. Com um payback de apenas 
                <strong>{payback:.1f} meses</strong>, você recuperará seu investimento em menos de 
                <strong>{payback/12:.1f} anos</strong>, muito abaixo da média nacional de 4-6 anos.</p>
            </div>
            
            <div class="analysis-section">
                <h4>🌱 Impacto Ambiental e Sustentabilidade</h4>
                <p>Além dos benefícios financeiros, seu sistema de {power:.2f} kWp evitará a emissão de 
                aproximadamente <strong>{power * 1.2:.1f} toneladas de CO₂</strong> por ano, equivalente ao 
                plantio de <strong>{int(power * 15)} árvores</strong>. Você estará contribuindo ativamente 
                para um futuro mais sustentável.</p>
            </div>
            
            <div class="analysis-section">
                <h4>📈 Valorização Patrimonial</h4>
                <p>Estudos do mercado imobiliário indicam que imóveis com energia solar valorizam entre 
                <strong>3% a 6%</strong>. Para um imóvel de R$ 500.000, isso representa uma valorização 
                adicional de <strong>R$ 15.000 a R$ 30.000</strong>, além da economia mensal de energia.</p>
            </div>
            
            <div class="analysis-section">
                <h4>🛡️ Proteção Contra Inflação Energética</h4>
                <p>Com a tarifa de energia aumentando em média <strong>4,8% ao ano</strong>, sua economia 
                mensal de R$ {monthly_savings:.2f} crescerá proporcionalmente. Em 10 anos, considerando 
                apenas a inflação energética, você economizará mais de 
                <strong>R$ {monthly_savings * 12 * 10 * 1.6:.0f}</strong>.</p>
            </div>
            
            <div class="analysis-section">
                <h4>⚡ Tecnologia de Ponta e Confiabilidade</h4>
                <p>Os equipamentos selecionados utilizam tecnologia fotovoltaica de última geração, com 
                <strong>garantia de 12 anos do fabricante</strong> e <strong>12 meses de garantia de 
                instalação pela PiEng Solar</strong>. Nossa equipe técnica especializada garante máxima 
                eficiência e durabilidade do seu sistema.</p>
            </div>
            
            <div class="conclusion">
                <h4>🎯 Conclusão da Análise</h4>
                <p><strong>Este é o momento ideal para investir em energia solar.</strong> Com tecnologia 
                madura, preços competitivos e incentivos governamentais vigentes, você tem a oportunidade 
                única de transformar um gasto mensal em um investimento rentável e sustentável.</p>
                
                <div class="urgency-note">
                    <p>⏰ <strong>Atenção:</strong> Os preços dos equipamentos fotovoltaicos têm apresentado 
                    volatilidade devido ao cenário internacional. Garantimos este orçamento por 
                    <strong>15 dias</strong>.</p>
                </div>
            </div>
        </div>
        """
        
        return analysis
    
    def generate_standard_proposal(self, proposals: List[Dict], client_data: Dict, 
                                 output_path: str = None) -> str:
        """
        Gera proposta padrão/enxuta focada em impacto visual e benefícios principais.
        """
        template_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ branding.company_name }} - Proposta Solar para {{ client_data.name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {{ branding.gradient }};
            min-height: 100vh;
            padding: 10px;
            margin: 0;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .header {
            background: {{ branding.gradient }};
            color: white;
            padding: 20px;
            text-align: center;
        }
        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .logo-circle {
            background: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: {{ branding.primary_color }};
            font-weight: bold;
            font-size: 18px;
        }
        .logo-text {
            text-align: left;
        }
        .logo-text h1 {
            font-size: 1.4em;
            font-weight: bold;
            margin: 0;
        }
        .logo-text p {
            font-size: 0.8em;
            opacity: 0.9;
            margin: 0;
        }
        .header h2 {
            font-size: 1.5em;
            margin: 5px 0;
        }
        .header p {
            font-size: 0.9em;
            margin: 0;
        }
        .urgency-banner {
            background: #e74c3c;
            color: white;
            text-align: center;
            padding: 8px;
            font-weight: bold;
            font-size: 0.9em;
        }
        .main-content {
            padding: 20px;
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        .system-card {
            background: #f8f9fa;
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            border: 2px solid transparent;
            font-size: 0.9em;
        }
        .system-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .system-card.recommended {
            border-color: #2ecc71;
            position: relative;
        }
        .recommended-badge {
            position: absolute;
            top: 8px;
            right: 8px;
            background: #2ecc71;
            color: white;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 0.7em;
            font-weight: bold;
            z-index: 1;
        }
        .card-header {
            background: {{ branding.gradient }};
            color: white;
            padding: 12px;
            text-align: center;
        }
        .card-title {
            font-size: 1em;
            font-weight: bold;
            margin-bottom: 3px;
        }
        .card-power {
            font-size: 1.3em;
            font-weight: bold;
            margin: 5px 0;
        }
        .card-body {
            padding: 12px;
        }
        .specs-list {
            list-style: none;
            margin: 8px 0;
            font-size: 0.8em;
        }
        .specs-list li {
            padding: 2px 0;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .price-section {
            background: #f1f3f4;
            padding: 8px;
            border-radius: 6px;
            text-align: center;
            margin: 8px 0;
        }
        .original-price {
            font-size: 0.8em;
            color: #e74c3c;
            text-decoration: line-through;
            margin-bottom: 3px;
            font-weight: bold;
        }
        .final-price {
            font-size: 1.2em;
            font-weight: bold;
            color: {{ branding.primary_color }};
            margin: 5px 0;
        }
        .payment-options {
            display: grid;
            grid-template-columns: 1fr;
            gap: 4px;
            margin: 8px 0;
        }
        .payment-option {
            background: #f8f9fa;
            padding: 6px;
            border-radius: 4px;
            text-align: center;
            border: 1px solid transparent;
        }
        .payment-option.highlight {
            border-color: #2ecc71;
            background: #e8f5e8;
        }
        .payment-title {
            font-size: 0.7em;
            font-weight: bold;
            margin-bottom: 3px;
            color: #333;
        }
        .payment-value {
            font-size: 0.8em;
            font-weight: bold;
            color: {{ branding.primary_color }};
        }
        .discount-tag {
            background: #2ecc71;
            color: white;
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.6em;
            display: inline-block;
            margin-top: 3px;
        }
        .benefits {
            background: #e8f5e8;
            padding: 6px;
            border-radius: 4px;
            margin: 6px 0;
            font-size: 0.75em;
        }
        .benefits h4 {
            color: #2ecc71;
            margin-bottom: 4px;
            font-size: 0.9em;
        }
        .select-button {
            width: 100%;
            background: {{ branding.gradient }};
            color: white;
            border: none;
            padding: 8px;
            border-radius: 5px;
            font-size: 0.8em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .select-button:hover {
            transform: scale(1.02);
        }
        .cta-section {
            background: {{ branding.gradient }};
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            margin-top: 15px;
        }
        .cta-section h3 {
            font-size: 1.2em;
            margin-bottom: 8px;
        }
        .cta-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 10px 0;
        }
        .cta-button {
            background: white;
            color: {{ branding.primary_color }};
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            font-size: 0.8em;
            transition: transform 0.3s ease;
        }
        .cta-button:hover {
            transform: scale(1.05);
        }
        .warranty-section {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
        }
        .warranty-section h3 {
            color: {{ branding.primary_color }};
            margin-bottom: 10px;
        }
        .warranty-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
        }
        .warranty-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid {{ branding.secondary_color }};
        }
        @media print {
            body {
                background: white !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            .container {
                box-shadow: none !important;
                border-radius: 0 !important;
                max-width: 100% !important;
                margin: 0 !important;
            }
        }
        @media (max-width: 768px) {
            .cards-grid {
                grid-template-columns: 1fr;
            }
            .warranty-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-circle">{{ branding.logo_symbol }}</div>
                <div class="logo-text">
                    <h1>{{ branding.company_name }}</h1>
                    <p>{{ branding.company_full_name }}</p>
                </div>
            </div>
            <h2>🌞 Proposta de Sistema Solar para {{ client_data.name }}</h2>
            <p>Escolha a Melhor Opção para Seu Imóvel</p>
        </div>
        <div class="urgency-banner">
            ⚡ INVESTIMENTO INTELIGENTE: SEU RETORNO RÁPIDO E CRESCENTE!
        </div>
        <div class="main-content">
            <div class="cards-grid">
                {% for proposal in proposals %}
                <div class="system-card {% if proposal.is_recommended %}recommended{% endif %}">
                    {% if proposal.is_recommended %}
                    <div class="recommended-badge">⭐ MELHOR OPÇÃO</div>
                    {% endif %}
                    <div class="card-header">
                        <div class="card-title">{{ proposal.kit_info.name }}</div>
                        <div class="card-power">{{ proposal.kit_info.power|round(2) }} kWp</div>
                    </div>
                    <div class="card-body">
                        <ul class="specs-list">
                            <li>✓ {{ proposal.kit_info.modules_desc }}</li>
                            <li>✓ {{ proposal.kit_info.inverter_desc }}</li>
                            <li>✓ Solução Otimizada para Retorno Rápido</li>
                        </ul>
                        <div class="price-section">
                            <div class="original-price">INVESTIMENTO: R$ {{ proposal.pricing.crossed_price|round(2)|replace(".", ",") }}</div>
                            <div class="final-price">R$ {{ proposal.pricing.final_price|round(2)|replace(".", ",") }}</div>
                            <div class="discount-tag">Preço Especial</div>
                        </div>
                        <div class="payment-options">
                            <div class="payment-option highlight">
                                <div class="payment-title">💰 À VISTA/PIX</div>
                                <div class="payment-value">R$ {{ proposal.pricing.cash_price|round(2)|replace(".", ",") }}</div>
                                <div class="discount-tag">{{ proposal.pricing.discount_cash_percent }}% OFF</div>
                            </div>
                            <div class="payment-option">
                                <div class="payment-title">💳 12x SEM JUROS</div>
                                <div class="payment-value">R$ {{ proposal.pricing.installment_12x|round(2)|replace(".", ",") }}</div>
                                <div style="font-size: 0.6em; color: #666;">Entrada + 11x</div>
                            </div>
                            <div class="payment-option">
                                <div class="payment-title">💳 18x CARTÃO</div>
                                <div class="payment-value">R$ {{ proposal.pricing.financing_installment|round(2)|replace(".", ",") }}</div>
                                <div style="font-size: 0.6em; color: #666;">Sem entrada</div>
                            </div>
                        </div>
                        <div class="benefits">
                            <h4>💡 Benefícios:</h4>
                            <p>• Geração: ~{{ proposal.calculations.monthly_generation|round(0) }} kWh/mês<br>
                            • Economia: R$ {{ proposal.calculations.monthly_savings|round(2)|replace(".", ",") }}/mês<br>
                            • Payback: {{ proposal.calculations.final_payback_months|round(1) }} meses<br>
                            • <strong>Margem: {{ proposal.calculations.final_margin_percent|round(1) }}%</strong></p>
                        </div>
                        <button class="select-button">
                            ESCOLHER ESTA OPÇÃO
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <div class="warranty-section">
                <h3>🛡️ Garantias Incluídas</h3>
                <div class="warranty-grid">
                    <div class="warranty-item">
                        <strong>Equipamentos</strong><br>
                        {{ branding.warranty_equipment }} pelo fabricante
                    </div>
                    <div class="warranty-item">
                        <strong>Instalação</strong><br>
                        {{ branding.warranty_installation }} pela {{ branding.company_name }}
                    </div>
                </div>
            </div>
            
            <div class="cta-section">
                <h3>🚀 Pronto para Economizar?</h3>
                <p>Entre em contato conosco e transforme sua conta de luz em investimento!</p>
                <div class="cta-buttons">
                    <button class="cta-button">📱 {{ branding.contact_phone }}</button>
                    <button class="cta-button">📧 {{ branding.contact_email }}</button>
                    <button class="cta-button">🌐 {{ branding.website }}</button>
                </div>
                <p style="font-size: 0.8em; margin-top: 10px;">
                    Proposta válida por 15 dias • Gerada em {{ current_date }}
                </p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(template_content)
        html_content = template.render(
            proposals=proposals,
            client_data=client_data,
            branding=self.branding,
            current_date=datetime.now().strftime("%d/%m/%Y")
        )
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return html_content
    
    def generate_analytical_proposal(self, proposals: List[Dict], client_data: Dict, 
                                   output_path: str = None) -> str:
        """
        Gera proposta analítica com análise detalhada, gráficos e texto persuasivo da IA.
        """
        ai_analysis = self._generate_ai_analysis(proposals, client_data.get('name', 'Cliente'))
        
        # Para a versão analítica, vamos usar o template padrão + seções adicionais
        standard_html = self.generate_standard_proposal(proposals, client_data)
        
        # Inserir análise da IA antes da seção de CTA
        analytical_html = standard_html.replace(
            '<div class="cta-section">',
            ai_analysis + '<div class="cta-section">'
        )
        
        # Adicionar estilos específicos para a análise
        ai_styles = """
        <style>
        .ai-analysis {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #FF6B35;
        }
        .ai-analysis h3 {
            color: #3366CC;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        .analysis-section {
            margin: 15px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .analysis-section h4 {
            color: #FF6B35;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        .conclusion {
            background: linear-gradient(135deg, #3366CC 0%, #FF6B35 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        .conclusion h4 {
            color: white !important;
            margin-bottom: 10px;
        }
        .urgency-note {
            background: rgba(255, 255, 255, 0.2);
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            border-left: 3px solid #FFD700;
        }
        </style>
        """
        
        analytical_html = analytical_html.replace('</head>', ai_styles + '</head>')
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(analytical_html)
        
        return analytical_html

