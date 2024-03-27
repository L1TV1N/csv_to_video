from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os
import pandas as pd


def overlay_audio_on_video(video_path, audio_path, start_time, end_time, output_video_path):
    # Загрузка видео и аудио файлов
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Повторение аудиофайла, если его длительность больше, чем видео
    if audio.duration > video.duration:
        audio = AudioFileClip(audio_path).loop(duration=video.duration)

    # Наложение аудио на видео
    video = video.set_audio(audio)

    # Сохранение результата
    video.write_videofile(output_video_path, codec="libx264")


def main():
    # Путь к оригинальному видео
    video_path = "goblin.mp4"

    # Папка с аудио файлами
    audio_folder = "C:/проекты/csv_to_video/adjusted"

    # Путь к CSV файлу
    csv_file = "output (2).csv"

    # Загрузка данных из CSV файла
    data = pd.read_csv(csv_file)

    # Создание списка для хранения видео с наложенным аудио
    videos_with_audio = []

    # Наложение аудио на видео для каждой строки в CSV файле
    for index, row in data.iterrows():
        audio_file_path = os.path.join(audio_folder, f"{row['index']}_adjusted.wav")
        start_time = pd.Timedelta(row['start']).total_seconds()
        end_time = pd.Timedelta(row['end']).total_seconds()
        output_video_path = f"video_{index}_with_audio.mp4"
        overlay_audio_on_video(video_path, audio_file_path, start_time, end_time, output_video_path)
        videos_with_audio.append(output_video_path)

    # Конкатенация всех видео с наложенным аудио
    final_video = concatenate_videoclips([VideoFileClip(video) for video in videos_with_audio])

    # Сохранение итогового видео
    final_video.write_videofile("final_video.mp4", codec="libx264")


if __name__ == "__main__":
    main()
