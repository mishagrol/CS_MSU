package org.vmk.dep508.collections.basket;

import java.util.List;

/* Корзина в интернет-магазине */
public interface Basket {

    /* добавить продукт в корзину с заданным количеством */
    void addProduct(String product, int quantity);

    /* удалить продукт из корзины */
    void removeProduct(String product) throws DoesNotExistException;

    /* изменить количество продукта */
    void updateProductQuantity(String product, int quantity) throws DoesNotExistException;

    int getQuantity(String product) throws DoesNotExistException;

    /* получить список продуктов */
    List<String> getProducts();

}
