#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

using namespace std;
using std::filesystem::directory_iterator;

string get_file_num_by_regex(string file_name, string regex) {
    string result = "";
    int pos = file_name.find(regex);
    if (pos != string::npos) {
        result = file_name.substr(0, pos);
    }
    return result;
}

void append_file_to_file(string file_name, string file_name_to_append) {
    ifstream file_to_append(file_name_to_append);
    ofstream file_to_write(file_name, ios::app);
    string line;
    while (getline(file_to_append, line)) {
        file_to_write << line << endl;
    }
    file_to_append.close();
    file_to_write.close();
}

void remove_file(string file_name) {
    if (remove(file_name.c_str()) != 0) {
        cout << "Error deleting file" << endl;
    }
}

void append_file_to_file_in_binary(string file_name, string file_name_to_append) {
    ifstream file_to_append(file_name_to_append, ios::binary);
    ofstream file_to_write(file_name, ios::app | ios::binary);
    if (file_to_append.is_open()) {
        cout << "open file_to_append success!" << endl;
    }
    if (file_to_write.is_open()) {
        cout << "open file_to_write success!" << endl;
    }
    file_to_append.seekg(0, file_to_append.end);
    int length = file_to_append.tellg();
    file_to_append.seekg(0, file_to_append.beg);
    if (length == 0 ) return;
    char buffer[length];
    while (file_to_append.read(buffer, length))
    {
        file_to_write.write(buffer, length);
    }
    file_to_append.close();
    file_to_write.close();
}



int main(int argc, char const *argv[])
{
    if (argc < 3) {
        cout << "Usage: merge_opus_files_2_1 <opus_file_dir> <opus_file_out_dir>" << endl;
        return 0;
    }

    // opus_61_202110271832159323674C65A85197D3.opus
    int max_num = 0;
    string in_dir = argv[1];
    string out_dir = argv[2];
    string out_file_path = out_dir + "/pcm_merged.pcm";
    cout << "out_file_path: " << out_file_path << endl;
    remove_file(out_file_path);

    directory_iterator end_itr;
    for (directory_iterator itr(argv[1]); itr != end_itr; ++itr) {
        if (is_regular_file(itr->status())) {
            string file_name = itr->path().filename().string();
            string file_num = get_file_num_by_regex(file_name, ".pcm");
            cout<<"skx:"<<file_num<<endl;
            int num  = stoi(file_num);
            if (num > max_num) {
                max_num = num;
            }
        }
    }

    for (int i = 1; i <= max_num; ++i) {
        string file_name = to_string(i) + ".pcm";
        cout << file_name << endl;
        append_file_to_file_in_binary(out_file_path, in_dir + "/" + file_name);
    }
    return 0;
}
