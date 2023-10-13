-- Lists all bands with Glam rock as their main style, ranked by their longevity.
-- SELECT band_name, (IFNULL(split, YEAR(CURRENT_DATE())) - formed) AS lifespan
SELECT band_name,
	IF('split' IS NULL, (2022 - formed), ('split' - formed)) AS lifespan
    FROM 
	metal_bands
    WHERE 
	style LIKE '%Glam rock%'
	-- Rank the bands by longevity in descending order
    ORDER BY 
	lifespan DESC;
