import os
import wave
import pandas as pd
from datetime import datetime
from pydub import AudioSegment
from pydub.effects import normalize

# Функция для получения длительности аудиофайла WAV
def get_audio_duration(file_name):
    with wave.open(file_name, 'r') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)
    return duration

# Функция для парсинга времени в формате час:минуты:секунды.миллисекунды
def parse_time(time_str):
    if len(time_str) > 8:
        format_str = '%H:%M:%S.%f'
    else:
        format_str = '%H:%M:%S'
    time_obj = datetime.strptime(time_str, format_str)
    return time_obj

# Функция для форматирования времени с миллисекундами
def format_timedelta_with_milliseconds(time_delta):
    seconds = time_delta.total_seconds()
    milliseconds = int((seconds - int(seconds)) * 1000)
    formatted_time = str(time_delta).split('.')[0] + f'.{milliseconds:03}'
    return formatted_time

# Функция для расчета темпа аудио
def calculate_audio_tempo(audio_duration, time_difference):
    tempo = (audio_duration / time_difference.total_seconds()) * 60
    return tempo

# Функция для корректировки скорости аудио
def adjust_audio_speed(input_audio_path, speed_factor):
    audio = AudioSegment.from_wav(input_audio_path)
    adjusted_audio = audio.speedup(playback_speed=speed_factor, chunk_size=150)
    return adjusted_audio

# Функция для нормализации аудио
def normalize_audio(input_audio_path, output_audio_path):
    audio = AudioSegment.from_wav(input_audio_path)
    normalized_audio = normalize(audio)
    normalized_audio.export(output_audio_path, format="wav")

# Создание папки для сохранения откорректированных аудиофайлов, если она не существует
adjusted_folder = 'adjusted'
os.makedirs(adjusted_folder, exist_ok=True)

# Чтение файла CSV
df = pd.read_csv('output (2).csv', delimiter=',')

# Добавление столбца для длительности аудиофайлов
df['audio_duration'] = df['index'].apply(lambda x: get_audio_duration(f'C:/проекты/csv_to_video/{x}.wav'))

# Преобразование столбцов времени в формат datetime
df['start'] = df['start'].apply(parse_time)
df['end'] = df['end'].apply(parse_time)

# Добавление столбца для разницы времени
df['time_difference'] = df['end'] - df['start']

# Вычисление процентной разницы
df['percentage_difference'] = ((df['time_difference'].dt.total_seconds() - df['audio_duration']) / df['audio_duration']) * 100

# Вычисление соотношения времени к длительности аудиофайла
df['time_to_audio_duration_ratio'] = (df['time_difference'].dt.total_seconds() / df['audio_duration']) * 100

# Расчет темпа аудио для каждого файла
df['audio_tempo'] = df.apply(lambda row: calculate_audio_tempo(row['audio_duration'], row['time_difference']), axis=1)

# Вывод всех полученных данных
print("Исходные данные из CSV:")
print(df)

# Вывод результатов вычислений и подгонка аудиофайлов
print("\nРезультаты вычислений и подгонка аудиофайлов:")
for index, row in df.iterrows():
    print(f"Для строки {index+1}:")
    print(f"Длительность аудиофайла: {row['audio_duration']} секунд")
    print(f"Разница времени: {format_timedelta_with_milliseconds(row['time_difference'])} секунд")
    print(f"Процентная разница между длительностью файла и временем: {row['percentage_difference']:.2f} %")
    print(f"Соотношение времени к длительности аудиофайла: {row['time_to_audio_duration_ratio']:.2f} %")
    print(f"Темп аудио: {row['audio_tempo']:.2f} BPM")

    # Подгонка аудио по темпу и сохранение
    speed_factor = row['audio_tempo'] / 60
    adjusted_audio = adjust_audio_speed(f'C:/проекты/csv_to_video/{row["index"]}.wav', speed_factor)
    adjusted_audio_path = f'{adjusted_folder}/{row["index"]}_adjusted.wav'
    adjusted_audio.export(adjusted_audio_path, format="wav")
    print(f"Откорректированное аудио сохранено по пути: {adjusted_audio_path}")

    # Нормализация аудио и сохранение
    normalized_audio_path = f'{adjusted_folder}/{row["index"]}_normalized.wav'
    normalize_audio(adjusted_audio_path, normalized_audio_path)
    print(f"Нормализованное аудио сохранено по пути: {normalized_audio_path}")
    print("\n")