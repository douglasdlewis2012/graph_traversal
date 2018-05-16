package com.douglaslewis;

import java.io.File;
import java.util.*;


public class AStar {
    private final String HOLDER = "_";

    private class Node implements Comparable<Node> {
        private int f;
        private int g;
        private String word;
        private Node previous;

        public Node(int f, int g, String word, Node previous) {
            this.f = f;
            this.g = g;
            this.word = word;
            this.previous = previous;
        }

        public void printNode() {
            StringBuilder builder = new StringBuilder();
            builder.append("f: ");
            builder.append(this.f);
            builder.append(" g: ");
            builder.append(this.g);
            builder.append(" word: ");
            builder.append(this.word);
            builder.append(" previous: ");
            builder.append(this.previous);
            System.out.println(builder.toString());
        }

        public int getF() {
            return f;
        }

        public int getG() {
            return g;
        }

        public String getWord() {
            return word;
        }

        public Node getPrevious() {
            return previous;
        }

        @Override
        public int compareTo(Node o) {
            String otherWord = ((Node) o).word;
            return this.word.compareTo(otherWord);
        }


    }


    public AStar() {
    }

    private int heuristic(String word, String end) {

        int sum = 0;
        char[] wordsArray = word.toCharArray();
        char[] endArray = end.toCharArray();

        for (int i = 0; i < word.length(); i++) {
            if (wordsArray[i] != endArray[i])
                sum++;
        }
        return sum;
    }


    private List<String> getWords(int size) {
        List<String> allWords = new ArrayList<String>();
        List<String> sizedWords = new ArrayList<String>();

        try {
            Scanner s = new Scanner(new File("words.txt"));

            while (s.hasNext()) {
                allWords.add(s.next().trim());
            }

            s.close();
        } catch (Exception e) {
            e.printStackTrace();
        }



        for (String word : allWords) {
            if (word.length() == size) {
                    sizedWords.add(word.toLowerCase());
            }
        }

        return sizedWords;
    }


    private Map<String, List<List<String>>> generateNeighbors(List<String> words) {
        Map<String, List<List<String>>> neighborhoods = new HashMap<>();
        Map<String, List<String>> match = new HashMap<>();

        for (String w : words) {
            List<List<String>> neihborhood = new ArrayList<>();
            for (int i = 0; i < w.length(); i++) {

                String p = getPattern(w,i);

                List<String> m = match.get(p);

                if (m == null) {
                    match.put(p, new ArrayList<>());
                    m = match.get(p);
                }

                m.add(w);
                neihborhood.add(m);
                neighborhoods.put(w, neihborhood);

            }
        }

        return neighborhoods;
    }

    private String getPattern(String w, int i ){
        String p = new String();

        for (int j = 0; j < w.length(); j++) {
            if (i == j) {
                p += HOLDER;
            } else {
                p += w.substring(j, j + 1);
            }
        }

        return p;

    }

    private String reconstructPath(Node node) {
        List<String> path = new ArrayList<String>();

        path.add(node.getWord());
        while (node.previous != null) {
            Node temp = node.previous;
            node = node.previous;
            path.add(temp.word);
        }

        Collections.reverse(path);


        StringBuilder pathString = new StringBuilder();
        for (String n : path) {
            pathString.append(n + " ");

        }

        return pathString.toString();
    }

    public String aStarSearch(String start, String end, List<String> words) {
        Map<String, List<List<String>>> neighbors = generateNeighbors(words);
        Set<String> openSet = new HashSet<>();
        openSet.add(start);

        Set<String> closedSet = new HashSet<>();
        PriorityQueue<Node> heap = new PriorityQueue<>();
        heap.add(new Node(heuristic(start, end), 0, start, null));


        while (!heap.isEmpty()) {
            Node node = heap.remove();
            if (node.getWord().equals(end)) {
                return reconstructPath(node);
            }

            openSet.remove(node.getWord());
            closedSet.add(node.getWord());

            int g = node.getG() + 1;
            List<List<String>> neighborhood = neighbors.get(node.getWord());
            for (List<String> localNeighbors : neighborhood) {
                for (String word : localNeighbors) {
                    if ((!closedSet.contains(word)) && (!openSet.contains(word))) {
                        Node newNode = new Node(heuristic(word, end) + g, g, word, node);
                        heap.add(newNode);
                        openSet.add(word);
                    }

                }

            }

        }

        return "No way found! between " + start + " - " + end;
    }

    public void runTests() {

    }

    public void test(String start, String end) {


        int size = 5;
        long startTime = System.nanoTime();
        List<String> words = getWords(size);
        System.out.println(aStarSearch(start, end, words));
        long endTime = System.nanoTime();
        System.out.println("Total time: " + (endTime - startTime) / 1.0e9);
        System.out.println("========================================");

    }
}
