import pandas as pd
from moviepy.editor import VideoFileClip, AudioFileClip

# Функция для вставки аудио в видео
def insert_audio(video_file, audio_file, start_time, end_time, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    # Обрезаем аудио по временным границам
    audio = audio.subclip(start_time, end_time)

    # Вставляем аудио в видео
    video = video.set_audio(audio)

    # Сохраняем видео с вставленным аудио
    video.write_videofile(output_file, codec='libx264', audio_codec='aac')

# видеофайл
video_file_name = 'goblin.mp4'

# CSV-файл
csv_file = 'tex.csv'  # Путь к вашему CSV-файлу
df = pd.read_csv(csv_file)

# Перебор строк CSV
for index, row in df.iterrows():
    video_file = video_file_name  # Имя видеофайла с расширением
    audio_file = row['line'] + '.wav'  # Имя аудиофайла с расширением
    start_time = row['start']  # Время начала вставки аудио в видео
    end_time = row['end']  # Время конца вставки аудио в видео
    output_file = f"output_{index}.mp4"  # Выходное имя файла

    # Вставка аудио в видео
    insert_audio(video_file, audio_file, start_time, end_time, output_file)
