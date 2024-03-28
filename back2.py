import pandas as pd
from moviepy.editor import VideoFileClip, concatenate_videoclips


# Функция для преобразования времени из формата чч:мм:сс.мс в секунды
def to_seconds(time_str):
    hours, minutes, seconds = map(float, time_str.split(':'))
    return 3600 * hours + 60 * minutes + seconds


# Чтение данных из CSV-файла
csv_file_path = "output (2).csv"  # Путь к вашему CSV-файлу
df = pd.read_csv(csv_file_path)

# Загрузка видеофайла
video_path = "test.mp4"  # Путь к вашему видеофайлу
video_clip = VideoFileClip(video_path)

# Создание списка подклипов для объединения
subclips = []

# Проход по каждой строке CSV-файла
for index, row in df.iterrows():
    start_time = to_seconds(row['start'])  # Преобразование начального времени в секунды
    end_time = to_seconds(row['end'])  # Преобразование конечного времени в секунды

    # Создание подклипа с указанными временными метками
    subclip = video_clip.subclip(start_time, end_time)

    # Уменьшение громкости на 1% для каждого подклипа
    subclip = subclip.volumex(0.01)

    # Добавление подклипа в список с учетом временных меток
    subclips.append(subclip.set_start(start_time).set_end(end_time))

# Объединение подклипов в один видеофайл
final_clip = concatenate_videoclips(subclips)

# Сохранение финального видеофайла
final_output_path = "output_video.mp4"  # Путь к финальному видеофайлу
final_clip.write_videofile(final_output_path, codec='libx264', audio_codec='aac')

# Освобождение ресурсов
video_clip.close()
