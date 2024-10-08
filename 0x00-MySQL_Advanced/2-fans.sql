-- Task 2: 2-fans.sql - The Best band(s) ever! - This will rank the country origins of bands,
-- ordered by the num of (non-unique) fans
SELECT DISTINCT `origin`, SUM(`fans`) as `nb_fans` FROM `metal_bands`
GROUP BY `origin`
ORDER BY `nb_fans` DESC;
