package org.vmk.dep508.library;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.sql.*;

import static org.junit.Assert.*;

public class LibraryTest {
    LibraryImpl lib = new LibraryImpl("jdbc:h2:mem:library", "", "");

    @Before
    public void setUp() throws Exception {
        Connection connection = lib.getConnection();
        try (Statement stmp = connection.createStatement()) {
            String createTableSql = "" +
                    "CREATE TABLE ABONENTS(" +
                    "    abonent_id int primary key," +
                    "    abonent_name varchar(255)" +
                    ");" +

                    "CREATE TABLE BOOKS(" +
                    "    book_id int primary key," +
                    "    book_title varchar(255)," +
                    "    abonent_id int," +
                    "    foreign key(abonent_id) references ABONENTS(abonent_id)" +
                    ");";
            stmp.execute(createTableSql);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @After
    public void tearDown() throws Exception {
        Connection connection = lib.getConnection();
        try (Statement stmp = connection.createStatement()) {
            stmp.execute("DROP TABLE books");
            stmp.execute("DROP TABLE abonents");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Test
    public void addNewBook() throws Exception {
        lib.addNewBook(new Book(1, "Harry Potter and the Sorcerer's Stone"));
        lib.addNewBook(new Book(2, "Harry Potter and the Chamber of Secrets"));
        lib.addNewBook(new Book(3, "Harry Potter and the Prisoner of Azkaban"));

        assertEquals(3, lib.findAvailableBooks().size());
//        System.out.println(lib.findAvailableBooks());
    }

    @Test
    public void addAbonent() throws Exception {
        lib.addAbonent(new Student(1, "Harry"));
        lib.addAbonent(new Student(2, "Ron"));
        lib.addAbonent(new Student(3, "Hermione"));

        assertEquals(3, lib.getAllStudents().size());
//        System.out.println(lib.getAllStudents());
    }

    @Test
    public void borrowBook() throws Exception {
        lib.addNewBook(new Book(1, "Harry Potter and the Sorcerer's Stone"));
        lib.addNewBook(new Book(2, "Harry Potter and the Chamber of Secrets"));
        lib.addAbonent(new Student(1, "Harry"));
        lib.addAbonent(new Student(2, "Ron"));

        assertEquals(2, lib.findAvailableBooks().size());

        lib.borrowBook(new Book(1, "Harry Potter and the Sorcerer's Stone"),
                new Student(1, "Harry"));
        assertEquals(1, lib.findAvailableBooks().size());
//        System.out.println(lib.findAvailableBooks());
    }

    @Test
    public void returnBook() throws Exception {
        lib.addNewBook(new Book(1, "Harry Potter and the Sorcerer's Stone"));
        lib.addNewBook(new Book(2, "Harry Potter and the Chamber of Secrets"));
        lib.addAbonent(new Student(1, "Harry"));
        lib.addAbonent(new Student(2, "Ron"));

        assertEquals(2, lib.findAvailableBooks().size());

        lib.borrowBook(new Book(1, "Harry Potter and the Sorcerer's Stone"),
                new Student(1, "Harry"));
        assertEquals(1, lib.findAvailableBooks().size());

        lib.returnBook(new Book(1, "Harry Potter and the Sorcerer's Stone"),
                new Student(1, "Harry"));
        assertEquals(2, lib.findAvailableBooks().size());
//        System.out.println(lib.findAvailableBooks());
    }

    @Test
    public void findAvailableBooks() throws Exception {
        lib.addNewBook(new Book(1, "Harry Potter and the Sorcerer's Stone"));
        lib.addNewBook(new Book(2, "Harry Potter and the Chamber of Secrets"));
        lib.addNewBook(new Book(3, "Harry Potter and the Prisoner of Azkaban"));

        assertEquals(3, lib.findAvailableBooks().size());
//        System.out.println(lib.findAvailableBooks());
    }

    @Test
    public void getAllStudents() throws Exception {
        lib.addAbonent(new Student(1, "Harry"));
        lib.addAbonent(new Student(2, "Ron"));
        lib.addAbonent(new Student(3, "Hermione"));

        assertEquals(3, lib.getAllStudents().size());
//        System.out.println(lib.getAllStudents());
    }

}
