package com.intelligester;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import java.net.HttpURLConnection;
import java.net.InetSocketAddress;

import java.util.concurrent.Executors;

public class IntelligesterEegPoll implements HttpHandler {
    private HttpServer httpServer;
    private HttpContext context;

    private IntelligesterEegPoll() throws IOException {
        InetSocketAddress address = new InetSocketAddress("0.0.0.0", 8080);
        this.httpServer = HttpServer.create(address, 0);
        this.httpServer.setExecutor(Executors.newFixedThreadPool(8));
        this.context = this.httpServer.createContext("/neural", this);
    }

    public final void handle(HttpExchange exchange) throws IOException {
        // Request method
        String requestMethod = exchange.getRequestMethod();
        if (requestMethod.equalsIgnoreCase("get")) {
            System.out.println("GET requested");
        } else if (requestMethod.equalsIgnoreCase("post")) {
            System.out.println("POST requested");
        }

        // Set the response headers
        Headers responseHeaders = exchange.getResponseHeaders();
        responseHeaders.set("Content-Type", "application/json");

        // Response is OK (HTTP 200)
        exchange.sendResponseHeaders(HttpURLConnection.HTTP_OK, 0);

        // Set up the input and output streams
        BufferedReader reader = new BufferedReader(new InputStreamReader(exchange.getRequestBody()));
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(exchange.getResponseBody()));

        // Read the input, and have the implementing child handle the output
        String messageString = reader.readLine();

        String remoteHostAddress = exchange.getRemoteAddress().getAddress().getHostAddress();
        this.handleExchange(remoteHostAddress, messageString, writer);
        writer.flush();
        exchange.close();
    }

    private final void handleExchange(String remoteHostAddress, String messageString, BufferedWriter responseWriter) {
        try {
            responseWriter.write("{\"api version\": \"EXCELTHIOR\", \"play again?");
        } catch (IOException ex) {
            System.err.println("Failed to respond to remote request.");
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        try {
            IntelligesterEegPoll server = new IntelligesterEegPoll();
            server.httpServer.start();
            EmotivWrapper.connect();
            EmotivWrapper.pollForever();
        } catch (IOException ex) {
            System.err.println("Failed to startup HTTP server: exiting!");
            System.exit(1);
        }

    }
}
