# Test Java Application

Simple Java application for testing the CLI Executor Agent.

## Structure

```
test-java-app/
├── src/
│   └── UserService.java    # Sample Java service class
└── README.md               # This file
```

## UserService.java

A simple user management service with the following methods:
- `addUser(String username)` - Add a new user
- `deleteUser(String username)` - Delete a user
- `getAllUsers()` - Get all users
- `getUserByIndex(int index)` - Get user by index
- `getUserCount()` - Get total user count
- `clearAllUsers()` - Clear all users

## Purpose

This code is intentionally WITHOUT logging statements so that the CLI Executor Agent can add them using the custom logging agent.

## Testing with CLI Executor Agent

Use this repository to test the CLI Executor Agent's ability to:
1. Read Java code
2. Select appropriate custom agent (logging-agent)
3. Execute Claude CLI or Copilot CLI
4. Add comprehensive logging to all methods
5. Commit and push changes to a new branch
