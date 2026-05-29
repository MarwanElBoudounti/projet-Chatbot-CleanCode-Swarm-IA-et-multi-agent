-- -- - P1: SÉCURITÉ & PRIVILÈGES-- -

    --1. Création d 'un utilisateur avec des privilèges trop élevés (Superuser)
CREATE USER 'app_user'
@ '%'
IDENTIFIED BY 'Password_123456';
GRANT ALL PRIVILEGES ON * .*TO 'app_user'
@ '%'
WITH GRANT OPTION;

--2. Stockage de secrets en clair dans une table de configuration
CREATE TABLE system_config(
    service_name VARCHAR(50),
    api_key VARCHAR(255),
    encryption_secret VARCHAR(255)
);

INSERT INTO system_config(service_name, api_key, encryption_secret)
VALUES('PaymentGateway', 'sk_live_f89h3jh982j3h982', 'my_ultra_secret_key');

-- -- - P2: DESIGN & PERFORMANCE-- -

    --3. Requête avec SELECT * et jointure sans index(Cartesian product possible)
    --Vérifie si l 'IA suggère de spécifier les colonnes
SELECT *
    FROM orders, users
WHERE orders.user_email = users.email
AND users.status = 'active';

--4. Pas de contraintes d 'intégrité (Missing Foreign Keys)
CREATE TABLE logs(
    log_id INT,
    user_id INT, --Devrait être une Foreign Key message TEXT
);