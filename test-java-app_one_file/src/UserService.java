package com.example.service;

import java.util.ArrayList;
import java.util.List;

public class UserService {
    
    private List<String> users = new ArrayList<>();
    
    public void addUser(String username) {
        if (username == null || username.isEmpty()) {
            throw new IllegalArgumentException("Username cannot be null or empty");
        }
        users.add(username);
    }
    
    public boolean deleteUser(String username) {
        return users.remove(username);
    }
    
    public List<String> getAllUsers() {
        return new ArrayList<>(users);
    }
    
    public String getUserByIndex(int index) {
        if (index < 0 || index >= users.size()) {
            throw new IndexOutOfBoundsException("Invalid user index: " + index);
        }
        return users.get(index);
    }
    
    public int getUserCount() {
        return users.size();
    }
    
    public void clearAllUsers() {
        users.clear();
    }
}
