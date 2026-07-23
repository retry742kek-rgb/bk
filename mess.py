import os
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

OUT = Path("downloads")
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()


IMAGES = [
    "мем с котом", "screenshot 2024-03-11 at 14.22.01", "IMG_{n}", "фотка с дачи",
    "DSC{n}", "аватарка новая", "скрин переписки", "photo_{n}_2023", "обои на телефон",
    "Снимок экрана {n}", "селфи", "картинка для презы",
]
DOCS = [
    "Диплом_финал_ФИНАЛ_v3", "реферат по истории", "договор аренды (подписанный)",
    "конспект лекции {n}", "Резюме_Иванов", "Домашка_{n}", "чек из магазина",
    "Отчёт за квартал", "список покупок", "Untitled document ({n})",
    "презентация проекта v{n}", "смета ремонт",
]
MEDIA = [
    "запись созвона {n}", "видео с дня рождения", "трек который искал",
    "podcast_ep{n}", "лекция {n} часть 2", "рингтон",
]
JUNK = [
    "новый документ", "aaa", "тест", "asdfgh", "123", "temp_{n}",
    "не удалять!!!", "СРОЧНО", "1", "copy of copy",
]

EXT_GROUPS = {
    "image": [".jpg", ".jpg", ".png", ".png", ".jpeg", ".webp", ".gif", ".HEIC"],
    "doc": [".pdf", ".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".DOCX"],
    "media": [".mp4", ".mp3", ".mp3", ".mov", ".wav", ".mkv"],
    "other": [".zip", ".rar", ".exe", ".py", ".json", ".html", ".apk", ".dmg", ""],
}


def make_name(pool):
    template = random.choice(pool)
    return template.format(n=random.randint(1, 9999))


def payload(seed_text, size_kb):
    """Текстовое наполнение: хорошо жмётся, но уникально для каждого файла."""
    block = (seed_text + " " + "-" * 40 + "\n")
    repeats = max(1, (size_kb * 1024) // len(block))
    return (block * repeats).encode("utf-8")


def write_file(name, ext, size_kb, days_ago, content=None):
    path = OUT / f"{name}{ext}"
    counter = 1
    while path.exists():
        path = OUT / f"{name} ({counter}){ext}"
        counter += 1
    data = content if content is not None else payload(path.name, size_kb)
    path.write_bytes(data)
    ts = (datetime.now() - timedelta(days=days_ago)).timestamp()
    os.utime(path, (ts, ts))
    return path



created = []

plan = [
    (IMAGES, "image", 120),
    (DOCS, "doc", 90),
    (MEDIA, "media", 35),
    (JUNK, "other", 40),
]

for pool, group, count in plan:
    for _ in range(count):
        name = make_name(pool)
        ext = random.choice(EXT_GROUPS[group])
        if group == "media":
            size_kb = random.randint(300, 2500)
        elif group == "image":
            size_kb = random.randint(80, 900)
        else:
            size_kb = random.randint(5, 300)
        days_ago = random.randint(1, 1460)  
        created.append(write_file(name, ext, size_kb, days_ago))



DUP_PREFIXES = ["Копия ", "", "(1) ", "final_", "Copy of "]
for source in random.sample(created, 30):
    data = source.read_bytes()
    prefix = random.choice(DUP_PREFIXES)
    new_name = prefix + source.stem + random.choice(["", " (2)", "_копия", "-1"])
    write_file(new_name, source.suffix, 0, random.randint(1, 1460), content=data)



for i in range(3):
    write_file(f"фильм скачанный но не просмотренный {i + 1}", ".mkv",
               random.randint(3000, 6000), random.randint(200, 1400))

total = sum(f.stat().st_size for f in OUT.iterdir())
print(f"Готово: {len(list(OUT.iterdir()))} файлов, {total / 1024 / 1024:.1f} МБ в папке {OUT.resolve()}")