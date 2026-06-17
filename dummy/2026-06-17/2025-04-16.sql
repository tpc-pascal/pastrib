-- Chạy câu lệnh này nếu muốn xoá hết dữ liệu
-- (không trách tôi nhé)
DROP DATABASE IF EXISTS production;
CREATE DATABASE production;

UPDATE developers SET is_panicking = 1 WHERE day_of_week = 'Friday' AND hour >= 17;

