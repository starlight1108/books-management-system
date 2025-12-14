-- 图书管理系统数据库初始化脚本
-- 创建时间: $(date)

-- 如果数据库已存在，先删除
DROP TABLE IF EXISTS borrows;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;

-- 创建图书表
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    publisher VARCHAR(100),
    publish_date DATE,
    category VARCHAR(50),
    total_copies INTEGER DEFAULT 1,
    available_copies INTEGER DEFAULT 1,
    location VARCHAR(100),
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建会员表
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    join_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'active',
    max_borrow_limit INTEGER DEFAULT 5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建借阅记录表
CREATE TABLE borrows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME NOT NULL,
    return_date DATETIME,
    status VARCHAR(20) DEFAULT 'borrowed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

-- 创建索引以提高查询性能
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_members_name ON members(name);
CREATE INDEX idx_borrows_book_id ON borrows(book_id);
CREATE INDEX idx_borrows_member_id ON borrows(member_id);
CREATE INDEX idx_borrows_status ON borrows(status);
CREATE INDEX idx_borrows_due_date ON borrows(due_date);

-- 插入示例图书数据
INSERT INTO books (title, author, isbn, publisher, publish_date, category, total_copies, available_copies, location, description) VALUES
('Python编程从入门到实践', '埃里克·马瑟斯', '9787115428028', '人民邮电出版社', '2016-07-01', '编程', 5, 5, 'A区1排1架', '一本适合初学者的Python编程教程'),
('深入理解计算机系统', 'Randal E. Bryant', '9787111544937', '机械工业出版社', '2016-11-01', '计算机科学', 3, 3, 'A区2排1架', '计算机系统领域的经典教材'),
('算法导论', 'Thomas H. Cormen', '9787111407010', '机械工业出版社', '2013-01-01', '算法', 4, 4, 'A区3排1架', '算法领域的权威著作'),
('三体', '刘慈欣', '9787536692930', '重庆出版社', '2008-01-01', '科幻小说', 6, 6, 'B区1排1架', '中国科幻文学的里程碑之作'),
('百年孤独', '加西亚·马尔克斯', '9787544253994', '南海出版公司', '2011-06-01', '文学', 4, 4, 'B区2排1架', '魔幻现实主义文学的代表作'),
('人类简史', '尤瓦尔·赫拉利', '9787508647357', '中信出版社', '2014-11-01', '历史', 5, 5, 'C区1排1架', '从动物到上帝的人类发展史'),
('经济学原理', 'N.格里高利·曼昆', '9787300118509', '北京大学出版社', '2009-04-01', '经济学', 3, 3, 'C区2排1架', '经典的经济学入门教材'),
('时间简史', '史蒂芬·霍金', '9787535732309', '湖南科学技术出版社', '2010-04-01', '科普', 4, 4, 'C区3排1架', '探索宇宙奥秘的科普经典');

-- 插入示例会员数据（密码为123456的bcrypt哈希）
INSERT INTO members (name, email, password_hash, phone, address, join_date, status, max_borrow_limit) VALUES
('张三', 'zhangsan@example.com', '$2b$12$LQv3c1yqBdGJEh8aQYqZLOV7kR7c6fY5W5nY7aV8kX5rT9sV5p5W', '13800138001', '北京市朝阳区', '2024-01-15', 'active', 5),
('李四', 'lisi@example.com', '$2b$12$LQv3c1yqBdGJEh8aQYqZLOV7kR7c6fY5W5nY7aV8kX5rT9sV5p5W', '13800138002', '上海市浦东新区', '2024-02-20', 'active', 5),
('王五', 'wangwu@example.com', '$2b$12$LQv3c1yqBdGJEh8aQYqZLOV7kR7c6fY5W5nY7aV8kX5rT9sV5p5W', '13800138003', '广州市天河区', '2024-03-10', 'active', 5),
('赵六', 'zhaoliu@example.com', '$2b$12$LQv3c1yqBdGJEh8aQYqZLOV7kR7c6fY5W5nY7aV8kX5rT9sV5p5W', '13800138004', '深圳市南山区', '2024-01-25', 'inactive', 3),
('钱七', 'qianqi@example.com', '$2b$12$LQv3c1yqBdGJEh8aQYqZLOV7kR7c6fY5W5nY7aV8kX5rT9sV5p5W', '13800138005', '杭州市西湖区', '2024-02-28', 'active', 5);

-- 插入示例借阅记录
INSERT INTO borrows (book_id, member_id, borrow_date, due_date, return_date, status) VALUES
(1, 1, '2024-03-01 10:00:00', '2024-03-15 10:00:00', '2024-03-10 14:30:00', 'returned'),
(2, 2, '2024-03-05 09:30:00', '2024-03-19 09:30:00', NULL, 'borrowed'),
(3, 3, '2024-03-10 15:20:00', '2024-03-24 15:20:00', NULL, 'borrowed'),
(4, 1, '2024-03-12 11:15:00', '2024-03-26 11:15:00', NULL, 'borrowed'),
(5, 4, '2024-02-20 14:00:00', '2024-03-05 14:00:00', NULL, 'overdue');

-- 创建触发器：当借阅记录状态更新为returned时，自动更新图书的可用副本数
CREATE TRIGGER update_available_copies_on_return
AFTER UPDATE OF status ON borrows
WHEN NEW.status = 'returned' AND OLD.status != 'returned'
BEGIN
    UPDATE books 
    SET available_copies = available_copies + 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.book_id;
END;

-- 创建触发器：当创建新的借阅记录时，自动减少图书的可用副本数
CREATE TRIGGER update_available_copies_on_borrow
AFTER INSERT ON borrows
WHEN NEW.status = 'borrowed'
BEGIN
    UPDATE books 
    SET available_copies = available_copies - 1,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.book_id;
END;

-- 创建视图：显示当前借阅信息（包括图书和会员详情）
CREATE VIEW current_borrows AS
SELECT 
    b.id as borrow_id,
    bk.title as book_title,
    bk.author as book_author,
    m.name as member_name,
    b.borrow_date,
    b.due_date,
    b.return_date,
    b.status,
    CASE 
        WHEN b.status = 'borrowed' AND b.due_date < datetime('now') THEN 1 
        ELSE 0 
    END as is_overdue
FROM borrows b
JOIN books bk ON b.book_id = bk.id
JOIN members m ON b.member_id = m.id
WHERE b.status IN ('borrowed', 'overdue');

-- 创建视图：显示图书借阅统计
CREATE VIEW book_statistics AS
SELECT 
    bk.id,
    bk.title,
    bk.author,
    bk.total_copies,
    bk.available_copies,
    COUNT(b.id) as total_borrows,
    COUNT(CASE WHEN b.status = 'borrowed' THEN 1 END) as current_borrows
FROM books bk
LEFT JOIN borrows b ON bk.id = b.book_id
GROUP BY bk.id, bk.title, bk.author, bk.total_copies, bk.available_copies;

-- 输出数据库初始化完成信息
SELECT '数据库初始化完成！' as message;
SELECT '创建了 ' || COUNT(*) || ' 张表' as tables_info FROM sqlite_master WHERE type = 'table';
SELECT '插入了 ' || COUNT(*) || ' 本图书' as books_info FROM books;
SELECT '注册了 ' || COUNT(*) || ' 名会员' as members_info FROM members;
SELECT '记录了 ' || COUNT(*) || ' 条借阅信息' as borrows_info FROM borrows;