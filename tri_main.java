public class tri_main {
    public static void main(String[] args) {
        triangle t1 = new triangle(1,1,1);
        triangle t2 = new triangle(1,10,12);

        System.out.println(t1.is_valid()); // true
        System.out.println(t2.is_valid()); // false
        System.out.println(t1.get_perimeter()); // 3
    }
}