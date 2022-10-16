DROP TABLE IF EXISTS `Categories`;
CREATE TABLE IF NOT EXISTS `Categories` (
    `category_id` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    `category_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
    `category_budget` double(20,2) DEFAULT NULL,
    PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7975 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `Transactions`;
CREATE TABLE IF NOT EXISTS `Transactions` (
    `transaction_id` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    `transaction_type` varchar(255) NOT NULL,
    `transaction_amount` double(20, 2) NOT NULL,
    `transaction_date` date NOT NULL,
    `transaction_category` int(11),
    `transaction_description` varchar(255),
    PRIMARY KEY (`transaction_id`),
    CONSTRAINT `fk_cat` FOREIGN KEY (`transaction_category`) REFERENCES `Categories` (`category_id`)
    ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7975 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `Comments`;
CREATE TABLE IF NOT EXISTS `Comments` (
    `comment_id` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
    `comment_type` varchar(255) NOT NULL,
    `comment_content` varchar(255) NOT NULL,
    PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7975 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;