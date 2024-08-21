def main():
    import transcription
    import sys

    try:
        filename, url = sys.argv[1:]
    except:
        extensao = input('Digite a extensão do arquivo (txt, md, etc.): ')
        filename = input('Nome do arquivo para salvar o texto: ')
        url = input('URL do vídeo: ')

    transcription.download_youtube_video(url, filename)
    transcription.to_wav(filename)
    text = transcription.transcrever(filename)
    transcription.save(filename, text)
    print('Programa finalizado')

if __name__ == '__main__':
    main()