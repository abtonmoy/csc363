int bar(int r, int s)
{
    int i;
    i = 20 + (r + s);
    return i;
}
int foo1(int a, int b)
{
    int g;
    g = bar(b, a);
}
int foo2(int a, int b);
{
    int h;
    h = bar(a, b);
    return h;
}
int main()
{
    int x;
    int y;
    int z;
    x = 6;
    y = 7;
    z = foo1(x,y) + foo2(x,y);
}