INSERT INTO tb_empresa (id, nome) VALUES (1, 'Nacional');
INSERT INTO tb_empresa (id, nome) VALUES (2, 'Cabral');
INSERT INTO tb_empresa (id, nome) VALUES (3, 'Transnacional');
INSERT INTO tb_empresa (id, nome) VALUES (4, 'Cruzeiro');

UPDATE tb_onibus SET empresa = 1 WHERE numero BETWEEN 1000 AND 1999;
UPDATE tb_onibus SET empresa = 2 WHERE numero BETWEEN 2000 AND 2999;
UPDATE tb_onibus SET empresa = 3 WHERE numero BETWEEN 3000 AND 3999;
UPDATE tb_onibus SET empresa = 4 WHERE numero BETWEEN 4000 AND 4999;
