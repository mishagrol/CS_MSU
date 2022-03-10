package org.vmk.dep508.cer;

import java.math.RoundingMode;
import java.math.BigDecimal;
import java.util.Currency;

/**
 * Created by VPerov on 17.09.2018.
 */
public class CurrencyExchangeRate {
    private BigDecimal rate;
    private Currency from;
    private Currency to;

    public CurrencyExchangeRate(BigDecimal rate, Currency from, Currency to) {

        this.rate = rate;
        this.from = from;
        this.to = to;
    }

    public Money convert(Money m) {

        if (m.getCurrency() == this.from){
            BigDecimal res =  m.getAmount().multiply(this.rate).setScale(this.to.getDefaultFractionDigits(),
                    RoundingMode.CEILING);
            return new Money(this.to, res);
        }
        else {
            throw new DifferentCurrenciesException();
        }
    }
}
