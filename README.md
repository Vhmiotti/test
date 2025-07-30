# 🎬 Processador de Vídeos do YouTube

Um processador avançado de vídeos do YouTube que extrai e estrutura conteúdo em **quatro modos distintos**, traduzindo automaticamente para português quando necessário. Ideal para criação de conteúdo, análise de vídeos e automação editorial.

## 🌟 Funcionalidades

### 🎯 Quatro Modos de Processamento

1. **📝 MODO 1 - Transcrição e Legendas**
   - Transcrição completa com timestamps
   - Formato SRT para legendas
   - JSON estruturado com blocos de fala
   - Limpeza automática de vícios de linguagem
   - Filtragem de conteúdo irrelevante (propaganda, CTAs)

2. **💡 MODO 2 - Insights Aplicáveis**
   - Extração de até 10 insights relevantes
   - Categorização automática: conceitual, ação imediata, motivacional, técnico
   - Timestamps precisos para cada insight
   - Descrições objetivas e claras

3. **🎬 MODO 3 - Clippings de Frases de Impacto**
   - 5-10 frases com alto potencial viral
   - Análise emocional: inspiração, crítica, urgência, esperança, humor
   - Contexto situacional de cada frase
   - Timestamps para criação de clips

4. **📰 MODO 4 - Conteúdo Final**
   - Resumo executivo em 3 parágrafos
   - Título otimizado para blog/SEO
   - 3 tipos de headlines: clickbait, profundo, prático
   - Post pronto para redes sociais com CTAs

### ✨ Recursos Avançados

- 🌐 **Tradução Automática**: Detecta idioma e traduz para português
- 🧹 **Limpeza Inteligente**: Remove vícios de linguagem e ruídos
- 📊 **Avaliação de Qualidade**: Analisa qualidade da transcrição
- 🎵 **Suporte Multi-formato**: Processa qualquer vídeo do YouTube
- 💾 **Export JSON**: Resultado estruturado pronto para APIs

## 🚀 Instalação Rápida

### Método 1: Instalação Automática (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/youtube-processor.git
cd youtube-processor

# Execute o instalador automático
python install_dependencies.py
```

### Método 2: Instalação Manual

```bash
# Instale FFmpeg (necessário para processamento de áudio)
# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Baixe de https://ffmpeg.org/download.html

# Instale dependências Python
pip install -r requirements.txt
```

## 📖 Como Usar

### Uso Básico

```python
from youtube_processor import YouTubeVideoProcessor

# Inicializa o processador
processor = YouTubeVideoProcessor(whisper_model="base")

# Processa um vídeo
url = "https://www.youtube.com/watch?v=exemplo"
resultado = processor.process_video(url)

# Salva o resultado
processor.save_result(resultado, "resultado.json")
```

### Exemplo Interativo

```bash
# Execute o exemplo interativo
python example_usage.py

# Ou use o processador principal
python youtube_processor.py
```

### Uso Avançado

```python
from youtube_processor import YouTubeVideoProcessor
import json

# Configuração personalizada
processor = YouTubeVideoProcessor(
    whisper_model="medium"  # tiny, base, small, medium, large
)

# Processa múltiplos vídeos
urls = [
    "https://www.youtube.com/watch?v=video1",
    "https://www.youtube.com/watch?v=video2"
]

for i, url in enumerate(urls):
    resultado = processor.process_video(url)
    processor.save_result(resultado, f"resultado_{i+1}.json")
    
    # Acessa resultados específicos
    if "erro" not in resultado:
        insights = resultado['modos']['insights']
        clippings = resultado['modos']['clippings']
        conteudo = resultado['modos']['conteudo']
        
        print(f"Vídeo {i+1}: {len(insights)} insights, {len(clippings)} clippings")
```

## 📊 Estrutura do JSON de Saída

```json
{
  "video": {
    "url": "https://youtube.com/...",
    "titulo_detectado": "Título do vídeo original",
    "idioma_origem": "en",
    "traduzido_para": "pt",
    "duracao_minutos": 14.2,
    "qualidade_transcricao": "alta",
    "motivo_qualidade": "áudio limpo, fala clara e pausas bem definidas"
  },
  "modos": {
    "transcricao": {
      "srt": "1\n00:00:01,000 --> 00:00:04,000\nTexto da transcrição...",
      "blocos": [
        {
          "start": "00:00:01,000",
          "end": "00:00:04,000",
          "speaker": "Speaker 1",
          "text": "Hoje vamos falar sobre disciplina e consistência."
        }
      ]
    },
    "insights": [
      {
        "nome": "Regra dos 5 Minutos",
        "tipo": "ação imediata",
        "timestamp": "00:03:21",
        "descricao": "Se leva menos de 5 minutos, faça agora..."
      }
    ],
    "clippings": [
      {
        "frase": "A disciplina é a forma mais pura de liberdade.",
        "timestamp": "00:04:18",
        "emocao": "inspiração",
        "contexto": "Após explicar como hábitos libertam a mente..."
      }
    ],
    "conteudo": {
      "resumo": "Neste vídeo, o autor apresenta pilares práticos...",
      "blog_titulo": "Como ser disciplinado mesmo nos piores dias",
      "headlines": {
        "clickbait": "Você nunca mais vai procrastinar depois disso",
        "profundo": "A disciplina silenciosa que constrói liberdade",
        "pratico": "3 ações simples para treinar sua mente hoje"
      },
      "post_social": "Disciplina não é sobre força de vontade..."
    }
  }
}
```

## ⚙️ Configurações

### Modelos Whisper Disponíveis

| Modelo | Tamanho | Velocidade | Qualidade | Uso Recomendado |
|--------|---------|------------|-----------|-----------------|
| `tiny` | 39 MB | Muito rápida | Básica | Testes rápidos |
| `base` | 74 MB | Rápida | Boa | **Uso geral** |
| `small` | 244 MB | Média | Muito boa | Qualidade alta |
| `medium` | 769 MB | Lenta | Excelente | Produção |
| `large` | 1550 MB | Muito lenta | Máxima | Casos especiais |

### Personalização

```python
# Personalizar filtros de conteúdo irrelevante
processor.irrelevant_phrases.extend([
    "minha frase customizada",
    "outro filtro"
])

# Personalizar vícios de linguagem
processor.filler_words.extend([
    "hmm", "ahh"
])

# Configurar palavras-chave para insights
custom_keywords = {
    'estratégico': ['planejamento', 'estratégia', 'visão'],
    'operacional': ['execução', 'implementação', 'prática']
}
```

## 🛠️ Dependências

### Principais
- **yt-dlp**: Download de vídeos do YouTube
- **OpenAI Whisper**: Transcrição de áudio com IA
- **googletrans**: Tradução automática
- **NLTK**: Processamento de linguagem natural
- **PyTorch**: Framework de deep learning

### Sistema
- **FFmpeg**: Processamento de áudio/vídeo
- **Python 3.8+**: Linguagem base

## 🔧 Solução de Problemas

### Erro: "FFmpeg not found"
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Baixe e instale de https://ffmpeg.org/
```

### Erro: "No module named 'torch'"
```bash
# Instale PyTorch
pip install torch torchvision torchaudio

# Para CPU apenas (mais leve)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Erro de Tradução
```python
# Use uma VPN ou configure proxy se houver bloqueio regional
# Ou desative a tradução modificando o código para retornar texto original
```

### Vídeo Muito Longo
```python
# Use modelo menor para vídeos longos
processor = YouTubeVideoProcessor(whisper_model="tiny")

# Ou processe apenas parte do vídeo (modifique yt-dlp options)
```

## 📈 Performance

### Tempos Estimados (vídeo de 10 minutos)

| Modelo | CPU | GPU | Qualidade |
|--------|-----|-----|-----------|
| tiny | 2 min | 30 seg | ⭐⭐ |
| base | 4 min | 1 min | ⭐⭐⭐ |
| small | 8 min | 2 min | ⭐⭐⭐⭐ |
| medium | 15 min | 4 min | ⭐⭐⭐⭐⭐ |

## 🎯 Casos de Uso

### 📝 Criação de Conteúdo
- Transformar vídeos em artigos de blog
- Gerar posts para redes sociais
- Criar newsletters com insights

### 📊 Análise de Conteúdo
- Extrair insights de palestras
- Analisar tendências de conteúdo
- Monitorar menções e temas

### 🎬 Produção de Mídia
- Criar clipes virais automaticamente
- Gerar legendas profissionais
- Produzir resumos executivos

### 🤖 Automação
- Integrar com APIs de CMS
- Alimentar sistemas de IA
- Automatizar workflows editoriais

## 🔮 Roadmap

- [ ] **Detecção de múltiplos falantes**
- [ ] **Análise de sentimento avançada**
- [ ] **Integração com APIs de redes sociais**
- [ ] **Suporte a playlists**
- [ ] **Interface web**
- [ ] **API REST**
- [ ] **Docker container**
- [ ] **Processamento em lote otimizado**

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🙏 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcrição de áudio
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Download de vídeos
- [NLTK](https://www.nltk.org/) - Processamento de linguagem natural
- [googletrans](https://github.com/ssut/py-googletrans) - Tradução automática

## 📞 Suporte

- 🐛 [Reportar Bug](https://github.com/seu-usuario/youtube-processor/issues)
- 💡 [Sugerir Feature](https://github.com/seu-usuario/youtube-processor/issues)
- 📧 Email: seu-email@exemplo.com

---

⭐ **Se este projeto foi útil, deixe uma estrela no GitHub!**

🚀 **Pronto para transformar vídeos em conteúdo estruturado? Comece agora!**