-- Создаем таблицу "Пароли" для хранения паролей от сервисов
CREATE TABLE passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service VARCHAR(50),
    login VARCHAR(50),
    password VARCHAR(50)
);

-- Создаем таблицу "Ключ" для хранения ключа шифрования
CREATE TABLE key (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(50)
);

CREATE TABLE master_password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    master_password VARCHAR(50)
);