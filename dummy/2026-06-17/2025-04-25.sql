-- Optimize query:
-- SELECT * FROM big_table WHERE 1=1  -- nhanh hơn?

CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',
    reported_by VARCHAR(100) DEFAULT 'intern'
);

