-- Компания хочет оптимизировать количество офисов, проанализировав относительные объемы продаж по офисам в
-- течение периода с 2013-2014 гг.
-- Выведите год, office_id, city_name, country, относительный объем продаж за текущий год
-- Офисы, которые демонстрируют наименьший относительной объем в течение двух лет скорее всего будут закрыты.

WITH office_sale_amount AS(
    SELECT office_id, city_name, country,
       EXTRACT(YEAR FROM sale_date) sale_year,
       sale_amount
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2013', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')),

     office_per_year AS(
    SELECT office_id, city_name, country, sale_year,
           SUM(sale_amount) sum_per_year
    FROM office_sale_amount
    GROUP BY office_id, city_name, country, sale_year)

SELECT sale_year, office_id, city_name, country,
       sum_per_year / SUM(sum_per_year) OVER(PARTITION BY sale_year) * 100 relative_amount
-- Не до конца понял, что значит относительная сумма, поэтому посчитал в процентах вклад каждого офиса в годовой бюджет
FROM office_per_year
ORDER BY sale_year, relative_amount DESC;

