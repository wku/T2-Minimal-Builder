import os
import subprocess
import logging
from datetime import datetime
import argparse

# Настройка логирования
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, f"build_t2_iso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def log_and_run_command(command, error_message):
    """Выполняет команду и логирует результат."""
    logger.info(f"Выполняем команду: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Команда выполнена успешно: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{error_message}: {e.stderr}")
        return False

def check_file_exists(file_path, description):
    """Проверяет существование файла и логирует результат."""
    exists = os.path.exists(file_path)
    logger.info(f"Проверка {description}: {'существует' if exists else 'не существует'} ({file_path})")
    return exists

def ensure_directory(path, description):
    """Обеспечивает существование каталога, создавая его, если нужно."""
    if check_file_exists(path, f"каталога {description}"):
        logger.warning(f"Каталог {path} уже существует, пропускаем создание.")
    else:
        try:
            os.makedirs(path)
            logger.info(f"Каталог {path} успешно создан.")
        except OSError as e:
            logger.error(f"Ошибка при создании каталога {path}: {e}")
            return False
    return True

def remove_directory(path, description):
    """Удаляет каталог, если он существует."""
    if check_file_exists(path, f"каталога {description}"):
        try:
            subprocess.run(["rm", "-rf", path], check=True)
            logger.info(f"Каталог {path} успешно удален.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка при удалении каталога {path}: {e}")
            return False
    else:
        logger.info(f"Каталог {path} не существует, удаление не требуется.")
    return True

def change_directory(path):
    """Меняет рабочую директорию и логирует это."""
    try:
        os.chdir(path)
        logger.info(f"Рабочая директория изменена на: {os.getcwd()}")
        return True
    except OSError as e:
        logger.error(f"Ошибка при смене директории на {path}: {e}")
        return False

def check_dependencies():
    """Проверяет наличие необходимых зависимостей."""
    ncurses_path = "/usr/include/ncurses.h"
    if not check_file_exists(ncurses_path, "заголовочного файла ncurses.h"):
        logger.error("Библиотека ncurses не установлена. Установите ее с помощью:")
        logger.error("sudo apt install libncurses5-dev libncursesw5-dev (для Ubuntu/Debian)")
        return False
    return True

def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Build a minimal Linux system with T2 SDE.")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() // 2,
                        help="Number of parallel jobs for building (default: half of CPU cores)")
    args = parser.parse_args()

    # Используем значение из аргумента или переменной окружения JOBS
    jobs = os.getenv("JOBS", args.jobs)
    if not isinstance(jobs, int):
        jobs = int(jobs)

    print(f"Starting minimal Linux system build with T2 SDE using {jobs} jobs...")
    logger.info(f"Starting minimal Linux system build with T2 SDE using {jobs} jobs.")

    # Проверка зависимостей
    if not check_dependencies():
        return

    # 1. Скачивание архива T2 SDE
    t2_url = "https://dl.t2sde.org/source/t2-24.6.tar.bz2"
    t2_archive = "t2-24.6.tar.bz2"
    if not check_file_exists(t2_archive, "архива T2 SDE"):
        if not log_and_run_command(["wget", t2_url], "Ошибка при скачивании архива T2 SDE"):
            return
    else:
        logger.info("Архив T2 SDE уже существует, пропускаем скачивание.")

    # 2. Распаковка архива
    t2_dir = "t2-24.6"
    if not check_file_exists(t2_dir, "распакованной директории T2 SDE"):
        if not log_and_run_command(["tar", "-xjf", t2_archive], "Ошибка при распаковке архива T2 SDE"):
            return
    else:
        logger.info("Директория T2 SDE уже распакована, пропускаем распаковку.")

    # 3. Подготовка конфигурационного каталога
    config_dir = "config/minimal"
    if not remove_directory(config_dir, "config/minimal"):
        return
    if not ensure_directory(config_dir, "config/minimal"):
        return

    # 4. Смена рабочей директории на t2-24.6
    if not change_directory(t2_dir):
        return

    # 5. Запуск Config
    config_script = "scripts/Config"
    if not check_file_exists(config_script, "скрипта Config"):
        logger.error("Скрипт Config не найден в директории t2-24.6/scripts.")
        logger.info("Проверьте содержимое архива или повторите распаковку.")
        return
    if not log_and_run_command([f"./{config_script}", "-cfg", "minimal"], "Ошибка при запуске Config"):
        return

    # 6. Сборка образа с ограничением числа задач
    build_script = "scripts/Build-Target"
    if not check_file_exists(build_script, "скрипта Build-Target"):
        logger.error("Скрипт Build-Target не найден в директории t2-24.6/scripts.")
        return
    build_command = [f"./{build_script}", "-cfg", "minimal", "-jobs", str(jobs)]
    if not log_and_run_command(build_command, "Ошибка при сборке образа"):
        return

    logger.info("Build completed successfully!")
    print("Build completed successfully! Logs saved to", log_file)

if __name__ == "__main__":
    main()