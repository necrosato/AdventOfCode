#include <map>
#include <chrono>
#include <iostream>
#include <fstream>

static std::map<char, int> shapes = { { 'A', 1 }, {'B', 2}, {'C', 3}, {'X', 1}, {'Y', 2}, {'Z', 3} };

int play( int p1, int p2 ) {
    if ( p1 == p2 ) { return p2 + 3; }
    if ( (p1%3)+1 == p2 ) { return p2 + 6; }
    return p2;
}
int play2( int p1, char outcome ) {
    if (outcome == 'Y') { return p1 + 3; }
    if (outcome == 'Z') { return (p1%3)+1 + 6; }
    return p1 == 1 ? 3 : p1-1;
}
int main( int argc, char** argv )
{
    FILE* fp = fopen("input2.txt", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    int score = 0;
    int score2 = 0;
    auto start = std::chrono::system_clock::now();

    char* line = NULL;
    size_t len = 0;
    while ((getline(&line, &len, fp)) != -1) {
        score += play(shapes[line[0]], shapes[line[2]]);
        score2 += play2(shapes[line[0]], line[2]);
    }
    fclose(fp);
    if (line)
        free(line);

    auto end = std::chrono::system_clock::now();
    std::cout << "part1: " << score << " part2: " << score2 << " took " << std::chrono::microseconds(end-start).count() << " microseconds" << std::endl;
    return 0;
}
