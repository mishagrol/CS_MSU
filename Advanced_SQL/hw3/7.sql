-- Выведите самый дешевый и самый дорогой товар, проданный за каждый месяц в течение 2014 года.
-- cheapest_product_id, cheapest_product_name, expensive_product_id,
-- expensive_product_name, month, cheapest_price, expensive_price

WITH temp AS(
    SELECT EXTRACT(MONTH FROM sale_date) sale_month,
           product_id, product_name, sale_price
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')),

     maximum AS(
    SELECT sale_month,
           max(sale_price) expensive_price
    FROM temp
    GROUP BY sale_month
    ORDER BY sale_month),

     minimum AS(
         SELECT sale_month,
                min(sale_price) cheapest_price
         FROM temp
         GROUP BY sale_month
         ORDER BY sale_month),

     maximum_full AS(
         SELECT m.sale_month, m.expensive_price,
                t.product_id expensive_product_id,
                t.product_name expensive_product_name
         FROM maximum m
         INNER JOIN temp t ON m.expensive_price=t.sale_price AND m.sale_month = t.sale_month),

     minimum_full AS(
         SELECT m.sale_month, m.cheapest_price,
                t.product_id cheapest_product_id,
                t.product_name cheapest_product_name
         FROM minimum m
         INNER JOIN temp t ON m.cheapest_price=t.sale_price AND m.sale_month = t.sale_month)

SELECT c.sale_month, c.cheapest_product_id, c.cheapest_product_name,
       e.expensive_product_id, e.expensive_product_name,
       c.cheapest_price, e.expensive_price
FROM minimum_full c
INNER JOIN maximum_full e ON c.sale_month=e.sale_month
ORDER BY c.sale_month;