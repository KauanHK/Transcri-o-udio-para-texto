from pydub import AudioSegment
import moviepy.editor as mp
import speech_recognition as sr
import pytubefix
import os
import sys



def download_youtube_video(url, filename: str | None = 'video'):
    
    print('Buscando vídeo...', end='')
    video = pytubefix.YouTube(url)
    print(' OK')

    stream = video.streams.filter(only_audio=True).first()

    print('Fazendo download do áudio...', end='')
    stream.download(filename=f'{filename}.mp4')
    print(' OK')

def to_wav(filename: str):

    print('Extraindo áudio...', end='')
    audio = AudioSegment.from_file(f'{filename}.mp4', format='mp4')
    print(' OK')

    print('Formatando áudio para formato wav...', end='')
    audio.export(f'{filename}.mp3', format='mp3')
    audio = AudioSegment.from_mp3(f'{filename}.mp3')
    print(' OK')

    print('Salvando e removendo arquivos...', end='')
    audio.export(f'{filename}.wav', format='wav')
    os.remove(f'{filename}.mp3')
    os.remove(f'{filename}.mp4')
    print(' OK')


def split_audio(filename: str, chunk_length_ms=20000):
    audio = AudioSegment.from_wav(f'{filename}.wav')
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

def transcrever(filename: str, extensao: str = '.txt', rm_wav_file: bool = True):
    recognizer = sr.Recognizer()

    print('Dividindo áudio...', end='')
    chunk_length_ms = 20000
    chunks = split_audio(filename, chunk_length_ms)
    print(' OK')

    print(f'Salvando texto em {filename}.{extensao}')
    chunk_filename = '4ib53453b.wav'
    num_chunks = len(chunks)
    for i, chunk in enumerate(chunks):
        chunk.export(chunk_filename, format='wav')

        with sr.AudioFile(chunk_filename) as source:
            print(f'Transcrevendo {int(chunk_length_ms*(i+1)/1000)}/{int(num_chunks*chunk_length_ms/1000)} seg', end='    \r')
            
            try:
                audio_text = recognizer.record(source)
            except Exception as e:
                print(f'\nErro: Parte do áudio não pode ser transcrita devido ao seguinte erro: {e}')
            
            try:
                texto = recognizer.recognize_google(audio_text, language='pt-BR')
            except Exception as e:
                print(f'Erro: {e}')
            else:
                save(filename, extensao, texto)


        os.remove(chunk_filename)
    if rm_wav_file:
        os.remove(f'{filename}.wav')
    print('\n Transcrição bem-sucedida')

    print(f'Salvando arquivo em {filename}.{extensao}....', end='')
    
    print(' OK')

    return texto

def save(filename: str, extensao: str, texto: str):
    arq = f'{filename}.{extensao}'
    mode = 'w' if not os.path.exists(arq) else 'a'
    with open(arq, mode) as arquivo:
        arquivo.write(' ' + texto)