#!/usr/bin/env python3
"""
Exemplo de uso do processador de vídeos do YouTube.
Este script demonstra como usar a classe YouTubeVideoProcessor para processar um vídeo.
"""

from youtube_processor import YouTubeVideoProcessor
import json

def main():
    """Exemplo prático de processamento de vídeo."""
    
    # URL do vídeo para processar
    # Substitua pela URL desejada
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("🎬 Processador de Vídeos do YouTube")
    print("=" * 50)
    
    # Permite ao usuário inserir uma URL personalizada
    custom_url = input(f"Digite a URL do vídeo (ou Enter para usar exemplo): ").strip()
    if custom_url:
        video_url = custom_url
    
    print(f"\n📹 Processando: {video_url}")
    print("⏳ Isso pode levar alguns minutos dependendo da duração do vídeo...")
    
    try:
        # Inicializa o processador
        # Modelos disponíveis: 'tiny', 'base', 'small', 'medium', 'large'
        # 'base' oferece boa qualidade com velocidade razoável
        processor = YouTubeVideoProcessor(whisper_model="base")
        
        # Processa o vídeo
        resultado = processor.process_video(video_url)
        
        # Verifica se houve erro
        if "erro" in resultado:
            print(f"❌ Erro no processamento: {resultado['erro']}")
            return
        
        # Salva o resultado completo
        nome_arquivo = "resultado_completo.json"
        processor.save_result(resultado, nome_arquivo)
        
        # Exibe resumo do processamento
        print("\n" + "=" * 50)
        print("✅ PROCESSAMENTO CONCLUÍDO!")
        print("=" * 50)
        
        video_info = resultado['video']
        modos = resultado['modos']
        
        print(f"📹 Título: {video_info['titulo_detectado']}")
        print(f"⏱️  Duração: {video_info['duracao_minutos']} minutos")
        print(f"🌐 Idioma: {video_info['idioma_origem']} → {video_info['traduzido_para']}")
        print(f"📊 Qualidade da transcrição: {video_info['qualidade_transcricao']}")
        print(f"💬 Motivo: {video_info['motivo_qualidade']}")
        
        print(f"\n📝 RESULTADOS:")
        print(f"   • Transcrição: {len(modos['transcricao']['blocos'])} blocos de texto")
        print(f"   • Insights: {len(modos['insights'])} insights extraídos")
        print(f"   • Clippings: {len(modos['clippings'])} frases de impacto")
        print(f"   • Conteúdo: Blog, headlines e post social gerados")
        
        # Mostra alguns exemplos dos resultados
        print(f"\n🎯 EXEMPLOS DE RESULTADOS:")
        print("-" * 30)
        
        # Exemplo de insight
        if modos['insights']:
            insight = modos['insights'][0]
            print(f"💡 Primeiro Insight:")
            print(f"   Nome: {insight['nome']}")
            print(f"   Tipo: {insight['tipo']}")
            print(f"   Timestamp: {insight['timestamp']}")
            print(f"   Descrição: {insight['descricao'][:100]}...")
        
        # Exemplo de clipping
        if modos['clippings']:
            clipping = modos['clippings'][0]
            print(f"\n🎬 Primeira Frase de Impacto:")
            print(f"   Frase: \"{clipping['frase']}\"")
            print(f"   Emoção: {clipping['emocao']}")
            print(f"   Timestamp: {clipping['timestamp']}")
        
        # Conteúdo gerado
        conteudo = modos['conteudo']
        print(f"\n📰 Conteúdo Gerado:")
        print(f"   Blog Título: {conteudo['blog_titulo']}")
        print(f"   Headline Clickbait: {conteudo['headlines']['clickbait']}")
        
        print(f"\n💾 Resultado completo salvo em: {nome_arquivo}")
        print("\n🎉 Processamento finalizado com sucesso!")
        
        # Opção de visualizar o JSON completo
        visualizar = input("\nDeseja visualizar o JSON completo? (s/N): ").strip().lower()
        if visualizar in ['s', 'sim', 'y', 'yes']:
            print("\n" + "=" * 60)
            print("JSON COMPLETO:")
            print("=" * 60)
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Processamento interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        print("Verifique se todas as dependências estão instaladas corretamente.")

def exemplo_batch():
    """Exemplo de processamento em lote de múltiplos vídeos."""
    print("\n🔄 EXEMPLO DE PROCESSAMENTO EM LOTE")
    print("=" * 50)
    
    # Lista de URLs para processar
    urls = [
        "https://www.youtube.com/watch?v=exemplo1",
        "https://www.youtube.com/watch?v=exemplo2",
        # Adicione mais URLs conforme necessário
    ]
    
    processor = YouTubeVideoProcessor(whisper_model="base")
    
    for i, url in enumerate(urls, 1):
        print(f"\n📹 Processando vídeo {i}/{len(urls)}: {url}")
        
        try:
            resultado = processor.process_video(url)
            
            if "erro" not in resultado:
                nome_arquivo = f"resultado_video_{i}.json"
                processor.save_result(resultado, nome_arquivo)
                print(f"✅ Vídeo {i} processado e salvo em {nome_arquivo}")
            else:
                print(f"❌ Erro no vídeo {i}: {resultado['erro']}")
                
        except Exception as e:
            print(f"❌ Erro inesperado no vídeo {i}: {str(e)}")
    
    print(f"\n🎉 Processamento em lote finalizado!")

if __name__ == "__main__":
    print("Escolha o modo de operação:")
    print("1. Processar um vídeo")
    print("2. Exemplo de processamento em lote")
    
    escolha = input("Digite sua escolha (1 ou 2): ").strip()
    
    if escolha == "2":
        exemplo_batch()
    else:
        main()