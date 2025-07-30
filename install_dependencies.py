#!/usr/bin/env python3
"""
Script de instalação de dependências para o Processador de Vídeos do YouTube.
Este script instala automaticamente todas as dependências necessárias.
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Executa um comando e exibe o progresso."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e.stderr}")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário. Versão atual:", f"{version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def install_system_dependencies():
    """Instala dependências do sistema baseado no OS."""
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Detectado: Linux")
        # Instala FFmpeg no Ubuntu/Debian
        commands = [
            "sudo apt update",
            "sudo apt install -y ffmpeg",
            "sudo apt install -y python3-dev",
            "sudo apt install -y build-essential"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Executando: {cmd}"):
                print("⚠️  Alguns pacotes podem não ter sido instalados. Continue mesmo assim.")
                
    elif system == "darwin":  # macOS
        print("🍎 Detectado: macOS")
        # Instala FFmpeg no macOS usando Homebrew
        if not run_command("which brew", "Verificando Homebrew"):
            print("📦 Homebrew não encontrado. Instalando...")
            homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            run_command(homebrew_install, "Instalando Homebrew")
        
        run_command("brew install ffmpeg", "Instalando FFmpeg")
        
    elif system == "windows":
        print("🪟 Detectado: Windows")
        print("⚠️  No Windows, você pode precisar instalar FFmpeg manualmente.")
        print("   Baixe de: https://ffmpeg.org/download.html")
        print("   Ou use: winget install ffmpeg")
        
    else:
        print(f"❓ Sistema operacional não reconhecido: {system}")
        print("   Você pode precisar instalar FFmpeg manualmente.")

def install_python_dependencies():
    """Instala dependências Python."""
    print("🐍 Instalando dependências Python...")
    
    # Atualiza pip primeiro
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Atualizando pip")
    
    # Instala PyTorch primeiro (pode ser necessário versão específica)
    if not run_command(f"{sys.executable} -m pip install torch torchvision torchaudio", "Instalando PyTorch"):
        print("⚠️  Erro ao instalar PyTorch. Tentando versão CPU...")
        run_command(f"{sys.executable} -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu", "Instalando PyTorch (CPU)")
    
    # Instala outras dependências
    if os.path.exists("requirements.txt"):
        run_command(f"{sys.executable} -m pip install -r requirements.txt", "Instalando dependências do requirements.txt")
    else:
        # Instala dependências individuais se requirements.txt não existir
        dependencies = [
            "yt-dlp>=2023.12.30",
            "openai-whisper>=20231117",
            "googletrans==4.0.0rc1",
            "nltk>=3.8.1",
            "beautifulsoup4>=4.12.2",
            "requests>=2.31.0",
            "python-dotenv>=1.0.0",
            "pydub>=0.25.1",
            "transformers>=4.36.0",
            "sentence-transformers>=2.2.2",
            "langdetect>=1.0.9",
            "regex>=2023.10.3"
        ]
        
        for dep in dependencies:
            run_command(f"{sys.executable} -m pip install '{dep}'", f"Instalando {dep.split('>=')[0]}")

def download_nltk_data():
    """Baixa dados necessários do NLTK."""
    print("📚 Baixando dados do NLTK...")
    
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ Dados do NLTK baixados!")
    except Exception as e:
        print(f"⚠️  Erro ao baixar dados do NLTK: {e}")

def test_installation():
    """Testa se a instalação foi bem-sucedida."""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testa importações principais
        import yt_dlp
        print("✅ yt-dlp - OK")
        
        import whisper
        print("✅ whisper - OK")
        
        import googletrans
        print("✅ googletrans - OK")
        
        import nltk
        print("✅ nltk - OK")
        
        import torch
        print("✅ torch - OK")
        
        # Testa se consegue importar o processador
        from youtube_processor import YouTubeVideoProcessor
        print("✅ YouTubeVideoProcessor - OK")
        
        print("\n🎉 Todas as dependências estão funcionando!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False

def main():
    """Função principal de instalação."""
    print("🚀 INSTALADOR DO PROCESSADOR DE VÍDEOS DO YOUTUBE")
    print("=" * 60)
    
    # Verifica versão do Python
    if not check_python_version():
        return
    
    # Pergunta ao usuário o que fazer
    print("\nO que você gostaria de instalar?")
    print("1. Tudo (recomendado)")
    print("2. Apenas dependências Python")
    print("3. Apenas dependências do sistema")
    print("4. Testar instalação existente")
    
    escolha = input("\nDigite sua escolha (1-4): ").strip()
    
    if escolha in ["1", ""]:  # Default é tudo
        print("\n📦 Instalando tudo...")
        install_system_dependencies()
        install_python_dependencies()
        download_nltk_data()
        test_installation()
        
    elif escolha == "2":
        install_python_dependencies()
        download_nltk_data()
        test_installation()
        
    elif escolha == "3":
        install_system_dependencies()
        
    elif escolha == "4":
        test_installation()
        
    else:
        print("❌ Escolha inválida.")
        return
    
    print("\n" + "=" * 60)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Execute: python example_usage.py")
    print("2. Ou importe: from youtube_processor import YouTubeVideoProcessor")
    print("3. Consulte o README.md para mais informações")
    print("\n✨ Instalação concluída!")

if __name__ == "__main__":
    main()