import java.util.*;

public class triangle {
    private int[] sides;

    public triangle(int a, int b, int c) {
        sides = new int[]{a ,b, c};
    }

    public boolean is_valid() {
        return (sides[0] + sides[1] > sides[2] &&
                sides[0] + sides[2] > sides[1] &&
                sides[1] + sides[2] > sides[0]);
    }

    public int get_perimeter() {
        return sides[0] + sides[1] + sides[2];
    }
}