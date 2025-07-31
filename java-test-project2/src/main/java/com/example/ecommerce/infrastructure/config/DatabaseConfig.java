package com.example.ecommerce.infrastructure.config;

import com.example.ecommerce.util.StringUtils;

public class DatabaseConfig {
    private String host;
    private int port;
    private String database;
    private String username;
    private String password;
    
    public DatabaseConfig() {
        this.host = "localhost";
        this.port = 5432;
        this.database = "ecommerce2";
    }
    
    public String getConnectionString() {
        if (StringUtils.isEmpty(host) || StringUtils.isEmpty(database)) {
            throw new IllegalStateException("Database configuration is incomplete");
        }
        return String.format("jdbc:postgresql://%s:%d/%s", host, port, database);
    }
    
    public String getHost() { return host; }
    public void setHost(String host) { this.host = host; }
    
    public int getPort() { return port; }
    public void setPort(int port) { this.port = port; }
    
    public String getDatabase() { return database; }
    public void setDatabase(String database) { this.database = database; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
