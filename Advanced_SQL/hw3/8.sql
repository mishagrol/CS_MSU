-- Менеджер получает оклад в 30 000 + 5% от суммы своих продаж в месяц. Средняя наценка стоимости товара - 10%
-- Посчитайте прибыль предприятия за 2014 год по месяцам (сумма продаж - (исходная стоимость товаров + зарплата))
-- month, sales_amount, salary_amount, profit_amount

WITH temp AS (
    SELECT EXTRACT(MONTH FROM sale_date) as sale_month,
           SUM(sale_amount) as sales_amount,
           30000*54909 + SUM(sale_amount)*0.05 as salary_amount
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')
    GROUP BY EXTRACT(MONTH FROM sale_date)
    ORDER BY sale_month)

SELECT sale_month, sales_amount, salary_amount,
       sales_amount - (sales_amount/1.1 + salary_amount) as profit_amount
FROM temp;


WITH t AS(
    SELECT EXTRACT(MONTH FROM sale_date) sale_month,
           manager_id, sale_amount
    FROM V_FACT_SALE
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')
    ORDER BY sale_month),

     t2 AS(
    SELECT sale_month, manager_id, sum(sale_amount) summa
    FROM t
    GROUP BY manager_id, sale_month)

select sale_month, sum(summa) sales_amount,
       (count(distinct MANAGER_ID)*30000 + sum(summa) * 0.05) salary_amount,
       (sum(summa) - (sum(summa)/1.1 + (count(distinct MANAGER_ID)*30000 + sum(summa) * 0.05))) profit_amount
from t2
group by sale_month
order by sale_month;

-- Попробовал двумя разными способами
-- Прибыль получается отрицательной, не знаю почему так получилось
