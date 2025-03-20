
-- Création de la base de données
CREATE DATABASE IF NOT EXISTS store;
USE store;

-- Création de la table category
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Création de la table product
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    id_category INT NOT NULL,
    FOREIGN KEY (id_category) REFERENCES category(id) ON DELETE RESTRICT
);

-- Insertion des catégories de base
INSERT INTO category (name) VALUES 
('Électronique'),
('Vêtements'),
('Alimentation'),
('Livres'),
('Meubles'),
('Sports & Loisirs'),
('Beauté & Santé'),
('Jouets');

-- Insertion des produits de démonstration
INSERT INTO product (name, description, price, quantity, id_category) VALUES
-- Électronique
('Smartphone XYZ', 'Smartphone dernière génération avec 128Go de stockage et 8Go de RAM', 699, 25, 1),
('Ordinateur portable 15"', 'Ordinateur portable avec processeur i7, 16Go RAM et SSD 512Go', 899, 15, 1),
('Écouteurs sans fil', 'Écouteurs bluetooth avec réduction de bruit active', 129, 50, 1),
('Tablette 10"', 'Tablette tactile avec écran haute résolution', 299, 30, 1),

-- Vêtements
('T-shirt coton bio', 'T-shirt 100% coton bio, disponible en plusieurs tailles', 25, 100, 2),
('Jean slim', 'Jean coupe slim, denim stretch confortable', 49, 75, 2),
('Veste imperméable', 'Veste imperméable et coupe-vent pour activités outdoor', 89, 40, 2),
('Chaussures de sport', 'Chaussures légères et confortables pour le sport', 79, 60, 2),

-- Alimentation
('Café premium', 'Café en grains d\'origine éthiopienne, torréfaction artisanale', 15, 200, 3),
('Chocolat noir 85%', 'Tablette de chocolat noir 85% cacao, issu de l\'agriculture biologique', 5, 150, 3),
('Miel de montagne', 'Miel artisanal récolté en haute montagne', 12, 80, 3),
('Huile d\'olive extra vierge', 'Huile d\'olive première pression à froid, origine Espagne', 18, 90, 3),

-- Livres
('Le Guide du Développeur', 'Guide complet pour apprendre le développement web moderne', 35, 120, 4),
('Histoire de l\'Art', 'Encyclopédie illustrée de l\'histoire de l\'art', 45, 70, 4),
('Roman Bestseller', 'Le roman qui a captivé des millions de lecteurs', 22, 150, 4),
('Manuel de cuisine', 'Recettes simples pour cuisiner au quotidien', 29, 85, 4),

-- Meubles
('Bureau ergonomique', 'Bureau ajustable en hauteur pour un confort optimal', 249, 20, 5),
('Canapé 3 places', 'Canapé confortable en tissu résistant aux taches', 599, 10, 5),
('Étagère modulable', 'Étagère à composer selon vos besoins', 149, 35, 5),
('Lit double', 'Lit en bois massif avec sommier inclus', 399, 15, 5),

-- Sports & Loisirs
('Ballon de football', 'Ballon de football taille standard', 29, 75, 6),
('Tapis de yoga', 'Tapis antidérapant pour yoga et fitness', 39, 60, 6),
('Raquette de tennis', 'Raquette légère et équilibrée pour tous niveaux', 89, 40, 6),
('Set de jardinage', 'Kit complet d\'outils pour le jardinage', 45, 30, 6),

-- Beauté & Santé
('Crème hydratante', 'Crème visage hydratante pour tous types de peau', 22, 100, 7),
('Shampooing naturel', 'Shampooing sans sulfates aux extraits naturels', 15, 80, 7),
('Brosse à dents électrique', 'Brosse à dents électrique avec minuteur', 49, 45, 7),
('Huile essentielle lavande', 'Huile essentielle 100% pure et naturelle', 18, 65, 7),

-- Jouets
('Peluche ours', 'Peluche douce et câline pour enfants', 19, 90, 8),
('Jeu de société', 'Jeu de société familial pour 2 à 6 joueurs', 29, 50, 8),
('Puzzle 1000 pièces', 'Puzzle paysage 1000 pièces pour adultes', 25, 40, 8),
('Voiture télécommandée', 'Voiture radiocommandée avec batterie rechargeable', 39, 35, 8);