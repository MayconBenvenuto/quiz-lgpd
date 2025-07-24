# Quiz Medsenior

Sistema de quiz interativo sobre planos de saúde especializados para a terceira idade desenvolvido em Python Flask.

## ✨ Funcionalidades

- ✅ Seleção de participante de lista pré-definida
- ✅ 10 perguntas sobre a Medsenior com 5 alternativas cada
- ✅ Timer de 60 segundos por pergunta
- ✅ Sistema de pontuação baseado na velocidade de resposta
- ✅ Feedback imediato (acerto/erro com resposta correta)
- ✅ Ranking em tempo real
- ✅ Interface responsiva e moderna
- ✅ Estatísticas gerais dos participantes
- ✅ Sistema de logging para monitoramento
- ✅ Backup automático do ranking
- ✅ Headers de segurança implementados

## 🔒 Melhorias de Segurança Implementadas

- ✅ Chave secreta dinâmica baseada em variável de ambiente
- ✅ Validação de entrada em todos os endpoints
- ✅ Headers de segurança (XSS Protection, Content Type Options, etc.)
- ✅ Tratamento de erros robusto
- ✅ Logging de segurança
- ✅ Validação de participantes contra lista permitida
- ✅ Sessões seguras com timeout

## 👥 Como Participar

Não há mais lista pré-definida de participantes. Qualquer pessoa pode participar do quiz:

**Requisitos para o nome:**
- Nome e sobrenome completos são obrigatórios
- Mínimo de 5 caracteres
- Máximo de 100 caracteres
- Apenas letras, espaços e acentos são permitidos
- Não são permitidos números ou caracteres especiais

**Exemplo de nomes válidos:**
- João Silva
- Maria Santos
- Ana Paula Costa
- José dos Santos

**Exemplos de nomes inválidos:**
- João (apenas um nome)
- João123 (contém números)
- J.Silva (contém pontos)

## Como Executar

### 1. Instalar Python
Certifique-se de ter Python 3.7+ instalado.

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o Aplicativo
```bash
python app.py
```

### 4. Acessar o Sistema
Abra seu navegador e acesse: http://localhost:5000

## Estrutura do Projeto

```
quiz-lgpd/
├── app.py                 # Aplicativo Flask principal
├── requirements.txt       # Dependências Python
├── ranking.json          # Arquivo gerado automaticamente com resultados
├── templates/
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial e quiz
│   └── ranking.html      # Página de ranking
└── README.md             # Este arquivo
```

## Como Funciona

1. **Início**: Participante seleciona seu nome da lista
2. **Quiz**: 10 perguntas com 60 segundos cada
3. **Pontuação**: Baseada na velocidade de resposta (máximo 100 pontos por pergunta)
4. **Resultado**: Feedback imediato após cada resposta
5. **Ranking**: Visualização em tempo real da classificação

## Temas das Perguntas

- Conceitos básicos da LGPD
- Bases legais para tratamento de dados
- Direitos dos titulares
- Dados pessoais sensíveis
- Penalidades e multas
- Princípios da LGPD
- Papel do DPO (Data Protection Officer)
- Aplicabilidade da lei

## Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **UI Framework**: Bootstrap 5
- **Ícones**: Font Awesome 6
- **Armazenamento**: JSON (para ranking)

## Recursos Visuais

- Design moderno com gradientes
- Interface responsiva para diferentes dispositivos
- Animações e transições suaves
- Timer visual com alerta nos últimos 10 segundos
- Cores diferenciadas para respostas corretas/incorretas
- Ranking com destaque para os primeiros colocados
- Estatísticas gerais dos participantes

## Personalização

Para adicionar mais perguntas, edite a lista `PERGUNTAS` no arquivo `app.py`.
Para modificar participantes, edite a lista `PARTICIPANTES` no mesmo arquivo.

## Suporte

Sistema desenvolvido para a Universidade Belz como ferramenta de treinamento em LGPD.
