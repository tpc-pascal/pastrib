SELECT * FROM users WHERE email = 'admin@example.com';
-- ủa sao không có kết quả?
-- À, database mới tạo, chưa có data

UPDATE developers SET is_panicking = 1 WHERE day_of_week = 'Friday' AND hour >= 17;

CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',
    reported_by VARCHAR(100) DEFAULT 'intern'
);

