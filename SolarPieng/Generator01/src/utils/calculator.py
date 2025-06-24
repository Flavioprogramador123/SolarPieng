import json
import math
from typing import Dict, List, Optional, Tuple


class SolarCalculator:
    """
    Implementa a lógica de precificação v5.3 conforme especificado:
    - Margem alvo inicial de 40%
    - Ajuste de preço para payback entre 16-20 meses
    - Engenharia de preços para diferentes modalidades de pagamento
    """
    
    def __init__(self, config_path: str = None):
        self.default_params = {
            'margin_target': 40,  # %
            'hsp': 5.25,  # kWh/m²/dia
            'tariff': 1.10,  # R$/kWh
            'simultaneity_factor': 30,  # %
            'energy_inflation': 4.8,  # %
            'system_efficiency': 75,  # %
            'consumption_factor': 65,  # %
            'days_per_month': 365 / 12,
            'payback_min': 16,  # meses
            'payback_max': 20,  # meses
            'discount_cash': 10,  # %
            'financing_rate': 15.5,  # %
            'markup_no_discount': 10,  # %
            'markup_crossed_price': 15.5  # %
        }
        
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.default_params.update(config.get('calculation_params', {}))
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
    
    def calculate_monthly_savings(self, power_kwp: float, params: Dict = None) -> float:
        """
        Calcula a economia mensal baseada na potência do sistema.
        
        Fórmula: Potência (kWp) * HSP * dias_no_mes * eficiencia_sistema * fator_consumo * tarifa_energia
        """
        if params is None:
            params = self.default_params
        
        monthly_generation = (
            power_kwp * 
            params['hsp'] * 
            params['days_per_month'] * 
            (params['system_efficiency'] / 100) * 
            (params['consumption_factor'] / 100)
        )
        
        monthly_savings = monthly_generation * params['tariff']
        return monthly_savings
    
    def calculate_payback(self, investment: float, monthly_savings: float) -> float:
        """Calcula o payback em meses."""
        if monthly_savings <= 0:
            return float('inf')
        return investment / monthly_savings
    
    def adjust_price_for_payback(self, initial_price: float, monthly_savings: float, params: Dict = None) -> Tuple[float, float]:
        """
        Ajusta o preço para que o payback fique entre 16-20 meses.
        Retorna (preço_final, payback_final)
        """
        if params is None:
            params = self.default_params
        
        initial_payback = self.calculate_payback(initial_price, monthly_savings)
        
        if initial_payback < params['payback_min']:
            # Payback muito baixo, aumentar preço
            final_price = monthly_savings * params['payback_min']
            final_payback = params['payback_min']
        elif initial_payback > params['payback_max']:
            # Payback muito alto, reduzir preço
            final_price = monthly_savings * params['payback_max']
            final_payback = params['payback_max']
        else:
            # Payback já está na faixa ideal
            final_price = initial_price
            final_payback = initial_payback
        
        return final_price, final_payback
    
    def calculate_pricing_structure(self, final_price: float, params: Dict = None) -> Dict:
        """
        Calcula toda a estrutura de preços baseada no preço final ajustado.
        """
        if params is None:
            params = self.default_params
        
        # Preço sem desconto (para 12x)
        price_no_discount = final_price * (1 + params['markup_no_discount'] / 100)
        
        # Preço "riscado" (INVESTIMENTO)
        crossed_price = price_no_discount * (1 + params['markup_crossed_price'] / 100)
        
        # Preço à vista (com desconto)
        cash_price = final_price * (1 - params['discount_cash'] / 100)
        
        # Financiamento 18x
        financing_total = final_price * (1 + params['financing_rate'] / 100)
        financing_installment = financing_total / 18
        
        # Parcelamento 12x sem juros
        installment_12x = price_no_discount / 12
        
        return {
            'final_price': final_price,
            'cash_price': cash_price,
            'price_no_discount': price_no_discount,
            'crossed_price': crossed_price,
            'financing_total': financing_total,
            'financing_installment': financing_installment,
            'installment_12x': installment_12x,
            'discount_cash_percent': params['discount_cash'],
            'financing_rate_percent': params['financing_rate']
        }
    
    def calculate_system_proposal(self, kit_data: Dict, params: Dict = None) -> Dict:
        """
        Calcula uma proposta completa para um kit/sistema.
        
        kit_data deve conter:
        - name: nome do fornecedor/kit
        - vcusto_raw: custo dos equipamentos
        - power: potência em kWp
        - modules_count: quantidade de módulos
        - modules_desc: descrição dos módulos
        - inverter_desc: descrição do inversor
        - inverter_type: tipo do inversor (string/micro)
        - freight_included: se o frete está incluso
        - freight_value: valor do frete (se não incluso)
        """
        if params is None:
            params = self.default_params.copy()
        
        # Custo total (incluindo frete se necessário)
        total_cost = kit_data['vcusto_raw']
        if not kit_data.get('freight_included', True):
            total_cost += kit_data.get('freight_value', 0)
        
        # Preço alvo inicial (margem de 40%)
        initial_price = total_cost * (1 + params['margin_target'] / 100)
        
        # Economia mensal
        monthly_savings = self.calculate_monthly_savings(kit_data['power'], params)
        
        # Ajuste do preço pelo payback
        final_price, final_payback = self.adjust_price_for_payback(initial_price, monthly_savings, params)
        
        # Estrutura de preços
        pricing = self.calculate_pricing_structure(final_price, params)
        
        # Margem final resultante
        final_margin = ((final_price / total_cost) - 1) * 100
        
        # Geração mensal estimada
        monthly_generation = (
            kit_data['power'] * 
            params['hsp'] * 
            params['days_per_month'] * 
            (params['system_efficiency'] / 100)
        )
        
        return {
            'kit_info': kit_data,
            'costs': {
                'equipment_cost': kit_data['vcusto_raw'],
                'freight_cost': kit_data.get('freight_value', 0) if not kit_data.get('freight_included', True) else 0,
                'total_cost': total_cost
            },
            'calculations': {
                'initial_price': initial_price,
                'monthly_savings': monthly_savings,
                'monthly_generation': monthly_generation,
                'final_payback_months': final_payback,
                'final_margin_percent': final_margin
            },
            'pricing': pricing,
            'parameters_used': params
        }
    
    def compare_systems(self, systems_data: List[Dict], params: Dict = None) -> List[Dict]:
        """
        Compara múltiplos sistemas e retorna as propostas ordenadas por melhor custo-benefício.
        """
        proposals = []
        
        for system in systems_data:
            proposal = self.calculate_system_proposal(system, params)
            proposals.append(proposal)
        
        # Ordenar por payback (menor primeiro)
        proposals.sort(key=lambda x: x['calculations']['final_payback_months'])
        
        # Adicionar ranking
        for i, proposal in enumerate(proposals):
            proposal['ranking'] = i + 1
            proposal['is_recommended'] = (i == 0)  # O primeiro é o recomendado
        
        return proposals


class QuickQuoteGenerator:
    """
    Gerador de orçamentos rápidos baseado no consumo residencial.
    """
    
    def __init__(self, components_db_path: str):
        with open(components_db_path, 'r', encoding='utf-8') as f:
            self.components_db = json.load(f)
        
        self.calculator = SolarCalculator()
    
    def calculate_required_power(self, monthly_consumption_kwh: float, hsp: float = 5.25, 
                                simultaneity_factor: float = 30) -> float:
        """
        Calcula a potência necessária baseada no consumo mensal.
        """
        # Ajustar consumo pelo fator de simultaneidade
        adjusted_consumption = monthly_consumption_kwh * (simultaneity_factor / 100)
        
        # Calcular potência necessária
        days_per_month = 365 / 12
        system_efficiency = 0.75
        
        required_power = adjusted_consumption / (hsp * days_per_month * system_efficiency)
        
        return required_power
    
    def select_optimal_components(self, required_power_kwp: float) -> Dict:
        """
        Seleciona os componentes otimizados para a potência necessária.
        CORRIGIDO: Agora seleciona realmente o melhor custo-benefício
        """
        # CORREÇÃO CRÍTICA: Ordenar por melhor Wp por R$ (não R$ por Wp)
        modules = sorted(self.components_db['modules'], 
                        key=lambda x: x['power_wp'] / x['price_per_unit'], 
                        reverse=True)  # Do maior para o menor (melhor custo-benefício)
        
        if not modules:
            raise ValueError("❌ Nenhum módulo disponível no banco de dados")
        
        best_module = modules[0]
        print(f"✅ Módulo selecionado: {best_module['name']} - {best_module['power_wp']}Wp por R${best_module['price_per_unit']}")
        
        # Calcular quantidade de módulos necessária
        modules_needed = math.ceil((required_power_kwp * 1000) / best_module['power_wp'])
        actual_power = (modules_needed * best_module['power_wp']) / 1000
        
        # Selecionar inversor adequado
        inverters = [inv for inv in self.components_db['inverters'] 
                    if inv['power_kw'] >= actual_power * 0.8 and inv['power_kw'] <= actual_power * 1.2]
        
        if not inverters:
            # Se não encontrar inversor na faixa, pegar o mais próximo
            inverters = sorted(self.components_db['inverters'], 
                             key=lambda x: abs(x['power_kw'] - actual_power))
        
        if not inverters:
            raise ValueError("❌ Nenhum inversor disponível no banco de dados")
        
        best_inverter = min(inverters, key=lambda x: x['price'])
        print(f"✅ Inversor selecionado: {best_inverter['name']} - {best_inverter['power_kw']}kW por R${best_inverter['price']}")
        
        # Calcular custos
        module_cost = modules_needed * best_module['price_per_unit']
        inverter_cost = best_inverter['price']
        structure_cost = modules_needed * self.components_db['structure']['cost_per_module']
        installation_cost = actual_power * self.components_db['installation']['cost_per_kwp']
        
        # Custos adicionais
        electrical_protection_cost = actual_power * self.components_db['additional_costs']['electrical_protection']['cost_per_kwp']
        project_cost = self.components_db['additional_costs']['project_approval']['fixed_cost']
        transportation_cost = actual_power * self.components_db['additional_costs']['transportation']['cost_per_kwp']
        
        # Estimativa de cabos (simplificada)
        cable_cost = modules_needed * 20  # R$ 20 por módulo em cabos
        
        total_cost = (module_cost + inverter_cost + structure_cost + 
                     installation_cost + electrical_protection_cost + 
                     project_cost + transportation_cost + cable_cost)
        
        return {
            'name': f'Orçamento Rápido - {actual_power:.2f} kWp',
            'vcusto_raw': total_cost,
            'power': actual_power,
            'modules_count': modules_needed,
            'modules_desc': f"{modules_needed}x {best_module['name']}",
            'inverter_desc': best_inverter['name'],
            'inverter_type': best_inverter['type'],
            'freight_included': True,
            'freight_value': 0,
            'cost_breakdown': {
                'modules': module_cost,
                'inverter': inverter_cost,
                'structure': structure_cost,
                'installation': installation_cost,
                'electrical_protection': electrical_protection_cost,
                'project': project_cost,
                'transportation': transportation_cost,
                'cables': cable_cost
            },
            'components_selected': {
                'module': best_module,
                'inverter': best_inverter
            }
        }
    
    def generate_quick_quote(self, monthly_consumption_kwh: float = None, 
                           bill_value: float = None, hsp: float = 5.25,
                           tariff: float = 1.10, simultaneity_factor: float = 30) -> Dict:
        """
        Gera um orçamento rápido baseado no consumo ou valor da conta.
        """
        if monthly_consumption_kwh is None and bill_value is None:
            raise ValueError("Deve fornecer consumo mensal ou valor da conta")
        
        if monthly_consumption_kwh is None:
            # Calcular consumo baseado no valor da conta
            monthly_consumption_kwh = bill_value / tariff
        
        print(f"📊 Calculando para consumo de {monthly_consumption_kwh:.0f} kWh/mês")
        
        # Calcular potência necessária
        required_power = self.calculate_required_power(monthly_consumption_kwh, hsp, simultaneity_factor)
        print(f"⚡ Potência necessária: {required_power:.2f} kWp")
        
        # Selecionar componentes
        system_data = self.select_optimal_components(required_power)
        
        # Calcular proposta
        params = self.calculator.default_params.copy()
        params.update({
            'hsp': hsp,
            'tariff': tariff,
            'simultaneity_factor': simultaneity_factor
        })
        
        proposal = self.calculator.calculate_system_proposal(system_data, params)
        
        # Adicionar informações específicas do orçamento rápido
        proposal['quick_quote_info'] = {
            'original_consumption_kwh': monthly_consumption_kwh,
            'bill_value_estimated': bill_value if bill_value else monthly_consumption_kwh * tariff,
            'power_required': required_power,
            'power_provided': system_data['power'],
            'oversizing_percent': ((system_data['power'] / required_power) - 1) * 100
        }
        
        print(f"✅ Proposta gerada com sucesso! Preço final: R${proposal['pricing']['final_price']:.2f}")
        
        return proposal