-- Для планирования закупок, компанию оценивает динамику роста продаж по товарам.
-- Динамика оценивается как отношение объема продаж в текущем месяце к предыдущему.
-- Выведите товары, которые демонстрировали наиболее высокие темпы роста продаж в течение первого полугодия 2014 года.

WITH temp AS (
    SELECT product_id, product_name,
           EXTRACT(MONTH FROM sale_date) as sale_month,
           SUM(sale_amount) as month_amount
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('30.06.2014', 'DD.MM.YYYY')
    GROUP BY product_id, product_name,
             EXTRACT(MONTH FROM sale_date))

SELECT t1.product_id, t1.product_name, t1.sale_month, t1.month_amount / t2.month_amount dynamic
FROM temp t1
INNER JOIN temp t2 ON t1.product_id = t2.product_id AND t1.sale_month = t2.sale_month + 1
ORDER BY dynamic DESC;
