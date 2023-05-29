

#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::string filename = "AI_text_file.txt";

    std::ifstream inputFile(filename);

    if (!inputFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(inputFile, line)) {
        std::cout << line << std::endl;
    }

    inputFile.close();

    return 0;
}

