import os
import pandas as pd
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence
from moviepy.editor import VideoFileClip, AudioFileClip


def time_to_seconds(time_str):
    """Преобразует строку времени в секунды"""
    time_format = "%H:%M:%S.%f" if '.' in time_str else "%H:%M:%S"
    dt = datetime.strptime(time_str, time_format)
    return dt.hour * 3600 + dt.minute * 60 + dt.second + dt.microsecond / 1000000


def concatenate_audio(audio_folder, csv_file, output_audio_path):
    # Загрузка данных из CSV файла
    data = pd.read_csv(csv_file)

    # Создание списка для хранения всех аудиофайлов
    audio_segments = []

    # Загрузка и объединение аудиофайлов
    for index, row in data.iterrows():
        audio_file_path = os.path.join(audio_folder, f"{row['index']}_adjusted.wav")
        audio = AudioSegment.from_wav(audio_file_path)
        audio_segments.append(audio)

    # Создание списка для хранения всех сегментов аудиофайлов и пауз
    segments_with_silence = []

    # Добавление аудиофайлов и тишины в соответствии с временными метками
    for i in range(len(audio_segments)):
        # Добавляем аудиофайл
        segments_with_silence.append(audio_segments[i])
        # Если это не последний аудиофайл
        if i < len(audio_segments) - 1:
            # Рассчитываем длительность тишины между текущим и следующим аудиофайлом
            silence_duration = (time_to_seconds(data.loc[i + 1, 'start']) - time_to_seconds(
                data.loc[i, 'end'])) * 1000  # в миллисекундах
            # Создаем сегмент тишины
            silence = AudioSegment.silent(duration=silence_duration)
            # Добавляем тишину
            segments_with_silence.append(silence)

    # Объединяем все сегменты аудиофайлов и тишины
    combined_audio = sum(segments_with_silence)

    # Сохраняем объединенный аудиофайл
    combined_audio.export(output_audio_path, format="wav")


def overlay_audio_on_video(video_path, audio_path, output_video_path):
    # Загрузка видео
    video = VideoFileClip(video_path)

    # Загрузка аудио
    audio = AudioFileClip(audio_path)

    # Наложение аудио на видео
    video = video.set_audio(audio)

    # Сохранение результата
    video.write_videofile(output_video_path, codec="libx264")


def main():
    # Папка с аудиофайлами
    audio_folder = "C:/проекты/csv_to_video/adjusted"

    # Путь к CSV файлу
    csv_file = "output (2).csv"

    # Путь для сохранения объединенного аудиофайла
    output_audio_path = "combined_audio.wav"

    # Объединение аудиофайлов
    concatenate_audio(audio_folder, csv_file, output_audio_path)

    # Оригинальное видео
    video_path = "goblin.mp4"

    # Получившееся аудио
    audio_path = "combined_audio.wav"

    # Выходное видео с наложенным аудио
    output_video_path = "video_with_audio.mp4"

    # Наложение аудио на видео
    overlay_audio_on_video(video_path, audio_path, output_video_path)


if __name__ == "__main__":
    main()