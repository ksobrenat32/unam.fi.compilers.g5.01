int hello() {
    print("Hello!\n");
    return 0;
}

int main(){
    int i = 0;
    while (i < 10) {
        hello();
        if (i == 5) {
            print("Halfway there!\n");
        } else {
            print(i);
        }
        i = i + 1;
    }
    print("Goodbye!\n");
    return 0;
}