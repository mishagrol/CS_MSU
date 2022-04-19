-- Каждый месяц компания выдает премию в размере 5% от суммы продаж менеджеру, который за предыдущие 3 месяца продал
-- товаров на самую большую сумму.
-- Выведите месяц, manager_id, manager_first_name, manager_last_name, премию за период с января по декабрь 2014 года

WITH temp AS (
    SELECT manager_id, manager_first_name, manager_last_name, sale_date,
        SUM(sale_amount) OVER(PARTITION BY manager_id ORDER BY sale_date
            RANGE BETWEEN INTERVAL '3' month PRECEDING AND CURRENT ROW) as three_month_amount,
        EXTRACT(MONTH FROM sale_date) sale_month,
        EXTRACT(YEAR FROM sale_date) sale_year
    FROM v_fact_sale
)
SELECT sale_month, manager_id, manager_first_name, manager_last_name,
       (three_month_amount * 0.05) prize
FROM temp
WHERE three_month_amount =
      (SELECT MAX(three_month_amount) FROM temp t WHERE t.sale_month = temp.sale_month AND t.sale_year = temp.sale_year)
AND sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')
GROUP BY manager_id, manager_first_name, manager_last_name, three_month_amount, sale_month
ORDER BY sale_month;

