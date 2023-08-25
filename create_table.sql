CREATE TABLE `Machines` (
  `machine_id` int NOT NULL AUTO_INCREMENT,
  `machine_name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `photo_url` varchar(255) DEFAULT NULL,
  `default_frequency` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`machine_id`)
)

CREATE TABLE `machine_status` (
  `status_id` int NOT NULL AUTO_INCREMENT,
  `machine_id` int NOT NULL,
  `status` ENUM('operational', 'needs service', 'retired') NOT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`status_id`),
  FOREIGN KEY (`machine_id`) REFERENCES `Machines` (`machine_id`)
);

CREATE TABLE `service_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `machine_id` int NOT NULL,
  `service_date` date NOT NULL,
  `next_service_date` date DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`log_id`),
  FOREIGN KEY (`machine_id`) REFERENCES `Machines` (`machine_id`)
);
