import datetime


def rename_file(user_id: str, original_filename: str) -> str:
    """
    Формирует уникальное имя файла с учётом user_id и текущего времени.

    Пример: user_abc123_20240604_151530.mp3
    """

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    extension = original_filename.split('.')[-1] if '.' in original_filename else 'bin'

    new_filename = f'user_{user_id[0:9]}_{timestamp}.{extension}'

    return new_filename
