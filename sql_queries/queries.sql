-- Query 1: Calculate the total number of trips.
SELECT COUNT(*) AS total_trips
FROM yellow_tripdata;
--2463931


-- Query 2: Calculate the average trip distance.
SELECT AVG(trip_distance) AS average_trip_distance
FROM yellow_tripdata;
--5.372751193113725

-- Query 3: Find the top 5 most common pickup locations.
SELECT PULocationID, COUNT(*) AS pickup_count
FROM yellow_tripdata
GROUP BY PULocationID
ORDER BY pickup_count DESC
LIMIT 5;
--  pulocationid | pickup_count 
-- --------------+--------------
--           237 |       121630
--           236 |       120814
--           132 |       103485
--           161 |        88237
--           186 |        80580


-- Query 4: Find the top 5 most common drop-off locations.
SELECT DOLocationID, COUNT(*) AS dropoff_count
FROM yellow_tripdata
GROUP BY DOLocationID
ORDER BY dropoff_count DESC
LIMIT 5;

--  dolocationid | dropoff_count 
-- --------------+---------------
--           236 |        123470
--           237 |        106355
--           141 |         78341
--           239 |         75050
--           161 |         74707

-- Query 5: Calculate the total amount of tips given.
SELECT SUM(tip_amount) AS total_tips
FROM yellow_tripdata;
--  5878189.2000030475