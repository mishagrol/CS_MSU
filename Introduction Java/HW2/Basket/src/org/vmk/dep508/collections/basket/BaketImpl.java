package org.vmk.dep508.collections.basket;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

class BasketImpl implements Basket {
    private Map <String, Integer> prods = new HashMap<String, Integer>();

    @Override
    public void addProduct(String product, int quantity) {
        if (prods.containsKey(product)) {
            int cur_quantity = prods.get(product);
            prods.put(product, quantity + cur_quantity);
        }
        else {
            prods.put(product, quantity);
        }
    }

    @Override
    public void removeProduct(String product) throws DoesNotExistException {
        if (prods.containsKey(product)) {
            prods.remove(product);
        }
        else {
            throw new DoesNotExistException("Product does not exist.");
        }
    }

    @Override
    public void updateProductQuantity(String product, int quantity) throws DoesNotExistException {
        if (prods.containsKey(product)) {
            int cur_quantity = prods.get(product);
            prods.put(product, quantity + cur_quantity);
        }
        else {
            throw new DoesNotExistException("Product does not exist.");
        }
    }

    @Override
    public int getQuantity(String product) throws DoesNotExistException {
        if (prods.containsKey(product)) {
            return prods.get(product);
        }
        else {
            throw new DoesNotExistException("Product does not exist.");
        }
    }

    @Override
    public List<String> getProducts() {
        List<String> prods_list = new ArrayList<>(prods.keySet());
        return prods_list;
    }

}
