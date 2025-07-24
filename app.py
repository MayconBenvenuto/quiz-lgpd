from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
import uuid
import secrets
import logging

app = Flask(__name__)
# Usar uma chave secreta mais segura
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações de sessão e segurança
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora

# Lista de participantes
PARTICIPANTES = [
    "Maycon – Desenvolvedor/Tester",
    "Viviane Pereira Pinto – Implantação",
    "Ellen Conceição de Oliveira – Movimentação Consultores",
    "Tuanny Luiza Santos – Implantação",
    "Josemir – Envio de Boletos, Atendimento ao Cliente",
    "Fabiana Ramalho – Supervisora de Marketing",
    "Maria Eduarda Vasconcelos dos Santos – Assistente de Marketing",
    "Mayara Lima – Coordenadora Equipe Operacional, Implantação Grandes Empresas",
    "Michele Verçosa – Supervisora Movimentação, Relacionamento com Grandes Empresas",
    "Josenilda Ribeiro de Menezes – Gestora de Saúde e Segurança do Trabalho",
    "Elton Albuquerque – COO",
    "Ricardo Belz – CFO",
    "Raphael Belz – CEO",
    "Bruno Vilela – Head Conecta Saúde"
]

# Perguntas do quiz sobre LGPD
PERGUNTAS = [
    {
        "pergunta": "O que significa a sigla LGPD?",
        "alternativas": [
            "Lei Geral de Proteção de Dados",
            "Lei Geral de Privacidade Digital",
            "Lei de Gestão de Proteção de Dados",
            "Lei Geral de Procedimentos Digitais",
            "Lei de Governança de Proteção Digital"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual é o prazo máximo para notificar a ANPD sobre incidentes de segurança?",
        "alternativas": [
            "24 horas",
            "48 horas",
            "72 horas",
            "7 dias",
            "15 dias"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual das seguintes NÃO é uma base legal para tratamento de dados pessoais?",
        "alternativas": [
            "Consentimento do titular",
            "Cumprimento de obrigação legal",
            "Interesse legítimo",
            "Proteção da vida",
            "Curiosidade empresarial"
        ],
        "resposta_correta": 4
    },
    {
        "pergunta": "O que são dados pessoais sensíveis segundo a LGPD?",
        "alternativas": [
            "Dados que podem causar danos financeiros",
            "Dados sobre origem racial, convicções religiosas, dados genéticos, biométricos, etc.",
            "Dados bancários e financeiros",
            "Dados de localização geográfica",
            "Dados de navegação na internet"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual é a multa máxima prevista na LGPD?",
        "alternativas": [
            "R$ 10 milhões",
            "R$ 25 milhões",
            "R$ 50 milhões",
            "R$ 100 milhões",
            "R$ 200 milhões"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "O que é o princípio da minimização na LGPD?",
        "alternativas": [
            "Reduzir o tempo de armazenamento",
            "Coletar apenas dados necessários para a finalidade",
            "Minimizar custos de implementação",
            "Reduzir o número de funcionários com acesso",
            "Minimizar riscos de vazamento"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual direito o titular dos dados NÃO possui segundo a LGPD?",
        "alternativas": [
            "Acesso aos seus dados",
            "Correção de dados incompletos",
            "Eliminação de dados desnecessários",
            "Portabilidade dos dados",
            "Venda dos próprios dados"
        ],
        "resposta_correta": 4
    },
    {
        "pergunta": "O que é o DPO (Data Protection Officer)?",
        "alternativas": [
            "Um software de proteção",
            "Encarregado de proteção de dados",
            "Departamento de proteção online",
            "Documento de política organizacional",
            "Dispositivo de proteção operacional"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "A LGPD se aplica a:",
        "alternativas": [
            "Apenas empresas públicas",
            "Apenas empresas privadas",
            "Apenas empresas com mais de 100 funcionários",
            "Toda organização que trata dados pessoais",
            "Apenas empresas de tecnologia"
        ],
        "resposta_correta": 3
    },
    {
        "pergunta": "Qual é o período de adaptação que as empresas tiveram para se adequar à LGPD?",
        "alternativas": [
            "A lei entrou em vigor imediatamente",
            "6 meses após a publicação",
            "1 ano após a publicação",
            "2 anos após a publicação",
            "3 anos após a publicação"
        ],
        "resposta_correta": 3
    }
]

def carregar_ranking():
    """Carrega o ranking do arquivo JSON com tratamento de erro"""
    try:
        if os.path.exists('ranking.json'):
            with open('ranking.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Ranking carregado com {len(data)} registros")
                return data
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Erro ao carregar ranking: {e}")
    return []

def salvar_ranking(dados):
    """Salva o ranking no arquivo JSON com tratamento de erro"""
    try:
        # Criar backup do arquivo existente
        if os.path.exists('ranking.json'):
            import shutil
            shutil.copy2('ranking.json', 'ranking_backup.json')
        
        with open('ranking.json', 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        logger.info(f"Ranking salvo com {len(dados)} registros")
    except IOError as e:
        logger.error(f"Erro ao salvar ranking: {e}")
        raise

@app.after_request
def after_request(response):
    """Adiciona headers de segurança"""
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

@app.route('/')
def index():
    return render_template('index_novo.html', participantes=PARTICIPANTES)

@app.route('/iniciar_quiz', methods=['POST'])
def iniciar_quiz():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não fornecidos'}), 400
            
        participante = data.get('participante', '').strip()
        logger.info(f"Tentativa de iniciar quiz: {participante}")
        
        if not participante:
            return jsonify({'erro': 'Participante não selecionado'}), 400
        
        # Validar se o participante está na lista permitida
        if participante not in PARTICIPANTES:
            return jsonify({'erro': 'Participante não válido'}), 400
        
        # Inicializar sessão
        session.permanent = True
        session['participante'] = participante
        session['pergunta_atual'] = 0
        session['pontuacao'] = 0
        session['respostas'] = []
        session['quiz_id'] = str(uuid.uuid4())
        session['inicio_quiz'] = datetime.now().isoformat()
        
        logger.info(f"Quiz iniciado para: {participante} - ID: {session['quiz_id']}")
        
        return jsonify({'sucesso': True})
        
    except Exception as e:
        logger.error(f"Erro ao iniciar quiz: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/pergunta')
def obter_pergunta():
    try:
        if 'participante' not in session:
            logger.warning("Tentativa de acesso sem sessão válida")
            return jsonify({'erro': 'Sessão não iniciada'}), 401
        
        pergunta_atual = session.get('pergunta_atual', 0)
        logger.info(f"Solicitando pergunta {pergunta_atual + 1} para {session['participante']}")
        
        if pergunta_atual >= len(PERGUNTAS):
            return jsonify({'quiz_finalizado': True})
        
        pergunta = PERGUNTAS[pergunta_atual].copy()
        # Remove a resposta correta do retorno
        pergunta.pop('resposta_correta', None)
        pergunta['numero'] = pergunta_atual + 1
        pergunta['total'] = len(PERGUNTAS)
        
        return jsonify(pergunta)
        
    except Exception as e:
        logger.error(f"Erro ao obter pergunta: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/responder', methods=['POST'])
def responder_pergunta():
    try:
        if 'participante' not in session:
            return jsonify({'erro': 'Sessão não iniciada'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não fornecidos'}), 400
            
        resposta = data.get('resposta')
        tempo_restante = data.get('tempo_restante', 0)
        
        # Validar resposta
        if resposta is None or not isinstance(resposta, int):
            return jsonify({'erro': 'Resposta inválida'}), 400
        
        pergunta_atual = session.get('pergunta_atual', 0)
        
        if pergunta_atual >= len(PERGUNTAS):
            return jsonify({'erro': 'Quiz já finalizado'}), 400
        
        pergunta = PERGUNTAS[pergunta_atual]
        resposta_correta = pergunta['resposta_correta']
        
        # Validar índice da resposta
        if resposta < 0 or resposta >= len(pergunta['alternativas']):
            return jsonify({'erro': 'Índice de resposta inválido'}), 400
        
        acertou = resposta == resposta_correta
        if acertou:
            # Pontuação baseada no tempo restante (máximo 100 pontos)
            pontos = max(10, int(tempo_restante * 1.5))
            session['pontuacao'] += pontos
        else:
            pontos = 0
        
        # Salvar resposta
        session['respostas'].append({
            'pergunta': pergunta_atual,
            'resposta_usuario': resposta,
            'resposta_correta': resposta_correta,
            'acertou': acertou,
            'pontos': pontos,
            'tempo_resposta': 60 - tempo_restante
        })
        
        resultado = {
            'acertou': acertou,
            'resposta_correta': resposta_correta,
            'alternativa_correta': pergunta['alternativas'][resposta_correta],
            'pontos_ganhos': pontos,
            'pontuacao_total': session['pontuacao']
        }
        
        # Avançar para próxima pergunta
        session['pergunta_atual'] += 1
        
        logger.info(f"Resposta processada para {session['participante']}: P{pergunta_atual + 1} - {'Correto' if acertou else 'Incorreto'}")
        
        return jsonify(resultado)
        
    except Exception as e:
        logger.error(f"Erro ao processar resposta: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/finalizar_quiz', methods=['POST'])
def finalizar_quiz():
    try:
        if 'participante' not in session:
            return jsonify({'erro': 'Sessão não iniciada'}), 401
        
        # Salvar resultado no ranking
        ranking = carregar_ranking()
        
        resultado = {
            'participante': session['participante'],
            'pontuacao': session['pontuacao'],
            'data_hora': datetime.now().isoformat(),
            'acertos': sum(1 for r in session['respostas'] if r['acertou']),
            'total_perguntas': len(PERGUNTAS),
            'quiz_id': session.get('quiz_id', ''),
            'duracao_quiz': datetime.now().isoformat()  # Poderia calcular tempo total
        }
        
        ranking.append(resultado)
        
        # Ordenar ranking por pontuação (decrescente)
        ranking.sort(key=lambda x: x['pontuacao'], reverse=True)
        
        # Limitar ranking a últimos 100 resultados para evitar arquivo muito grande
        if len(ranking) > 100:
            ranking = ranking[:100]
        
        salvar_ranking(ranking)
        
        logger.info(f"Quiz finalizado para {session['participante']}: {resultado['acertos']}/{resultado['total_perguntas']} - {resultado['pontuacao']} pontos")
        
        # Dados para retorno (antes de limpar sessão)
        resultado_retorno = {
            'pontuacao_final': resultado['pontuacao'],
            'acertos': resultado['acertos'],
            'total_perguntas': resultado['total_perguntas']
        }
        
        # Limpar sessão
        session.clear()
        
        return jsonify(resultado_retorno)
        
    except Exception as e:
        logger.error(f"Erro ao finalizar quiz: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.route('/ranking')
def ver_ranking():
    ranking = carregar_ranking()
    return render_template('ranking_novo.html', ranking=ranking)

@app.route('/api/ranking')
def api_ranking():
    try:
        ranking = carregar_ranking()
        return jsonify(ranking)
    except Exception as e:
        logger.error(f"Erro ao obter ranking via API: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

# Handlers de erro globais
@app.errorhandler(404)
def not_found(error):
    return render_template('base_novo.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro interno: {error}")
    return jsonify({'erro': 'Erro interno do servidor'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Exceção não tratada: {e}")
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    # Configuração para produção
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)