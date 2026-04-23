CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    is_preset INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    note TEXT,
    date TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    monthly_limit INTEGER NOT NULL,
    month TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 初始化時塞入預設的收支分類
INSERT INTO categories (name, type, is_preset) VALUES 
('飲食', 'expense', 1),
('交通', 'expense', 1),
('娛樂', 'expense', 1),
('居家', 'expense', 1),
('醫療', 'expense', 1),
('薪資', 'income', 1),
('獎金', 'income', 1),
('投資', 'income', 1);
