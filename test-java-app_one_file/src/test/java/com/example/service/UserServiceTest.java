package com.example.service;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    @Test
    void addUser_addsValidUser_andIncrementsCount() {
        UserService service = new UserService();

        assertEquals(0, service.getUserCount());
        service.addUser("alice");
        assertEquals(1, service.getUserCount());
        assertEquals(List.of("alice"), service.getAllUsers());
    }

    @Test
    void addUser_allowsWhitespaceStringBecauseOnlyEmptyIsRejected() {
        UserService service = new UserService();

        service.addUser(" ");
        assertEquals(1, service.getUserCount());
        assertEquals(" ", service.getUserByIndex(0));
    }

    @Test
    void addUser_allowsDuplicates() {
        UserService service = new UserService();

        service.addUser("alice");
        service.addUser("alice");

        assertEquals(2, service.getUserCount());
        assertEquals(List.of("alice", "alice"), service.getAllUsers());
    }

    @Test
    void addUser_throwsForNull() {
        UserService service = new UserService();

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.addUser(null));
        assertEquals("Username cannot be null or empty", ex.getMessage());
        assertEquals(0, service.getUserCount());
    }

    @Test
    void addUser_throwsForEmptyString() {
        UserService service = new UserService();

        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> service.addUser(""));
        assertEquals("Username cannot be null or empty", ex.getMessage());
        assertEquals(0, service.getUserCount());
    }

    @Test
    void deleteUser_returnsTrueAndRemovesWhenUserExists() {
        UserService service = new UserService();
        service.addUser("alice");
        service.addUser("bob");

        assertTrue(service.deleteUser("alice"));
        assertEquals(1, service.getUserCount());
        assertEquals(List.of("bob"), service.getAllUsers());
    }

    @Test
    void deleteUser_returnsFalseWhenUserDoesNotExist() {
        UserService service = new UserService();
        service.addUser("alice");

        assertFalse(service.deleteUser("missing"));
        assertEquals(1, service.getUserCount());
        assertEquals(List.of("alice"), service.getAllUsers());
    }

    @Test
    void deleteUser_returnsFalseForNullBecauseNullCannotBeAdded() {
        UserService service = new UserService();
        service.addUser("alice");

        assertFalse(service.deleteUser(null));
        assertEquals(1, service.getUserCount());
        assertEquals(List.of("alice"), service.getAllUsers());
    }

    @Test
    void deleteUser_removesOnlyFirstMatchingDuplicate() {
        UserService service = new UserService();
        service.addUser("alice");
        service.addUser("bob");
        service.addUser("alice");

        assertTrue(service.deleteUser("alice"));

        assertEquals(2, service.getUserCount());
        assertEquals(List.of("bob", "alice"), service.getAllUsers());
    }

    @Test
    void getAllUsers_returnsCopy_modifyingReturnedListDoesNotAffectInternalState() {
        UserService service = new UserService();
        service.addUser("alice");
        service.addUser("bob");

        List<String> snapshot = service.getAllUsers();
        snapshot.add("mallory");
        snapshot.remove("alice");

        // Internal list must remain unchanged
        assertEquals(2, service.getUserCount());
        assertEquals(List.of("alice", "bob"), service.getAllUsers());
    }

    @Test
    void getUserByIndex_returnsCorrectUser_forValidIndices() {
        UserService service = new UserService();
        service.addUser("alice");
        service.addUser("bob");

        assertEquals("alice", service.getUserByIndex(0));
        assertEquals("bob", service.getUserByIndex(1));
    }

    @Test
    void getUserByIndex_throwsForNegativeIndex() {
        UserService service = new UserService();
        service.addUser("alice");

        IndexOutOfBoundsException ex = assertThrows(IndexOutOfBoundsException.class, () -> service.getUserByIndex(-1));
        assertEquals("Invalid user index: -1", ex.getMessage());
    }

    @Test
    void getUserByIndex_throwsForIndexEqualToSize() {
        UserService service = new UserService();
        service.addUser("alice");

        IndexOutOfBoundsException ex = assertThrows(IndexOutOfBoundsException.class, () -> service.getUserByIndex(1));
        assertEquals("Invalid user index: 1", ex.getMessage());
    }

    @Test
    void getUserByIndex_throwsWhenListEmptyAndIndexZero() {
        UserService service = new UserService();

        IndexOutOfBoundsException ex = assertThrows(IndexOutOfBoundsException.class, () -> service.getUserByIndex(0));
        assertEquals("Invalid user index: 0", ex.getMessage());
    }

    @Test
    void getUserCount_tracksAddsDeletesAndClear() {
        UserService service = new UserService();

        assertEquals(0, service.getUserCount());

        service.addUser("alice");
        service.addUser("bob");
        assertEquals(2, service.getUserCount());

        assertTrue(service.deleteUser("alice"));
        assertEquals(1, service.getUserCount());

        service.clearAllUsers();
        assertEquals(0, service.getUserCount());
        assertTrue(service.getAllUsers().isEmpty());
    }

    @Test
    void clearAllUsers_isIdempotent() {
        UserService service = new UserService();

        service.clearAllUsers();
        service.clearAllUsers();

        assertEquals(0, service.getUserCount());
        assertTrue(service.getAllUsers().isEmpty());
    }

    @Test
    void clearAllUsers_allowsUsersToBeAddedAgain() {
        UserService service = new UserService();
        service.addUser("alice");

        service.clearAllUsers();
        service.addUser("bob");

        assertEquals(1, service.getUserCount());
        assertEquals(List.of("bob"), service.getAllUsers());
    }
}
