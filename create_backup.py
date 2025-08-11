import os
import shutil
import logging
import logging.handlers as handlers

from json_util import load_json, save_json
""" """



WORKDIRS = [
    './log',
    './config',
]

def create_dirs(workdirs):
    """Создает каталоги по списку путей workdirs"""
    for path in workdirs:
        os.makedirs(path, exist_ok=True)


def create_loggger(logfilename: str):
    """ Создает логгер типа RotatingFileHandler c параметрами
    logfilename,
    file_count = 5,
    maxBytes = 5 * 1024 * 1024,
    fmt = "%(asctime)s [%(module)s %(levelname)s] => %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S',
    """

    file_count = 5
    maxBytes = 5 * 1024 * 1024

    logger = logging.getLogger('main_logger')

    handler = handlers.RotatingFileHandler(logfilename,
                                           maxBytes=maxBytes,
                                           backupCount=file_count,
                                           encoding='utf-8')

    fmt = "%(asctime)s [%(module)s %(levelname)s] => %(message)s"
    datefmt = '%Y-%m-%d %H:%M:%S'

    formatter = logging.Formatter(fmt, datefmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def copy_folder(src, dst):
    for root, dirs, files in os.walk(src):
        target_dir = root.replace(src, dst)
        os.makedirs(target_dir, exist_ok=True)
        for file in files:
            src_path = os.path.join(root, file)
            dst_path = os.path.join(target_dir, file)
            logger.info(f"копируем {src_path} в {dst_path}")

            try:
                shutil.copy(src_path, dst_path)
            except Exception as e:
                logger.exception(f"Произошла ошибка при копировании файла '{src_path}")


if __name__ == '__main__':
    """ Скрипт для копирования директории с логированием ошибок"""
    create_dirs(WORKDIRS)

    logger = create_loggger('./log/applog.log')
    logger.setLevel(logging.INFO)

    if os.path.exists('./config/appsettings.json'):
        try:
            SETTINGS = load_json('./config/appsettings.json')
            src_f = SETTINGS['src_f']
            dst_f = SETTINGS['dst_f']
        except Exception as e:
            logger.exception('При открытии файла appsettings.json произошла ошибка')
        if src_f and dst_f:
            try:
                logger.info(f'Копирование {src_f} в {dst_f} начато')
                copy_folder(src_f, dst_f)
                logger.info(f'Копирование {src_f} в {dst_f} завершено')
            except Exception as e:
                logger.exception('При открытии файла appsettings.json произошла ошибка')
        else:
            logger.info(f'{src_f} или {dst_f} не определены в файле конфигурации')
    else:
        save_json('./config/appsettings.json', {'src_f': '', 'dst_f': ''})
        logger.info(f'appsettings.json не найден, создан новый файл конфигурации')
