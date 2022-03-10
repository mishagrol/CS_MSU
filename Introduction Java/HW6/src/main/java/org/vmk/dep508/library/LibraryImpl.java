package org.vmk.dep508.library;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class LibraryImpl implements Library{

    private String jdbcUrl;
    private String user;
    private String password;

    public LibraryImpl(String jdbcUrl, String user, String password) {
        this.jdbcUrl = jdbcUrl;
        this.user = user;
        this.password = password;
    }

    Connection getConnection() throws SQLException {
        return DriverManager.getConnection(jdbcUrl, user, password);
    }

    @Override
    public void addNewBook(Book book) {
        String addBookSql = "insert into books (book_id, book_title, abonent_id) values(?, ?, NULL)";
        try (PreparedStatement stmp = getConnection().prepareStatement(addBookSql)){
            stmp.setInt(1, book.getId());
            stmp.setString(2, book.getTitle());
            stmp.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void addAbonent(Student student) {
        String addAbonentSql = "insert into abonents (abonent_id, abonent_name) values(?, ?)";
        try (PreparedStatement stmp = getConnection().prepareStatement(addAbonentSql)){
            stmp.setInt(1, student.getId());
            stmp.setString(2, student.getName());
            stmp.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void borrowBook(Book book, Student student) {
        String borrowBookSql = "update books set abonent_id = ? where book_id = ? and book_title = ?";
        try (PreparedStatement stmp = getConnection().prepareStatement(borrowBookSql)){
            stmp.setInt(1, student.getId());
            stmp.setInt(2, book.getId());
            stmp.setString(3, book.getTitle());
            stmp.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void returnBook(Book book, Student student) {
        String borrowBookSql = "update books set abonent_id = NULL where book_id = ? and book_title = ?";
        try (PreparedStatement stmp = getConnection().prepareStatement(borrowBookSql)){
            stmp.setInt(1, book.getId());
            stmp.setString(2, book.getTitle());
            stmp.execute();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    @Override
    public List<Book> findAvailableBooks() {
        List<Book> result = new ArrayList<>();
        String selectBooksSql = "select book_id, book_title from books where abonent_id is NULL";
        try (Statement stmt = getConnection().createStatement();
             ResultSet rs = stmt.executeQuery(selectBooksSql);) {
            while (rs.next()) {
                Integer book_id = rs.getInt("book_id");
                String book_title = rs.getString("book_title");
                result.add(new Book(book_id, book_title));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public List<Student> getAllStudents() {
        List<Student> result = new ArrayList<>();
        String selectAbonentsSql = "select abonent_id, abonent_name from abonents";
        try (Statement stmt = getConnection().createStatement();
             ResultSet rs = stmt.executeQuery(selectAbonentsSql);) {
            while (rs.next()) {
                Integer abonent_id = rs.getInt("abonent_id");
                String abonent_name = rs.getString("abonent_name");
                result.add(new Student(abonent_id, abonent_name));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return result;
    }
}
