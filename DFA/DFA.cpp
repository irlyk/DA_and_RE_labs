// DFA.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>

using namespace std;

class DFA {
public:
	vector<vector<int>> table; //таблица состояний
	vector<char> eps = { '0','1','2' }; //алфавит
	vector<int> fin;

	void readFin() {
		setlocale(LC_ALL, "RUSSIAN");
		cout << "Введите конечные состояния: (вида '1 2 3 ...')" << endl;
		string input1;
		getline(cin, input1);
		if (input1.empty()) {
			cout << "Конечные состояния заданы неверно!" << endl;
			exit(-1);
		}
		stringstream bufferStream(input1);
		string tmp;
		while (getline(bufferStream, tmp, ' '))
		{
			if (tmp.empty()) {
				continue;
			}

			try {
				fin.push_back(atoi(tmp.c_str()));
			}
			catch (exception e) {
				cout << "не удалось преобразовать в int!" << endl;
				exit(-1);
			}
		}
	}

	void printFin() {
		setlocale(LC_ALL, "RUSSIAN");
		cout << "Введённые конечные состояния:" << endl;
		for (int i = 0; i < fin.size(); i++) {
			cout << fin[i] << "; ";
		}
		cout << endl;
	}

	void printAlf() {
		cout << "Алфавит:" << endl;
		for (int i = 0; i < eps.size(); i++) {
			cout << eps[i] << "; ";
		}
		cout << endl;
	}

	void readTable(string filename) {
		setlocale(LC_ALL, "RUSSIAN");
		ifstream in(filename);
		if (in.is_open())
		{
			string buffer; //буфер считывания строки
			while (!in.eof())
			{
				getline(in, buffer);
				if (buffer.empty()) {
					continue;
				}
				stringstream bufferStream(buffer); //поток считанной строки
				vector<int> vec_buff; //временный вектор
				string tmp; //временная строка
				while (getline(bufferStream, tmp, ';'))
				{
					if (tmp.empty()) {
						continue;
					}
					try {
						vec_buff.push_back(atoi(tmp.c_str()));
					}
					catch (exception e) {
						cout << "не удалось преобразовать в int!" << endl;
						exit(-1);
					}
				}
				table.push_back(vec_buff);
			}
		}
		else
		{
			cout << "Файл не найден.";
			exit(-1);
		}
		in.close();
	}

	bool isBellongTo(string cc, int start) {
		stringstream ss(cc);
		char a;
		int q = start, cur = 0;
		while (ss.get(a)) {
			for (int i = 0; i < eps.size(); i++) {
				if (eps[i] == a) {
					cur = i;
					break;
				}
			}
			q = table[q][cur];
		}
		for (int i = 0; i < fin.size(); i++) {
			if (q == fin[i]) {
				return true;
			}
		}
		return false;
	}

	void printTable() {
		setlocale(LC_ALL, "RUSSIAN");
		cout << "считанная таблица состояний:" << endl;
		for (int i = 0; i < table.size(); i++) {
			cout << "q" << i << ": ";
			for (int j = 0; j < table[i].size(); j++) {
				cout << table[i][j] << "; ";
			}
			cout << endl;
		}
		cout << endl;
	}
};


int main()
{
	setlocale(LC_ALL, "RUSSIAN");

	DFA dfa;
	dfa.readTable("123.csv");
	dfa.printTable();
	dfa.readFin();
	dfa.printFin();
	dfa.printAlf();

	int start;
	cout << "Ведите начальное состояние:" << endl;
	cin >> start;

	while (true) {
		cout << "Ведите цепочку:" << endl;
		string input;
		cin >> input;
		if (dfa.isBellongTo(input, start))
			cout << "Принадлежит" << endl;
		else
			cout << "Не принадлежит" << endl;

		cout << endl;
	}
}
