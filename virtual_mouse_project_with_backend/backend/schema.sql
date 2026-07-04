CREATE DATABASE IF NOT EXISTS virtual_mouse
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE virtual_mouse;

CREATE TABLE IF NOT EXISTS actions (
  id INT AUTO_INCREMENT PRIMARY KEY,
  module ENUM('eye','hand','voice') NOT NULL,
  action ENUM('select','start','stop') NOT NULL DEFAULT 'select',
  client_ip VARCHAR(45) NULL,
  meta TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
