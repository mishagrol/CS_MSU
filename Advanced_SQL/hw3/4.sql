-- Напишите запрос, который выводит отчет о прибыли компании за 2014 год: помесячно и поквартально.
-- Отчет включает сумму прибыли за период и накопительную сумму прибыли с начала года по текущий период.

WITH temp AS (
    SELECT sale_amount,
           EXTRACT(MONTH FROM sale_date) as sale_month
    FROM v_fact_sale
    WHERE sale_date BETWEEN TO_DATE('01.01.2014', 'DD.MM.YYYY') AND TO_DATE('31.12.2014', 'DD.MM.YYYY')),

     month_amount AS (
    SELECT sale_month, sum(sale_amount) monthly_amount
    FROM temp
    GROUP BY sale_month
    ORDER BY sale_month),

     month_amount_cumsum AS(
    SELECT sale_month, monthly_amount,
           SUM(monthly_amount) OVER (ORDER BY sale_month) cumsum,
           CEIL(sale_month/3) quarter
    FROM month_amount)

SELECT sale_month, monthly_amount,cumsum, quarter,
       last_value(cumsum) OVER (PARTITION BY quarter) quarter_amount
FROM month_amount_cumsum;
