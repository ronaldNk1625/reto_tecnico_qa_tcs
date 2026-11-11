package com.demoblaze.automation.util;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.InputStream;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public final class JsonReader {

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private JsonReader() {
    }

    public static JsonNode getTestCaseById(String filePath, String testCaseId) {
        try (InputStream is = JsonReader.class.getClassLoader().getResourceAsStream(filePath)) {
            if (is == null) {
                throw new IllegalArgumentException("No se encontro el archivo JSON en resources: " + filePath);
            }
            JsonNode rootNode = MAPPER.readTree(is);
            if (rootNode.isArray()) {
                for (JsonNode node : rootNode) {
                    if (node.has("id") && testCaseId.equalsIgnoreCase(node.get("id").asText())) {
                        return node;
                    }
                }
            } else if (rootNode.has(testCaseId)) {
                return rootNode.get(testCaseId);
            }
            throw new IllegalArgumentException("No se encontro el caso de prueba con ID: " + testCaseId + " en " + filePath);
        } catch (Exception e) {
            throw new RuntimeException("Error leyendo el archivo JSON: " + filePath, e);
        }
    }

    public static Map<String, Object> getTestCaseAsMap(String filePath, String testCaseId) {
        JsonNode node = getTestCaseById(filePath, testCaseId);
        return MAPPER.convertValue(node, new TypeReference<Map<String, Object>>() {});
    }
}

