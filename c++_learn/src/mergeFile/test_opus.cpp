#include <iostream>
#include <fstream>
#include <string>
#include "myopus.h"
#include <filesystem>


#define ENCODE_PACK_SIZE    800

using namespace std;
using std::filesystem::directory_iterator;

opus_state_dec *decoder = NULL;

void convert_opus_to_pcm(string opus_file, string pcm_file)
{
	fstream infile(opus_file, ios::in | ios::binary | ios::ate);
	long size = infile.tellg();
	infile.seekg(0, ios::beg);
	char *buffer = new char[size];
	infile.read(buffer, size);
	infile.close();
	cout << "size：" << size;
	char *pdata = buffer;
	char *output = NULL;
	short *decode_buffer = NULL;
	int total_encoded_size = 0;
	fstream decodedfile(pcm_file, ios::out | ios::binary | ios::app);

	int decoded_size = myopus_decode(decoder, pdata, size, &decode_buffer);
	cout << "Opus decode return " << decoded_size << "." << endl;

	if (decoded_size > 0)
	{
		decodedfile.write((const char *)decode_buffer, decoded_size);
	}
	decodedfile.close();
	delete[] buffer;
}

string get_file_num_by_regex(string file_name, string regex)
{
	string result = "";
	int pos = file_name.find(regex);
	if (pos != string::npos)
	{
		result = file_name.substr(0, pos);
	}
	return result;
}

void remove_all_file_in_dir(string dir_path)
{
	for (auto &p : directory_iterator(dir_path))
	{
		remove(p.path().c_str());
	}
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        cout << "Usage: test indir outdir" << endl;
        return 1;
    }
    int ret = open_decoder(&decoder, 16000, 1);
    if (ret != 0) {
        cout << "Create opus decoder failed " << ret << "." << endl;
        return 2;
    }
	int max_num = 0;
	string in_dir = argv[1];
	string out_dir = argv[2];
	remove_all_file_in_dir(out_dir);
    directory_iterator end_itr;
	for (directory_iterator itr(argv[1]); itr != end_itr; ++itr)
	{
		if (is_regular_file(itr->status()))
		{
			string file_name = itr->path().filename().string();
			string file_num = get_file_num_by_regex(file_name, ".opus");
			int num = stoi(file_num);
			if (num > max_num)
			{
				max_num = num;
			}
		}
	}
	for (int i = 1; i <= max_num; ++i)
	{
		string opus_name = to_string(i) + ".opus";
		string pcm_name = to_string(i) + ".pcm";
		string opus_file = in_dir + "/" + opus_name;
		string pcm_file = out_dir + "/" + pcm_name;
		cout << "opus_file: " << opus_file << endl;
		cout << "pcm_file: " << pcm_file << endl;
		convert_opus_to_pcm(opus_file, pcm_file);
	}

	close_decoder(decoder);

    cout << "Test opus ok." << endl;

    return 0;
}
