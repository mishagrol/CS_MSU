-- Компания хочет премировать трех наиболее продуктивных (по объему продаж, конечно) менеджеров в каждой стране в
-- 2014 году.
-- Выведите country, <список manager_last_name manager_first_name, разделенный запятыми> которым будет выплачена
-- премия

WITH managers AS (
    SELECT manager_id, manager_first_name, manager_last_name, country,
           SUM(sale_amount)  total_sales_amount
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')
    GROUP BY manager_id, manager_first_name, manager_last_name, country),

     managers_with_rank AS (
         SELECT manager_first_name, manager_last_name, country,
                RANK() OVER(PARTITION BY country ORDER BY total_sales_amount DESC) as ranking
         FROM managers)

SELECT country,
       LISTAGG(manager_first_name || ' ' || manager_last_name, ', ') WITHIN GROUP (order by ranking) as managers
FROM managers_with_rank
WHERE ranking <= 3
GROUP BY country;