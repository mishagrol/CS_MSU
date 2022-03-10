package org.vmk.dep508.collections.basket;

import org.junit.*;

import static org.junit.Assert.*;

public class BasketImplTest {

    Basket basket;
    String one = "Product One";
    String two = "Product Two";
    String three = "Product Three";

    /*Вызыватется при инициализации класса BasketImplTest*/
    @BeforeClass
    public static void setupClass(){

    }

    /*Вызыватется перед вызовом каждого метода помеченного аннотацией @Test*/
    @Before
    public void setup(){
        basket = new BasketImpl();
    }

    /*Вызыватется после вызова каждого метода помеченного аннотацией @Test*/
    @After
    public void clear() {
        basket = null;
    }

    /*Вызывается после вызова всех тестовых методов*/
    @AfterClass
    public static void releaseRecources() {

    }

    @Test
    public void addProduct() throws DoesNotExistException {
        assertEquals(0, basket.getProducts().size());

        basket.addProduct(one, 1);
        basket.addProduct(two, 5);
        assertEquals(2, basket.getProducts().size());

        basket.addProduct(one, 1);
        assertEquals(2, basket.getQuantity(one));
        assertEquals(2, basket.getProducts().size());
    }

    @Test
    public void removeProduct() throws DoesNotExistException {
        basket.addProduct(one, 1);
        basket.addProduct(two, 5);
        basket.removeProduct(one);

        assertThrows(DoesNotExistException.class, () -> basket.removeProduct(three));
        assertEquals(1, basket.getProducts().size());
    }


    @Test
    public void updateProductQuantity() throws DoesNotExistException {
        basket.addProduct(one, 1);
        basket.updateProductQuantity(one, 2);

        assertEquals(3, basket.getQuantity(one));
        assertThrows(DoesNotExistException.class, () -> basket.updateProductQuantity(three, 2));
    }

    @Test
    public void getProducts() throws DoesNotExistException {
        assertEquals(0, basket.getProducts().size());

        basket.addProduct(one, 1);
        basket.addProduct(two, 5);

        assertTrue(basket.getProducts().contains(one));
        assertTrue(basket.getProducts().contains(two));
        assertEquals(2, basket.getProducts().size());

        basket.removeProduct(two);
        assertEquals(1, basket.getProducts().size());
    }
}