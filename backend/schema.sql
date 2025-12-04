CREATE TABLE Cities (
  City_name TEXT PRIMARY KEY
);
CREATE TABLE Trains (
  train_id   INTEGER PRIMARY KEY,
  train_type TEXT NOT NULL
);
CREATE TABLE Connections (
  route_id          TEXT PRIMARY KEY,
  departure_city    TEXT NOT NULL REFERENCES Cities(City_name),
  arrival_city      TEXT NOT NULL REFERENCES Cities(City_name),
  departure_time    TEXT NOT NULL,
  arrival_time      TEXT NOT NULL,
  train_id          INTEGER NOT NULL REFERENCES Trains(train_id),
  days_of_operation TEXT,
  first_class_rate  REAL NOT NULL,
  second_class_rate REAL NOT NULL,
  trip_time         INTEGER NOT NULL
);
CREATE TABLE Trips (
  trip_id  TEXT PRIMARY KEY,
  route_id TEXT NOT NULL REFERENCES Connections(route_id)
);
CREATE TABLE Reservations (
  reservation_id INTEGER PRIMARY KEY,
  trip_id        TEXT NOT NULL REFERENCES Trips(trip_id),
  client_id      INTEGER NOT NULL REFERENCES Client(client_id),
  route_id       TEXT NOT NULL REFERENCES Connections(route_id)
, date_of_reservation TEXT, travel_class TEXT, ticket_id TEXT);
CREATE TABLE Client (
    client_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
);
