package org.vmk.dep508.stream.iris;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.stream.Collectors;


public class App {
    public static void main(String[] args) throws IOException {
        App a = new App();
        a.test();
    }

    public void test() throws IOException {

        //load data from file iris.data
        List<Iris> irisList = Files.lines(Paths.get("iris.data")).map(Iris::parse).collect(Collectors.toList());
        IrisDataSetHelper helper = new IrisDataSetHelper(irisList);

        //get average sepal width
        Double avgSetalLength = helper.getAverage(Iris::getSepalLength);
        System.out.println(avgSetalLength);

        //get average petal square - petal width multiplied on petal length
        Double avgPetalSquare = helper.getAverage(t -> t.getPetalLength() * t.getPetalWidth());
        System.out.println(avgPetalSquare);

        //get average petal square for flowers with sepal width > 4
        Double avgPetalSquareWithFilter = helper.getAverageWithFilter(t -> t.getSepalLength() > 4,
                                                                      t -> t.getPetalLength() * t.getPetalWidth());
        System.out.println(avgPetalSquareWithFilter);

        //get flowers grouped by Petal size (Petal.SMALL, etc.)
        Map groupsByPetalSize = helper.groupBy(t -> Iris.classifyByPatel((Iris) t));
        System.out.println(groupsByPetalSize);

        //get max sepal width for flowers grouped by species
        Map maxSepalWidthForGroupsBySpecies = helper.maxFromGroupedBy(Iris::getSpecies, Iris::getSepalWidth);
        System.out.println(maxSepalWidthForGroupsBySpecies);
    }

}

