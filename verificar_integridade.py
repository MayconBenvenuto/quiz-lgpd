#!/usr/bin/env python3
"""
Script de verificação de integridade do Quiz LGPD
Executa testes básicos para garantir que o sistema está funcionando corretamente
"""

import sys
import os
import json
import traceback

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("🔍 Testando imports...")
    try:
        import flask
        import secrets
        import logging
        import uuid
        import datetime
        print("✅ Todas as dependências importadas com sucesso")
        return True
    except ImportError as e:
        print(f"❌ Erro ao importar dependências: {e}")
        return False

def test_app_creation():
    """Testa se o app Flask pode ser criado"""
    print("🔍 Testando criação do app...")
    try:
        import app
        print("✅ App Flask criado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar app: {e}")
        traceback.print_exc()
        return False

def test_quiz_data():
    """Testa a integridade dos dados do quiz"""
    print("🔍 Testando dados do quiz...")
    try:
        import app
        
        # Verificar se existem participantes
        if not app.PARTICIPANTES:
            print("❌ Lista de participantes está vazia")
            return False
        print(f"✅ {len(app.PARTICIPANTES)} participantes carregados")
        
        # Verificar se existem perguntas
        if not app.PERGUNTAS:
            print("❌ Lista de perguntas está vazia")
            return False
        print(f"✅ {len(app.PERGUNTAS)} perguntas carregadas")
        
        # Verificar estrutura das perguntas
        for i, pergunta in enumerate(app.PERGUNTAS):
            required_keys = ['pergunta', 'alternativas', 'resposta_correta']
            for key in required_keys:
                if key not in pergunta:
                    print(f"❌ Pergunta {i+1} não tem o campo '{key}'")
                    return False
            
            if len(pergunta['alternativas']) != 5:
                print(f"❌ Pergunta {i+1} não tem exatamente 5 alternativas")
                return False
            
            if not (0 <= pergunta['resposta_correta'] < 5):
                print(f"❌ Pergunta {i+1} tem resposta_correta inválida")
                return False
        
        print("✅ Estrutura dos dados do quiz está correta")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar dados do quiz: {e}")
        return False

def test_ranking_file():
    """Testa se o arquivo de ranking pode ser lido/escrito"""
    print("🔍 Testando sistema de ranking...")
    try:
        import app
        
        # Testar carregamento
        ranking = app.carregar_ranking()
        print(f"✅ Ranking carregado: {len(ranking)} registros")
        
        # Testar salvamento (backup)
        test_data = [{"test": "data"}]
        app.salvar_ranking(test_data)
        
        # Restaurar dados originais
        app.salvar_ranking(ranking)
        print("✅ Sistema de ranking funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de ranking: {e}")
        return False

def test_routes():
    """Testa se as rotas estão definidas"""
    print("🔍 Testando rotas...")
    try:
        import app
        
        expected_routes = [
            '/',
            '/iniciar_quiz',
            '/pergunta',
            '/responder',
            '/finalizar_quiz',
            '/ranking',
            '/api/ranking'
        ]
        
        # Obter rotas definidas
        routes = [str(rule.rule) for rule in app.app.url_map.iter_rules() if rule.rule != '/static/<path:filename>']
        
        for route in expected_routes:
            if route not in routes:
                print(f"❌ Rota '{route}' não encontrada")
                return False
        
        print(f"✅ Todas as {len(expected_routes)} rotas esperadas estão definidas")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar rotas: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando verificação de integridade do Quiz LGPD")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_quiz_data,
        test_ranking_file,
        test_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Erro inesperado no teste {test.__name__}: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema está funcionando corretamente.")
        return True
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
