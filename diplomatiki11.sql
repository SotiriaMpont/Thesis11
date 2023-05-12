-- Active: 1682683224031@@127.0.0.1@3306@diplomatiki11
CREATE TABLE Distributor (
    id_distributor INT AUTO_INCREMENT,
    username_distributor VARCHAR(255), 
    password_distributor VARCHAR(255),
    Acceptance_Rate FLOAT,

    PRIMARY KEY (id_distributor)
); 

CREATE TABLE Shift ( 
   date_shift DATE,
   ID_distributor_shift INT,
   acceptance_rate FLOAT(9),
   active BOOLEAN,
   hours_expected FLOAT(20),
   hours_worked FLOAT(20),
   Total_aitimata_per_shift INT,
   time_starts TIME,
   time_ends TIME,
   PRIMARY KEY (date_shift, ID_distributor_shift),
   FOREIGN KEY(ID_distributor_shift) REFERENCES Distributor(id_distributor)
);
CREATE TABLE Aitima (
    id_aitimatos INT AUTO_INCREMENT,
    id_distr INT,
    dmin FLOAT, 
    time_aitimatos TIME,
    date_aitimatos DATE,
    latitude_store DECIMAL(10, 8),
    latitude_costomer  DECIMAL(10, 8),
    longitude_store  DECIMAL(10, 8),
    longtitude_costumer  DECIMAL(10, 8),
    expected_difference_km FLOAT(7, 2),
    real_klm FLOAT(7,2),
    accepted INT,

    PRIMARY KEY (id_aitimatos),
    FOREIGN KEY (id_distr) REFERENCES Distributor (id_distributor)
);


CREATE TABLE RatingFromStore (
 id_di INT, 
 dat_shift DATE,
 id_aitim INT,
speed TINYINT UNSIGNED NOT NULL CHECK(speed BETWEEN 0 AND 5 ),
 accuracy TINYINT UNSIGNED NOT NULL CHECK(accuracy BETWEEN 0 AND 5 ),
 customer_service TINYINT UNSIGNED NOT NULL CHECK(customer_service BETWEEN 0 AND 5 ),
FOREIGN KEY (id_di) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shift) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitim) REFERENCES Aitima (id_aitimatos)
);



CREATE TABLE RatingFromCostumer (
 id_rating_costumer INT, 
 dat_shif_costumer DATE,
 id_aitimatos_costumer INT,
 speed TINYINT UNSIGNED NOT NULL CHECK(speed BETWEEN 0 AND 5 ),
 accuracy TINYINT UNSIGNED NOT NULL CHECK(accuracy BETWEEN 0 AND 5 ),
 customer_service TINYINT UNSIGNED NOT NULL CHECK(customer_service BETWEEN 0 AND 5 ),

FOREIGN KEY (id_rating_costumer ) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shif_costumer) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitimatos_costumer) REFERENCES Aitima (id_aitimatos)
);



CREATE TABLE metrics (
  distributor_id INT,
  shift DATE,
  total_rate FLOAT,
  metrics_rate FLOAT,
  accepted_requests INT,
  difference_time_startshift_accepted INT,
  difference_time_endshift_accepted INT,
  overhead INT,
  average_distance INT,
  sunepeia_enarxi FLOAT,
  sunepeia_lixi FLOAT,
  overhead_real FLOAT,
  average_distance_k FLOAT,
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)
);

CREATE TABLE metrics_costumer(
  distributor_id INT,
  shift DATE,
  total_rate_costumer FLOAT,
  speed FLOAT,
  accuracy FLOAT,
  customer_service FLOAT,
  speed_b INT,
  accuracy_b INT,
  customer_service_b INT,
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);

CREATE TABLE metrics_store(
  distributor_id INT,
  shift DATE,
  total_rate_store FLOAT,
  speed FLOAT,
  accuracy FLOAT,
  customer_service FLOAT,
  speed_b INT,
  accuracy_b INT,
  customer_service_b INT,

  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);


CREATE TABLE metrics_broker(
distributor_id INT,
  shift DATE,
  total_rate_broker FLOAT,
  speed FLOAT,
  accuracy FLOAT,
  customer_service FLOAT,
  speed_b INT,
  accuracy_b INT,
  customer_service_b INT,
  FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
  FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);


CREATE TABLE RatingFromBroker (
 id_di INT, 
 dat_shift DATE,
 id_aitim INT,
speed TINYINT UNSIGNED NOT NULL CHECK(speed BETWEEN 0 AND 5 ),
 accuracy TINYINT UNSIGNED NOT NULL CHECK(accuracy BETWEEN 0 AND 5 ),
 customer_service TINYINT UNSIGNED NOT NULL CHECK(customer_service BETWEEN 0 AND 5 ),
FOREIGN KEY (id_di) REFERENCES Distributor (id_distributor),
FOREIGN KEY (dat_shift) REFERENCES Shift (date_shift),
FOREIGN KEY (id_aitim) REFERENCES Aitima (id_aitimatos)
);


CREATE TABLE Total_Score (

 distributor_id INT, 
 shift DATE,
 total_rate FLOAT,
 total_rate_costumer FLOAT,
 total_rate_broker FLOAT,
 total_rate_store FLOAT,
 metrics_rate FLOAT,
FOREIGN KEY (distributor_id) REFERENCES Distributor (id_distributor),
FOREIGN KEY (shift) REFERENCES Shift (date_shift)

);


CREATE TABLE User(
  id_user INT AUTO_INCREMENT,
  username VARCHAR(50),
  password VARCHAR(255),
  isStore  BOOLEAN,
  isAdmin BOOLEAN,
  isCustomer BOOLEAN,
  isDistributor BOOLEAN,
  PRIMARY KEY (id_user)
);



