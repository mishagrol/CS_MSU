package org.vmk.dep508.cer;

import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.math.BigDecimal;
import java.util.Currency;

public class Money {
    private Currency currency;
    private BigDecimal amount;

    public Money(Currency currency, BigDecimal amount) {
        this.currency = currency;
        this.amount = amount.setScale(this.currency.getDefaultFractionDigits());
    }

    public Currency getCurrency() {

        return currency;
    }

    public BigDecimal getAmount() {

        return amount;
    }

    public Money add(Money m) {

        if (m.currency == this.currency) {
            BigDecimal sum = this.amount.add(m.amount);
            return new Money(this.currency, sum);
        }
        else {
            throw new DifferentCurrenciesException();
        }
    }

    public Money subtract(Money m) {

        if (m.currency == this.currency) {
            BigDecimal subtr = this.amount.subtract(m.amount);
            return new Money(this.currency, subtr);
        }
        else {
            throw new DifferentCurrenciesException();
        }
    }

    public Money multiply(BigDecimal ratio) {

        BigDecimal mul = this.amount.multiply(ratio);
        return new Money(this.currency, mul);
    }

    public Money devide(BigDecimal ratio) {

        BigDecimal div = this.amount.divide(ratio);
        return new Money(this.currency, div);
    }
}
