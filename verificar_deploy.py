#!/usr/bin/env python3
"""
Script de Verificação Pré-Deploy para Render
Verifica se todos os arquivos necessários estão presentes e corretos
"""

import os
import json
import sys

def check_file_exists(filename, description):
    """Verifica se um arquivo existe"""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description} não encontrado: {filename}")
        return False

def check_render_yaml():
    """Verifica se o render.yaml está correto"""
    if not os.path.exists('render.yaml'):
        print("❌ render.yaml não encontrado")
        return False
    
    with open('render.yaml', 'r') as f:
        content = f.read()
        
    required_items = [
        'type: web',
        'runtime: python3',
        'buildCommand: pip install -r requirements_deploy.txt',
        'gunicorn app:app',
        'SECRET_KEY'
    ]
    
    for item in required_items:
        if item not in content:
            print(f"❌ render.yaml está faltando: {item}")
            return False
    
    print("✅ render.yaml está correto")
    return True

def check_requirements():
    """Verifica se requirements_deploy.txt tem as dependências necessárias"""
    if not os.path.exists('requirements_deploy.txt'):
        print("❌ requirements_deploy.txt não encontrado")
        return False
    
    with open('requirements_deploy.txt', 'r') as f:
        content = f.read()
    
    required_packages = ['Flask', 'gunicorn', 'Werkzeug']
    
    for package in required_packages:
        if package not in content:
            print(f"❌ requirements_deploy.txt está faltando: {package}")
            return False
    
    print("✅ requirements_deploy.txt está correto")
    return True

def check_app_structure():
    """Verifica a estrutura básica do app"""
    try:
        import app
        
        # Verificar se as variáveis necessárias existem
        if not hasattr(app, 'PARTICIPANTES') or not app.PARTICIPANTES:
            print("❌ Lista de participantes vazia ou não encontrada")
            return False
        
        if not hasattr(app, 'PERGUNTAS') or not app.PERGUNTAS:
            print("❌ Lista de perguntas vazia ou não encontrada")
            return False
        
        if len(app.PERGUNTAS) != 10:
            print(f"❌ Número incorreto de perguntas: {len(app.PERGUNTAS)} (esperado: 10)")
            return False
        
        print(f"✅ App estruturado corretamente: {len(app.PARTICIPANTES)} participantes, {len(app.PERGUNTAS)} perguntas")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar app: {e}")
        return False

def check_git_status():
    """Verifica se o repositório Git está atualizado"""
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("⚠️  Há mudanças não commitadas:")
            print(result.stdout)
            print("💡 Execute: git add . && git commit -m 'Preparado para deploy' && git push")
            return False
        else:
            print("✅ Repositório Git está atualizado")
            return True
            
    except subprocess.CalledProcessError:
        print("⚠️  Não foi possível verificar status do Git")
        return True  # Não é um erro crítico
    except FileNotFoundError:
        print("⚠️  Git não encontrado no sistema")
        return True  # Não é um erro crítico

def main():
    """Executa todas as verificações pré-deploy"""
    print("🚀 Verificação Pré-Deploy para Render")
    print("=" * 50)
    
    checks = [
        (lambda: check_file_exists('app.py', 'Arquivo principal da aplicação'), True),
        (lambda: check_file_exists('requirements_deploy.txt', 'Dependências para produção'), True),
        (lambda: check_file_exists('runtime.txt', 'Versão do Python'), True),
        (lambda: check_file_exists('render.yaml', 'Configuração do Render'), True),
        (lambda: check_file_exists('templates/index_novo.html', 'Template principal'), True),
        (lambda: check_file_exists('templates/ranking_novo.html', 'Template de ranking'), True),
        (lambda: check_file_exists('templates/base_novo.html', 'Template base'), True),
        (check_render_yaml, True),
        (check_requirements, True),
        (check_app_structure, True),
        (check_git_status, False)  # Não crítico
    ]
    
    passed = 0
    critical_failed = 0
    
    for check_func, is_critical in checks:
        try:
            if check_func():
                passed += 1
            elif is_critical:
                critical_failed += 1
        except Exception as e:
            print(f"❌ Erro inesperado na verificação: {e}")
            if is_critical:
                critical_failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultado: {passed}/{len(checks)} verificações passaram")
    
    if critical_failed == 0:
        print("🎉 PROJETO PRONTO PARA DEPLOY!")
        print("\n🚀 Próximos passos:")
        print("1. Acesse https://render.com")
        print("2. Clique em 'New' → 'Web Service'")
        print("3. Conecte seu repositório GitHub")
        print("4. Selecione este repositório")
        print("5. O Render detectará automaticamente o render.yaml")
        print("6. Clique em 'Create Web Service'")
        print("7. Aguarde o deploy (2-5 minutos)")
        print("\n🌐 Após o deploy, sua URL será:")
        print("https://quiz-lgpd-belz.onrender.com")
        return True
    else:
        print(f"⚠️  {critical_failed} verificações críticas falharam!")
        print("Corrija os problemas acima antes de fazer deploy.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
