// Read zipped csv file and manipulate dataframe

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <zip.h> // For reading zip files
#include <string>

/*
int replaceString() {
    // Assuming the input string and substring are provided
    std::string input_string = "Hello, this is a sample string. Replace 'sample' with 'new'.";

    // Define the substring to be replaced
    std::string substring_to_replace = "sample";

    // Define the replacement string
    std::string replacement_string = "new";

    // Use the find() method to locate the substring
    size_t pos = input_string.find(substring_to_replace);

    // If the substring is found, replace it
    if (pos != std::string::npos) {
        input_string.replace(pos, substring_to_replace.length(), replacement_string);
    }

    // Print the result
    std::cout << input_string << std::endl;

    return 0;
}
*/
int main() {
  const char* zipFilePath = "../Data/leash-BELKA.zip";
  const char* csvFileName = "train.csv";

  // Open the zip file
  struct zip* archive = zip_open(zipFilePath, 0, NULL);
  if (!archive) {
    std::cerr << "Error opening zip file." << std::endl;
    return 1;
  }

  // Locate the CSV file in the zip archive
  struct zip_stat st;
  zip_stat_init(&st);
  zip_stat(archive, csvFileName, 0, &st);

  // Read the CSV file
  char* buffer = new char[st.size];
  struct zip_file* file = zip_fopen(archive, csvFileName, 0);
  zip_fread(file, buffer, st.size);
  zip_fclose(file);

  // Process the CSV data (e.g., parse it into rows and columns)
  std::istringstream csvStream(buffer);
  std::string line;
  int j = 0;
  while (std::getline(csvStream, line) && (j < 10)) {
    // Process each line of the CSV
    // ...
    std::cout << line << endl;
    j += 1;
  }

  // Clean up
  delete[] buffer;
  zip_close(archive);

  return 0;
}