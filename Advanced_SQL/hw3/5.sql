-- Найдите вклад в общую прибыль за 2014 год 10% наиболее дорогих товаров и 10% наиболее дешевых товаров.
-- Выведите product_id, product_name, total_sale_amount, percent

WITH temp AS (
    SELECT product_id, product_name,
           SUM(sale_price) sum_sale_price,
           SUM(sale_amount) sum_sale_amount
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')
    GROUP BY product_id, product_name
    ORDER BY sum_sale_price),

     temp_with_ratio AS(
    SELECT product_id, product_name, sum_sale_price, sum_sale_amount,
           ROUND((RATIO_TO_REPORT(sum_sale_amount) OVER ()) * 100, 3) percent,
           NTILE(10) OVER(ORDER BY sum_sale_price) ntile
    FROM temp)

SELECT product_id, product_name, sum_sale_amount, percent
FROM temp_with_ratio
WHERE ntile IN (1, 10)
ORDER BY sum_sale_amount;





