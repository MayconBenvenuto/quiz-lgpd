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

# Não há mais lista pré-definida de participantes
# Os usuários podem inserir seu próprio nome e sobrenome

# Perguntas do quiz sobre Medsenior
PERGUNTAS = [
    {
        "pergunta": "Qual é o tempo de carência normal para internações clínicas, cirúrgicas e UTI na Medsenior?",
        "alternativas": [
            "180 dias",
            "120 dias",
            "90 dias",
            "60 dias"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "Qual é a especialidade principal da Medsenior?",
        "alternativas": [
            "Planos de saúde para empresas",
            "Consultoria médica",
            "Planos de saúde para idosos",
            "Medicina preventiva"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "A partir de qual idade é possível contratar um plano Medsenior?",
        "alternativas": [
            "50 anos",
            "55 anos",
            "60 anos",
            "65 anos"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual é o principal diferencial da Medsenior no mercado?",
        "alternativas": [
            "Preços mais baixos",
            "Atendimento especializado para a terceira idade",
            "Cobertura internacional",
            "Consultas online"
        ],
        "resposta_correta": 1
    },
    {
        "pergunta": "Qual é o tempo de carência para consultas médicas na Medsenior?",
        "alternativas": [
            "Não há carência",
            "30 dias",
            "60 dias",
            "90 dias"
        ],
        "resposta_correta": 0
    },
    {
        "pergunta": "A Medsenior oferece cobertura para:",
        "alternativas": [
            "Apenas consultas",
            "Consultas e exames",
            "Cobertura hospitalar completa",
            "Apenas emergências"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "Qual é o tempo de carência para partos na Medsenior?",
        "alternativas": [
            "180 dias",
            "240 dias",
            "300 dias",
            "Não se aplica ao público-alvo"
        ],
        "resposta_correta": 3
    },
    {
        "pergunta": "A Medsenior possui rede própria ou credenciada?",
        "alternativas": [
            "Apenas rede própria",
            "Apenas rede credenciada",
            "Ambas - rede própria e credenciada",
            "Não possui rede"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "Qual é o foco principal dos serviços da Medsenior?",
        "alternativas": [
            "Medicina esportiva",
            "Pediatria",
            "Geriatria e cuidados com idosos",
            "Medicina do trabalho"
        ],
        "resposta_correta": 2
    },
    {
        "pergunta": "A Medsenior oferece cobertura para procedimentos de alta complexidade?",
        "alternativas": [
            "Não oferece",
            "Apenas para emergências",
            "Sim, conforme ANS",
            "Apenas com coparticipação"
        ],
        "resposta_correta": 2
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
    return render_template('index_novo.html')

@app.route('/iniciar_quiz', methods=['POST'])
def iniciar_quiz():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'erro': 'Dados não fornecidos'}), 400
            
        participante = data.get('participante', '').strip()
        logger.info(f"Tentativa de iniciar quiz: {participante}")
        
        if not participante:
            return jsonify({'erro': 'Nome completo é obrigatório'}), 400
        
        # Validar se o nome tem pelo menos nome e sobrenome
        palavras = participante.split()
        if len(palavras) < 2:
            return jsonify({'erro': 'Por favor, informe nome e sobrenome completos'}), 400
        
        # Validar se contém apenas letras, espaços e acentos
        import re
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', participante):
            return jsonify({'erro': 'Nome deve conter apenas letras'}), 400
        
        # Validar tamanho mínimo e máximo
        if len(participante) < 5:
            return jsonify({'erro': 'Nome muito curto'}), 400
        if len(participante) > 100:
            return jsonify({'erro': 'Nome muito longo'}), 400
        
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