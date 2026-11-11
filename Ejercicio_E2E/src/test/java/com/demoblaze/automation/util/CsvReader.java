package com.demoblaze.automation.util;

import com.opencsv.CSVReader;
import com.opencsv.CSVReaderHeaderAware;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public final class CsvReader {

    private CsvReader() {
    }

    public static Map<String, String> getTestCaseById(String filePath, String testCaseId) {
        try (InputStream is = CsvReader.class.getClassLoader().getResourceAsStream(filePath)) {
            if (is == null) {
                throw new IllegalArgumentException("No se encontro el archivo CSV en resources: " + filePath);
            }
            try (CSVReaderHeaderAware reader = new CSVReaderHeaderAware(new InputStreamReader(is, StandardCharsets.UTF_8))) {
                Map<String, String> row;
                while ((row = reader.readMap()) != null) {
                    if (testCaseId.equalsIgnoreCase(row.get("id"))) {
                        return new HashMap<>(row);
                    }
                }
            }
            throw new IllegalArgumentException("No se encontro el registro con id " + testCaseId + " en " + filePath);
        } catch (Exception e) {
            throw new RuntimeException("Error leyendo archivo CSV: " + filePath, e);
        }
    }
}

