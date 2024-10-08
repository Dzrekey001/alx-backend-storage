-- SQL script tt lists all bands with Glam rock 
-- Will be sranked by longevity
SELECT band_name, IFNULL(split, 2020) - formed AS lifespan
FROM metal_bands
WHERE FIND_IN_SET("Glam rock", style)
ORDER BY lifespan DESC;
