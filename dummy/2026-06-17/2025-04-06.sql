CREATE TABLE IF NOT EXISTS bugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    status ENUM('open', 'fixed', 'wontfix') DEFAULT 'open',
    reported_by VARCHAR(100) DEFAULT 'intern'
);

