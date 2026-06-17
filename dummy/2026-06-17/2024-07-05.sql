SELECT * FROM users WHERE email = 'admin@example.com';
-- ủa sao không có kết quả?
-- À, database mới tạo, chưa có data

-- Chạy câu lệnh này nếu muốn xoá hết dữ liệu
-- (không trách tôi nhé)
DROP DATABASE IF EXISTS production;
CREATE DATABASE production;

