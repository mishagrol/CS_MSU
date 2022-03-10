package org.vmk.dep508.sites;

import java.util.Map;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.*;

public class Main {

    public static void main(String[] args) {
        Pages pages = new Pages();
        pages.addPage("a");
        pages.addPage("b");
        pages.addPage("c");
        pages.addPage("d");
        pages.addPage("e");

        String[] available_pages = {"a", "b", "c", "d", "e"};
        Random random = new Random();

        ExecutorService service = null;
        try {
            service = Executors.newFixedThreadPool(50);
            for (int j = 0; j < 10; j++) {
                for (int i = 0; i < 50; i++) {
                    int random_page = random.nextInt(available_pages.length);
                    pages.updateQuantity(available_pages[random_page]);
                }
            }
        } finally {
            if (null != service) service.shutdown();
        }

        synchronized (pages) {
            pages.notifyAll();
        }

        System.out.println(pages.getPages());
    }

}


class Pages {
    private Map<String, Integer> pages = new HashMap<>();

    public void addPage(String page_name){
        pages.put(page_name, 0);
    }

    public synchronized void updateQuantity(String page_name){
        int cur_qnt = pages.get(page_name);
        pages.put(page_name, cur_qnt + 1);
    }

    public Map<String, Integer> getPages(){
        return pages;
    }

}
