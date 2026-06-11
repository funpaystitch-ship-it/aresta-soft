#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import datetime
import getpass

# ─── файл склада ───────────────────────────────────────────────────────────────
WAREHOUSE_FILE = "warehouse.json"
WAREHOUSE_PASS = "1425"

def load_warehouse():
    if os.path.exists(WAREHOUSE_FILE):
        with open(WAREHOUSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_warehouse(data):
    with open(WAREHOUSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── утилиты ───────────────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def now():
    return datetime.datetime.now().strftime("%H:%M:%S  %d.%m.%Y")

def divider():
    print("═" * 52)

def header():
    clear()
    divider()
    print("        ▓  A R E S T A   S O F T  ▓")
    print("       WAREHOUSE MANAGEMENT SYSTEM v1.0")
    divider()
    print(f"  TIME: {now()}")
    divider()

def pause():
    input("\n  [ENTER] — назад в меню...")

# ─── 1. ЗАГРУЗИТЬ ДАННЫЕ ───────────────────────────────────────────────────────
def menu_upload():
    while True:
        header()
        print("  > ЗАГРУЗИТЬ ДАННЫЕ АККАУНТА НА СКЛАД\n")
        print("  1. Загрузить письменные данные")
        print("  2. Загрузить файл")
        print("  0. Назад")
        divider()
        choice = input("  > Выберите: ").strip()

        if choice == "1":
            upload_text()
        elif choice == "2":
            upload_file()
        elif choice == "0":
            break
        else:
            print("  [!] Неверный выбор.")

def upload_text():
    header()
    print("  > ЗАГРУЗИТЬ ПИСЬМЕННЫЕ ДАННЫЕ\n")
    print("  Введите данные аккаунта (логин, пароль, токен и т.д.)")
    print("  Для завершения ввода введите пустую строку.\n")
    lines = []
    while True:
        line = input("  >> ")
        if line == "":
            break
        lines.append(line)
    if not lines:
        print("\n  [!] Данные не введены.")
        pause()
        return
    data = "\n".join(lines)
    wh = load_warehouse()
    entry = {
        "type": "ТЕКСТ",
        "name": f"Запись #{len(wh)+1}",
        "data": data,
        "time": now()
    }
    wh.append(entry)
    save_warehouse(wh)
    print(f"\n  [OK] Данные загружены на склад! ID: #{len(wh)}")
    pause()

def upload_file():
    header()
    print("  > ЗАГРУЗИТЬ ФАЙЛ\n")
    path = input("  Введите полный путь к файлу:\n  >> ").strip().strip('"')
    if not os.path.exists(path):
        print("\n  [!] Файл не найден.")
        pause()
        return
    size = round(os.path.getsize(path) / 1024, 1)
    name = os.path.basename(path)
    wh = load_warehouse()
    entry = {
        "type": "ФАЙЛ",
        "name": name,
        "data": f"Путь: {path} | Размер: {size} KB",
        "time": now()
    }
    wh.append(entry)
    save_warehouse(wh)
    print(f"\n  [OK] Файл '{name}' ({size} KB) загружен на склад! ID: #{len(wh)}")
    pause()

# ─── 2. ОТКРЫТЬ СКЛАД ──────────────────────────────────────────────────────────
def menu_warehouse():
    header()
    print("  > ОТКРЫТЬ СКЛАД — ТРЕБУЕТСЯ АВТОРИЗАЦИЯ\n")
    pwd = getpass.getpass("  Введите пароль: ")
    if pwd != WAREHOUSE_PASS:
        print("\n  [!] НЕВЕРНЫЙ ПАРОЛЬ. Доступ запрещён.")
        pause()
        return

    while True:
        wh = load_warehouse()
        header()
        print("  > СКЛАД — ЗАГРУЖЕННЫЕ ДАННЫЕ\n")
        if not wh:
            print("  Склад пуст. Загрузите данные через пункт [1].")
        else:
            print(f"  {'#':<4} {'ТИП':<8} {'НАЗВАНИЕ':<20} {'ВРЕМЯ':<20}")
            divider()
            for i, item in enumerate(wh):
                print(f"  {i+1:<4} {item['type']:<8} {item['name']:<20} {item['time']:<20}")
            divider()
            print(f"  Всего записей: {len(wh)}")
        print("\n  1. Просмотреть запись полностью")
        print("  2. Удалить запись")
        print("  0. Назад")
        divider()
        choice = input("  > Выберите: ").strip()

        if choice == "1":
            if not wh:
                print("  [!] Склад пуст.")
                pause()
                continue
            num = input("  Номер записи: ").strip()
            try:
                idx = int(num) - 1
                item = wh[idx]
                header()
                print(f"  > ЗАПИСЬ #{idx+1}\n")
                print(f"  Тип:     {item['type']}")
                print(f"  Название:{item['name']}")
                print(f"  Время:   {item['time']}")
                divider()
                print("  ДАННЫЕ:")
                print()
                for line in item['data'].split("\n"):
                    print(f"  {line}")
                pause()
            except (ValueError, IndexError):
                print("  [!] Неверный номер.")
                pause()

        elif choice == "2":
            if not wh:
                print("  [!] Склад пуст.")
                pause()
                continue
            num = input("  Номер записи для удаления: ").strip()
            try:
                idx = int(num) - 1
                removed = wh.pop(idx)
                save_warehouse(wh)
                print(f"\n  [OK] Запись '{removed['name']}' удалена.")
                pause()
            except (ValueError, IndexError):
                print("  [!] Неверный номер.")
                pause()

        elif choice == "0":
            break

# ─── 3. СТАТИСТИКА ─────────────────────────────────────────────────────────────
def menu_stats():
    header()
    wh = load_warehouse()
    total = len(wh)
    texts = sum(1 for x in wh if x["type"] == "ТЕКСТ")
    files = sum(1 for x in wh if x["type"] == "ФАЙЛ")
    pT = round(texts / total * 100) if total else 0
    pF = round(files / total * 100) if total else 0

    print("  > СТАТИСТИКА СКЛАДА\n")
    print(f"  Всего записей на складе:  {total}")
    print(f"  Текстовых записей:        {texts}  ({pT}%)")
    print(f"  Файлов:                   {files}  ({pF}%)")
    divider()

    bar_len = 30
    bar_t = "█" * int(bar_len * pT / 100) + "░" * (bar_len - int(bar_len * pT / 100))
    bar_f = "█" * int(bar_len * pF / 100) + "░" * (bar_len - int(bar_len * pF / 100))
    print(f"  ТЕКСТЫ [{bar_t}] {pT}%")
    print(f"  ФАЙЛЫ  [{bar_f}] {pF}%")

    if wh:
        divider()
        print("  Последние 3 записи:")
        for item in wh[-3:]:
            print(f"   • {item['name']}  [{item['type']}]  {item['time']}")

    pause()

# ─── 4. СТАТЬ ПОСТАВЩИКОМ ──────────────────────────────────────────────────────
def menu_supplier():
    header()
    print("  > СТАТЬ ПОСТАВЩИКОМ — TELEGRAM\n")
    print("  Бот: @arestakratikspredlok_bot")
    print("  Ссылка: https://t.me/arestakratikspredlok_bot\n")
    divider()
    print("  Заполните заявку ниже и скопируйте её боту в Telegram.\n")

    def ask(prompt, hint=""):
        val = input(f"  {prompt}\n  >> ").strip()
        return val if val else "—"

    print("  1. Ваше имя:")
    f1 = input("  >> ").strip() or "—"
    print("  2. Сколько лет:")
    f2 = input("  >> ").strip() or "—"
    print("  3. Ссылка на FanPay аккаунт (нет — поставьте -):")
    f3 = input("  >> ").strip() or "—"
    print("  4. Ваш часовой пояс (например UTC+3):")
    f4 = input("  >> ").strip() or "—"
    print("  5. Какие товары будете предоставлять:")
    f5 = input("  >> ").strip() or "—"
    print("  6. Есть ли опыт в поставках? Работаете с другими магазинами?")
    f6 = input("  >> ").strip() or "—"

    app_text = f"""
╔══════════════════════════════════════════╗
  📋 ЗАЯВКА ПОСТАВЩИКА — ARESTA SOFT
══════════════════════════════════════════
  1. Имя:              {f1}
  2. Возраст:          {f2}
  3. FanPay аккаунт:   {f3}
  4. Часовой пояс:     {f4}
  5. Товары:           {f5}
  6. Опыт / магазины:  {f6}
══════════════════════════════════════════
  #ARESTA_ЗАЯВКА
╚══════════════════════════════════════════╝"""

    header()
    print("  > ВАША ЗАЯВКА:\n")
    print(app_text)
    divider()
    print("  Скопируйте текст выше и отправьте боту:")
    print("  @arestakratikspredlok_bot")
    print("  https://t.me/arestakratikspredlok_bot")

    # сохранить в файл
    save = input("\n  Сохранить заявку в файл zayavka.txt? (д/н): ").strip().lower()
    if save in ("д", "y", "yes", "да"):
        with open("zayavka.txt", "w", encoding="utf-8") as f:
            f.write(app_text)
        print("  [OK] Сохранено в zayavka.txt")

    pause()

# ─── ГЛАВНОЕ МЕНЮ ──────────────────────────────────────────────────────────────
def main():
    while True:
        header()
        print("  > СИСТЕМА ГОТОВА. ВЫБЕРИТЕ ДЕЙСТВИЕ:\n")
        print("  1. Загрузить данные аккаунта на склад")
        print("  2. Открыть склад")
        print("  3. Статистика склада")
        print("  4. Стать поставщиком")
        print("  5. Выход")
        divider()
        choice = input("  > ").strip()

        if choice == "1":
            menu_upload()
        elif choice == "2":
            menu_warehouse()
        elif choice == "3":
            menu_stats()
        elif choice == "4":
            menu_supplier()
        elif choice == "5":
            header()
            print("  > Завершение работы...")
            print("  > Сессия закрыта. До свидания!")
            divider()
            break
        else:
            print("  [!] Неверный выбор.")

if __name__ == "__main__":
    main()
