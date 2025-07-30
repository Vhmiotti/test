#!/usr/bin/env python3
"""
Script de teste e demonstração do Processador de Vídeos do YouTube.
Este arquivo mostra um exemplo de saída JSON estruturada.
"""

import json
from datetime import datetime

def create_example_output():
    """Cria um exemplo de saída JSON para demonstração."""
    
    example_result = {
        "video": {
            "url": "https://www.youtube.com/watch?v=exemplo123",
            "titulo_detectado": "Como Desenvolver Disciplina Pessoal em 30 Dias",
            "idioma_origem": "pt",
            "traduzido_para": "pt",
            "duracao_minutos": 12.4,
            "qualidade_transcricao": "alta",
            "motivo_qualidade": "áudio limpo, fala clara e pausas bem definidas",
            "uploader": "Canal Produtividade",
            "upload_date": "20241201",
            "view_count": 45230
        },
        "modos": {
            "transcricao": {
                "srt": """1
00:00:01,000 --> 00:00:05,500
Hoje vamos falar sobre como desenvolver disciplina pessoal de forma prática.

2
00:00:05,500 --> 00:00:10,200
A disciplina não é sobre força de vontade, mas sobre sistemas inteligentes.

3
00:00:10,200 --> 00:00:15,800
Vou compartilhar três estratégias que mudaram completamente minha rotina.

4
00:00:15,800 --> 00:00:20,100
A primeira estratégia é a regra dos dois minutos.""",
                "blocos": [
                    {
                        "start": "00:00:01,000",
                        "end": "00:00:05,500",
                        "speaker": "Speaker 1",
                        "text": "Hoje vamos falar sobre como desenvolver disciplina pessoal de forma prática."
                    },
                    {
                        "start": "00:00:05,500",
                        "end": "00:00:10,200",
                        "speaker": "Speaker 1",
                        "text": "A disciplina não é sobre força de vontade, mas sobre sistemas inteligentes."
                    },
                    {
                        "start": "00:00:10,200",
                        "end": "00:00:15,800",
                        "speaker": "Speaker 1",
                        "text": "Vou compartilhar três estratégias que mudaram completamente minha rotina."
                    },
                    {
                        "start": "00:00:15,800",
                        "end": "00:00:20,100",
                        "speaker": "Speaker 1",
                        "text": "A primeira estratégia é a regra dos dois minutos."
                    }
                ]
            },
            "insights": [
                {
                    "nome": "Regra dos Dois Minutos",
                    "tipo": "ação imediata",
                    "timestamp": "00:01:15",
                    "descricao": "Se uma tarefa leva menos de dois minutos para ser concluída, faça imediatamente ao invés de adiar. Isso evita acúmulo de pequenas tarefas."
                },
                {
                    "nome": "Sistema de Recompensas",
                    "tipo": "motivacional",
                    "timestamp": "00:03:42",
                    "descricao": "Crie um sistema de recompensas pequenas para cada meta atingida. O cérebro precisa de feedback positivo para manter novos hábitos."
                },
                {
                    "nome": "Ambiente de Sucesso",
                    "tipo": "técnico",
                    "timestamp": "00:05:20",
                    "descricao": "Modifique seu ambiente físico para facilitar bons hábitos e dificultar os ruins. O ambiente é mais forte que a motivação."
                },
                {
                    "nome": "Princípio da Consistência",
                    "tipo": "conceitual",
                    "timestamp": "00:07:10",
                    "descricao": "Consistência supera intensidade. É melhor fazer 10 minutos todos os dias do que 2 horas uma vez por semana."
                },
                {
                    "nome": "Tracking Visual",
                    "tipo": "técnico",
                    "timestamp": "00:09:30",
                    "descricao": "Use um calendário ou app para marcar visualmente seus progressos. Ver a sequência de sucessos motiva a continuar."
                }
            ],
            "clippings": [
                {
                    "frase": "A disciplina é a forma mais pura de liberdade.",
                    "timestamp": "00:02:18",
                    "emocao": "inspiração",
                    "contexto": "Contexto do momento no vídeo: Após explicar como hábitos libertam a mente da decisão constante sobre o que fazer..."
                },
                {
                    "frase": "Você não precisa de motivação, você precisa de um sistema.",
                    "timestamp": "00:04:45",
                    "emocao": "crítica",
                    "contexto": "Contexto do momento no vídeo: Criticando a dependência de motivação para manter hábitos saudáveis..."
                },
                {
                    "frase": "Comece tão pequeno que seja impossível falhar.",
                    "timestamp": "00:06:12",
                    "emocao": "esperança",
                    "contexto": "Contexto do momento no vídeo: Explicando como começar com micro-hábitos para garantir sucesso inicial..."
                },
                {
                    "frase": "O que você faz hoje determina quem você será amanhã.",
                    "timestamp": "00:08:33",
                    "emocao": "urgência",
                    "contexto": "Contexto do momento no vídeo: Enfatizando a importância de ações diárias na formação da identidade..."
                },
                {
                    "frase": "Seus hábitos são votos para o tipo de pessoa que você quer ser.",
                    "timestamp": "00:11:15",
                    "emocao": "inspiração",
                    "contexto": "Contexto do momento no vídeo: Conclusão sobre como cada ação pequena contribui para a identidade desejada..."
                }
            ],
            "conteudo": {
                "resumo": "Neste vídeo, o autor apresenta estratégias práticas para desenvolver disciplina pessoal baseadas em sistemas ao invés de motivação. Ele explica a regra dos dois minutos, a importância do ambiente e como usar recompensas para manter novos hábitos. O foco está em consistência e pequenas ações diárias que, acumuladas, geram grandes transformações na vida pessoal e profissional.",
                "blog_titulo": "Como desenvolver disciplina pessoal em 30 dias: guia prático e completo",
                "headlines": {
                    "clickbait": "Você nunca mais vai procrastinar depois de conhecer estas 3 estratégias",
                    "profundo": "A ciência por trás da disciplina: como sistemas superam motivação",
                    "pratico": "3 passos simples para criar disciplina duradoura hoje mesmo"
                },
                "post_social": "A disciplina não é sobre força de vontade, mas sobre sistemas inteligentes. Este vídeo mudou minha perspectiva sobre como criar hábitos duradouros. Vale cada minuto investido. #Disciplina #Produtividade #Hábitos #Crescimento"
            }
        },
        "metadata": {
            "processado_em": datetime.now().isoformat(),
            "versao_processador": "1.0.0",
            "tempo_processamento_segundos": 142.5
        }
    }
    
    return example_result

def save_example():
    """Salva o exemplo em um arquivo JSON."""
    result = create_example_output()
    
    with open("exemplo_saida.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("✅ Exemplo de saída salvo em: exemplo_saida.json")
    return result

def display_summary(result):
    """Exibe um resumo formatado do resultado."""
    print("\n" + "="*60)
    print("🎬 EXEMPLO DE PROCESSAMENTO DE VÍDEO DO YOUTUBE")
    print("="*60)
    
    video = result["video"]
    modos = result["modos"]
    
    print(f"📹 Título: {video['titulo_detectado']}")
    print(f"⏱️  Duração: {video['duracao_minutos']} minutos")
    print(f"🌐 Idioma: {video['idioma_origem']} → {video['traduzido_para']}")
    print(f"📊 Qualidade: {video['qualidade_transcricao']}")
    print(f"👁️  Visualizações: {video['view_count']:,}")
    
    print(f"\n📝 RESULTADOS EXTRAÍDOS:")
    print(f"   • Transcrição: {len(modos['transcricao']['blocos'])} blocos")
    print(f"   • Insights: {len(modos['insights'])} insights")
    print(f"   • Clippings: {len(modos['clippings'])} frases de impacto")
    
    print(f"\n💡 INSIGHTS DESTACADOS:")
    for i, insight in enumerate(modos['insights'][:3], 1):
        print(f"   {i}. {insight['nome']} ({insight['tipo']})")
        print(f"      {insight['timestamp']} - {insight['descricao'][:80]}...")
    
    print(f"\n🎯 FRASES DE IMPACTO:")
    for i, clip in enumerate(modos['clippings'][:3], 1):
        print(f"   {i}. \"{clip['frase']}\" ({clip['emocao']})")
    
    print(f"\n📰 CONTEÚDO GERADO:")
    conteudo = modos['conteudo']
    print(f"   Blog: {conteudo['blog_titulo']}")
    print(f"   Clickbait: {conteudo['headlines']['clickbait']}")
    print(f"   Post Social: {conteudo['post_social'][:100]}...")
    
    print(f"\n🎉 Este é um exemplo do que o processador pode fazer!")
    print(f"    Execute 'python example_usage.py' para processar um vídeo real.")

def main():
    """Função principal."""
    print("🎬 Demonstração do Processador de Vídeos do YouTube")
    print("Este script mostra um exemplo de saída estruturada.")
    
    # Cria e salva exemplo
    result = save_example()
    
    # Exibe resumo
    display_summary(result)
    
    # Opção de ver JSON completo
    ver_json = input("\nDeseja ver o JSON completo? (s/N): ").strip().lower()
    if ver_json in ['s', 'sim', 'y', 'yes']:
        print("\n" + "="*60)
        print("JSON COMPLETO:")
        print("="*60)
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()