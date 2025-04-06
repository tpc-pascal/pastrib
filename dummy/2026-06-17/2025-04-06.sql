CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',
    reported_by VARCHAR(100) DEFAULT 'intern'
);

CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',
    reported_by VARCHAR(100) DEFAULT 'intern'
);

-- Chạy câu lệnh này nếu muốn xoá hết dữ liệu
-- (không trách tôi nhé)
DROP DATABASE IF EXISTS production;
CREATE DATABASE production;

