import json
import os
import re
import tempfile
import time
from datetime import timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs

import yt_dlp
import whisper
from googletrans import Translator
from langdetect import detect
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import torch

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class YouTubeVideoProcessor:
    """
    Processador de vídeos do YouTube que extrai e estrutura conteúdo em quatro modos:
    1. Transcrição e legendas
    2. Insights aplicáveis
    3. Clippings de frases de impacto
    4. Conteúdo final (blog, post, headlines)
    """
    
    def __init__(self, whisper_model: str = "base"):
        """
        Inicializa o processador com modelo Whisper especificado.
        
        Args:
            whisper_model: Modelo Whisper a usar ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.translator = Translator()
        self.whisper_model = whisper.load_model(whisper_model)
        self.temp_dir = tempfile.mkdtemp()
        
        # Palavras e frases irrelevantes para filtrar
        self.irrelevant_phrases = [
            "se inscreve no canal", "curte o vídeo", "deixa o like", 
            "compartilha", "ativa o sininho", "vinheta", "abertura",
            "encerramento", "patrocinador", "anúncio", "propaganda"
        ]
        
        # Vícios de linguagem para remover
        self.filler_words = [
            "ééé", "ahh", "hmm", "tipo", "né", "tá", "então", "assim",
            "sabe", "entende", "ok", "certo", "beleza"
        ]

    def extract_video_info(self, url: str) -> Dict:
        """Extrai informações básicas do vídeo."""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        return {
            'url': url,
            'titulo_detectado': info.get('title', ''),
            'duracao_minutos': round(info.get('duration', 0) / 60, 1),
            'uploader': info.get('uploader', ''),
            'upload_date': info.get('upload_date', ''),
            'view_count': info.get('view_count', 0)
        }

    def download_audio(self, url: str) -> str:
        """Baixa o áudio do vídeo e retorna o caminho do arquivo."""
        audio_path = os.path.join(self.temp_dir, 'audio.wav')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path.replace('.wav', '.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return audio_path

    def transcribe_audio(self, audio_path: str) -> Dict:
        """Transcreve o áudio usando Whisper."""
        result = self.whisper_model.transcribe(audio_path, language='auto')
        
        # Detecta idioma original
        sample_text = result['text'][:200]
        try:
            original_language = detect(sample_text)
        except:
            original_language = result.get('language', 'unknown')
            
        return {
            'segments': result['segments'],
            'text': result['text'],
            'language': original_language
        }

    def clean_text(self, text: str) -> str:
        """Limpa o texto removendo vícios de linguagem e ruídos."""
        # Remove vícios de linguagem
        for filler in self.filler_words:
            text = re.sub(rf'\b{re.escape(filler)}\b', '', text, flags=re.IGNORECASE)
        
        # Remove repetições excessivas
        text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)
        
        # Limpa espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Adiciona pontuação básica se necessário
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
            
        return text

    def is_relevant_segment(self, text: str) -> bool:
        """Verifica se um segmento é relevante (não é spam/propaganda)."""
        text_lower = text.lower()
        return not any(phrase in text_lower for phrase in self.irrelevant_phrases)

    def translate_to_portuguese(self, text: str, source_lang: str) -> str:
        """Traduz texto para português se necessário."""
        if source_lang == 'pt':
            return text
            
        try:
            translated = self.translator.translate(text, src=source_lang, dest='pt')
            return translated.text
        except:
            return text  # Retorna original se tradução falhar

    def seconds_to_srt_time(self, seconds: float) -> str:
        """Converte segundos para formato SRT (HH:MM:SS,mmm)."""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

    def mode1_transcription(self, segments: List, original_language: str) -> Dict:
        """Modo 1: Transcrição e legendas."""
        srt_content = ""
        json_blocks = []
        
        for i, segment in enumerate(segments):
            text = self.clean_text(segment['text'])
            
            if not self.is_relevant_segment(text):
                continue
                
            # Traduz se necessário
            if original_language != 'pt':
                text = self.translate_to_portuguese(text, original_language)
            
            start_time = self.seconds_to_srt_time(segment['start'])
            end_time = self.seconds_to_srt_time(segment['end'])
            
            # Formato SRT
            srt_content += f"{len(json_blocks) + 1}\n"
            srt_content += f"{start_time} --> {end_time}\n"
            srt_content += f"{text}\n\n"
            
            # JSON block
            json_blocks.append({
                "start": start_time,
                "end": end_time,
                "speaker": "Speaker 1",  # Pode ser expandido para detectar múltiplos falantes
                "text": text
            })
        
        return {
            "srt": srt_content.strip(),
            "blocos": json_blocks
        }

    def mode2_insights(self, segments: List, original_language: str) -> List[Dict]:
        """Modo 2: Insights aplicáveis."""
        insights = []
        
        # Palavras-chave para diferentes tipos de insights
        keywords = {
            'conceitual': ['conceito', 'ideia', 'teoria', 'princípio', 'fundamento'],
            'ação imediata': ['faça', 'execute', 'implemente', 'comece', 'inicie', 'agora'],
            'motivacional': ['motivação', 'inspiração', 'força', 'determinação', 'persistência'],
            'técnico': ['método', 'técnica', 'ferramenta', 'processo', 'sistema']
        }
        
        for segment in segments:
            text = self.clean_text(segment['text'])
            
            if not self.is_relevant_segment(text) or len(text.split()) < 10:
                continue
                
            # Traduz se necessário
            if original_language != 'pt':
                text = self.translate_to_portuguese(text, original_language)
            
            # Determina tipo do insight baseado em palavras-chave
            insight_type = 'conceitual'  # default
            text_lower = text.lower()
            
            for tipo, palavras in keywords.items():
                if any(palavra in text_lower for palavra in palavras):
                    insight_type = tipo
                    break
            
            # Extrai insights de segmentos mais longos e informativos
            if len(text.split()) >= 15:
                insights.append({
                    "nome": self.extract_insight_name(text),
                    "tipo": insight_type,
                    "timestamp": self.seconds_to_srt_time(segment['start']),
                    "descricao": text[:200] + "..." if len(text) > 200 else text
                })
        
        # Limita a 10 insights mais relevantes
        return insights[:10]

    def extract_insight_name(self, text: str) -> str:
        """Extrai um nome curto para o insight."""
        sentences = sent_tokenize(text)
        if sentences:
            # Pega a primeira frase e simplifica
            first_sentence = sentences[0]
            words = word_tokenize(first_sentence)
            # Pega as primeiras 3-5 palavras principais
            important_words = [w for w in words[:8] if len(w) > 3 and w.isalpha()]
            return ' '.join(important_words[:4]).title()
        return "Insight Importante"

    def mode3_clippings(self, segments: List, original_language: str) -> List[Dict]:
        """Modo 3: Clippings de frases de impacto."""
        clippings = []
        
        # Padrões para identificar frases impactantes
        impact_patterns = [
            r'"[^"]*"',  # Frases entre aspas
            r'[A-Z][^.!?]*[.!?]',  # Frases que começam com maiúscula
        ]
        
        emotional_keywords = {
            'inspiração': ['sonho', 'possível', 'acredite', 'conquiste', 'sucesso', 'vitória'],
            'crítica': ['problema', 'erro', 'falha', 'cuidado', 'atenção', 'perigo'],
            'urgência': ['agora', 'hoje', 'imediatamente', 'urgente', 'rápido'],
            'esperança': ['futuro', 'esperança', 'melhor', 'crescimento', 'evolução'],
            'humor': ['engraçado', 'hilário', 'piada', 'riso', 'divertido']
        }
        
        for segment in segments:
            text = self.clean_text(segment['text'])
            
            if not self.is_relevant_segment(text):
                continue
                
            # Traduz se necessário
            if original_language != 'pt':
                text = self.translate_to_portuguese(text, original_language)
            
            # Procura por frases impactantes
            sentences = sent_tokenize(text)
            for sentence in sentences:
                if len(sentence.split()) >= 5 and len(sentence.split()) <= 20:
                    # Determina emoção baseada em palavras-chave
                    emotion = 'inspiração'  # default
                    sentence_lower = sentence.lower()
                    
                    for emocao, palavras in emotional_keywords.items():
                        if any(palavra in sentence_lower for palavra in palavras):
                            emotion = emocao
                            break
                    
                    clippings.append({
                        "frase": sentence.strip(),
                        "timestamp": self.seconds_to_srt_time(segment['start']),
                        "emocao": emotion,
                        "contexto": f"Contexto do momento no vídeo: {text[:100]}..."
                    })
        
        # Ordena por potencial de impacto e limita a 5-10
        clippings = sorted(clippings, key=lambda x: len(x['frase'].split()), reverse=True)
        return clippings[:8]

    def mode4_content(self, full_text: str, video_info: Dict, original_language: str) -> Dict:
        """Modo 4: Conteúdo final (blog, post, headlines)."""
        
        # Traduz texto completo se necessário
        if original_language != 'pt':
            full_text = self.translate_to_portuguese(full_text, original_language)
        
        # Gera resumo
        sentences = sent_tokenize(full_text)
        # Pega as frases mais importantes (início, meio, fim)
        key_sentences = []
        if len(sentences) > 0:
            key_sentences.append(sentences[0])  # Primeira frase
        if len(sentences) > 2:
            key_sentences.append(sentences[len(sentences)//2])  # Frase do meio
        if len(sentences) > 1:
            key_sentences.append(sentences[-1])  # Última frase
            
        resumo = ' '.join(key_sentences)
        
        # Gera título do blog baseado no título original
        titulo_original = video_info.get('titulo_detectado', '')
        if original_language != 'pt':
            titulo_original = self.translate_to_portuguese(titulo_original, original_language)
        
        blog_titulo = self.generate_blog_title(titulo_original, full_text)
        
        # Gera headlines
        headlines = self.generate_headlines(titulo_original, full_text)
        
        # Gera post social
        post_social = self.generate_social_post(resumo, titulo_original)
        
        return {
            "resumo": resumo,
            "blog_titulo": blog_titulo,
            "headlines": headlines,
            "post_social": post_social
        }

    def generate_blog_title(self, original_title: str, content: str) -> str:
        """Gera título otimizado para blog."""
        # Extrai palavras-chave principais
        words = word_tokenize(content.lower())
        # Remove stopwords
        try:
            stop_words = set(stopwords.words('portuguese'))
        except:
            stop_words = set(['o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'suas', 'numa', 'nem', 'suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos', 'pelas', 'só', 'nós', 'você', 'vocês', 'eles', 'elas'])
        
        important_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Se o título original é bom, usa uma versão melhorada
        if len(original_title.split()) > 3:
            return f"Como {original_title.lower()}: guia prático e completo"
        else:
            # Cria título baseado nas palavras-chave
            if important_words:
                main_topic = important_words[0].title()
                return f"O guia definitivo sobre {main_topic}"
            else:
                return "Estratégias práticas para o sucesso"

    def generate_headlines(self, original_title: str, content: str) -> Dict[str, str]:
        """Gera três tipos de headlines."""
        base_topic = original_title.split(':')[0] if ':' in original_title else original_title
        
        return {
            "clickbait": f"Você nunca mais vai {base_topic.lower()} da mesma forma depois disso",
            "profundo": f"A verdade sobre {base_topic.lower()} que ninguém te conta",
            "pratico": f"3 passos simples para {base_topic.lower()} com eficiência"
        }

    def generate_social_post(self, resumo: str, titulo: str) -> str:
        """Gera post para redes sociais."""
        # Pega a primeira frase do resumo
        first_sentence = sent_tokenize(resumo)[0] if resumo else titulo
        
        return f"{first_sentence} Este conteúdo mudou minha perspectiva sobre o tema. Vale cada minuto investido. #Aprendizado #Crescimento #Conteúdo"

    def assess_transcription_quality(self, segments: List) -> Tuple[str, str]:
        """Avalia a qualidade da transcrição."""
        if not segments:
            return "baixa", "Nenhum segmento transcrito"
        
        # Calcula métricas básicas
        total_segments = len(segments)
        avg_confidence = sum(seg.get('confidence', 0.5) for seg in segments) / total_segments
        avg_duration = sum(seg['end'] - seg['start'] for seg in segments) / total_segments
        
        if avg_confidence > 0.8 and avg_duration > 2:
            return "alta", "áudio limpo, fala clara e pausas bem definidas"
        elif avg_confidence > 0.6:
            return "média", "áudio razoável com algumas interferências"
        else:
            return "baixa", "áudio com ruído ou fala pouco clara"

    def process_video(self, url: str) -> Dict:
        """
        Processa um vídeo do YouTube e retorna o JSON estruturado com todos os modos.
        
        Args:
            url: URL do vídeo do YouTube
            
        Returns:
            Dict: JSON estruturado com todos os modos processados
        """
        try:
            # Extrai informações do vídeo
            video_info = self.extract_video_info(url)
            
            # Baixa e transcreve o áudio
            audio_path = self.download_audio(url)
            transcription_result = self.transcribe_audio(audio_path)
            
            segments = transcription_result['segments']
            full_text = transcription_result['text']
            original_language = transcription_result['language']
            
            # Avalia qualidade da transcrição
            quality, quality_reason = self.assess_transcription_quality(segments)
            
            # Processa cada modo
            mode1_result = self.mode1_transcription(segments, original_language)
            mode2_result = self.mode2_insights(segments, original_language)
            mode3_result = self.mode3_clippings(segments, original_language)
            mode4_result = self.mode4_content(full_text, video_info, original_language)
            
            # Monta resultado final
            result = {
                "video": {
                    **video_info,
                    "idioma_origem": original_language,
                    "traduzido_para": "pt" if original_language != "pt" else "pt",
                    "qualidade_transcricao": quality,
                    "motivo_qualidade": quality_reason
                },
                "modos": {
                    "transcricao": mode1_result,
                    "insights": mode2_result,
                    "clippings": mode3_result,
                    "conteudo": mode4_result
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "erro": f"Erro ao processar vídeo: {str(e)}",
                "video": {"url": url}
            }
        
        finally:
            # Limpa arquivos temporários
            try:
                if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
                    import shutil
                    shutil.rmtree(self.temp_dir)
            except:
                pass

    def save_result(self, result: Dict, output_file: str = "resultado.json"):
        """Salva o resultado em um arquivo JSON."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Resultado salvo em: {output_file}")


def main():
    """Exemplo de uso do processador."""
    # URL de exemplo (substitua pela URL desejada)
    url = input("Digite a URL do vídeo do YouTube: ").strip()
    
    if not url:
        print("URL não fornecida. Usando exemplo...")
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll como exemplo
    
    # Inicializa o processador
    processor = YouTubeVideoProcessor(whisper_model="base")
    
    print("Processando vídeo... Isso pode levar alguns minutos.")
    
    # Processa o vídeo
    result = processor.process_video(url)
    
    # Salva o resultado
    processor.save_result(result)
    
    # Exibe resumo
    if "erro" not in result:
        print(f"\n✅ Processamento concluído!")
        print(f"📹 Vídeo: {result['video']['titulo_detectado']}")
        print(f"⏱️ Duração: {result['video']['duracao_minutos']} minutos")
        print(f"🌐 Idioma: {result['video']['idioma_origem']} → {result['video']['traduzido_para']}")
        print(f"📊 Qualidade: {result['video']['qualidade_transcricao']}")
        print(f"📝 Transcrição: {len(result['modos']['transcricao']['blocos'])} blocos")
        print(f"💡 Insights: {len(result['modos']['insights'])} extraídos")
        print(f"🎯 Clippings: {len(result['modos']['clippings'])} frases de impacto")
        print(f"📰 Conteúdo: Blog, headlines e post social gerados")
    else:
        print(f"❌ Erro: {result['erro']}")


if __name__ == "__main__":
    main()