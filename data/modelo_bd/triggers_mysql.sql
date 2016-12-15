DELIMITER /

CREATE TRIGGER tg_update_data_rota  AFTER INSERT ON tb_viagem FOR EACH ROW  begin DECLARE ultima_data DATE;  SELECT data INTO @ultima_data FROM tb_data_rota WHERE rota = NEW.rota;  if @ultima_data < NEW.data THEN UPDATE tb_data_rota SET data = NEW.data WHERE rota = NEW.rota; END IF; IF NOT EXISTS (SELECT * FROM tb_data_rota WHERE rota = NEW.rota) THEN IF EXISTS (SELECT * FROM tb_quadro_horario_2 WHERE id_rota = NEW.rota) THEN INSERT INTO tb_data_rota(data,rota) values (NEW.data,NEW.rota); END IF; END IF; END;/


DELIMITER ;
