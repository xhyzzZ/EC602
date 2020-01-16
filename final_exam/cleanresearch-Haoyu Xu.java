// Copyright 2019 Haoyu Xu xhy@bu.edu
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

class Pair {
    int date;
    double dose;
    int id;
    public Pair(int date, double dose, int id) {
        this.date = date;
        this.dose = dose;
        this.id = id;
    }
}
public class two {
    public static void main(String[] args) throws IOException {
        String inputFileName = args[1];
        String outputFileName = args[2];
        List<String> records = readFile(inputFileName);
        List<String> data = cleanData(records);
        createAndWrite(data, outputFileName);
    }

    public static List<String> cleanData(List<String> records) {
        List<Pair> data = new ArrayList<>();
        for (String record : records) {
            String[] parts = record.split(" ");
            for (String part : parts) {
                // date
                StringBuilder numberDate = new StringBuilder();
                int id = 0;
                double dose = 0;
                if (part.indexOf('/') != -1) {
                    String[] date = part.split("/");
                    for (String val : date) {
                        numberDate.append(val);
                    }
                } else if (part.indexOf('.') != -1) {
                    // dose
                    dose = Double.parseDouble(part);
                } else {
                    // id
                    id = Integer.parseInt(part);
                }
                data.add(new Pair(Integer.parseInt(numberDate.toString()), dose, id));
            }
        }

        PriorityQueue<Pair> queue = new PriorityQueue<>(new Comparator<Pair>() {
            @Override
            public int compare(Pair o1, Pair o2) {
                if (o1.date != o2.date) {
                    return o1.date - o2.date;
                } else {
                    if (o1.id != o2.id) {
                        return o1.id - o2.id;
                    } else {
                        return 0;
                    }
                }
            }
        });
        queue.addAll(data);
        List<String> res = new ArrayList<>();
        for (Pair x : queue) {
            StringBuilder sb = new StringBuilder();
            String val = String.valueOf(x.date);
            int interval = 0;
            for (int i = 0; i < val.length(); i++) {
                interval++;
                sb.append(i);
                if (interval % 2 == 1) {
                    sb.append("/");
                }
            }
            double dose = x.dose;
            int id = x.id;
            String s = "";
            s += sb.toString() + " " + id + " " + dose;
            res.add(s);
        }
        return res;
    }


    private static List<String> readFile(String filename) {
        List<String> records = new ArrayList<>();
        try {
            BufferedReader reader = new BufferedReader(new FileReader(filename));
            String line;
            while ((line = reader.readLine()) != null) {
                records.add(line);
            }
            reader.close();
            return records;
        } catch (Exception e) {
            System.err.format("Exception occurred trying to read '%s'.", filename);
            e.printStackTrace();
            return null;
        }
    }

    private static void createAndWrite(List<String> data, String fileName) throws IOException {
        PrintWriter writer = new PrintWriter(fileName, StandardCharsets.UTF_8);
        for (String val : data) {
            writer.println(val);
        }
        writer.close();
    }
}
