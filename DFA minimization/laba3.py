import csv


def csv_read(file_name):
    with open(file_name, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        some_dict = {}
        flag_swap = True
        new_alth = []
        for row in spamreader:
            if flag_swap:
                for some_symbol in row:
                    if some_symbol == '': continue
                    else: new_alth.append(some_symbol)
                flag_swap = False
            else:
                some_dict[row[0]] = {}
                for i in range(len(new_alth)):
                    some_dict[row[0]][new_alth[i]] = row[i + 1]
        return new_alth, some_dict


def minimiz_of_graph(alphabet_use, graph_array, fin):

    def split(R_class, splitter_q, splitter_a):
        R_class1 = []
        R_class2 = []
        for r in R_class:
            if graph_array[r][splitter_a] == splitter_q:
                R_class1.append(r)
            else:
                R_class2.append(r)
        return R_class1, R_class2

    Q_no_f = [x for x in graph_array.keys() if x not in fin]
    final_graph = [fin, Q_no_f]  # [F, Q \ F]
    S_queue = []
    for symbol_ in alphabet_use:
        for f in fin:
            S_queue.append((graph_array[f][symbol_], symbol_))
        for q_f in Q_no_f:
            S_queue.append((graph_array[q_f][symbol_], symbol_))
    while S_queue != []:
        splitter = S_queue.pop(0)
        for R in final_graph:
            R1, R2 = split(R, splitter[0], splitter[1])
            if R1 != [] and R2 != []:
                i = final_graph.index(R)
                final_graph.pop(i)
                final_graph.insert(i, R2)
                final_graph.insert(i, R1)
                for symbol_ in alphabet_use:
                    for q in R1:
                        S_queue.append((q, symbol_))
                    for q in R2:
                        S_queue.append((q, symbol_))
    return final_graph


def make_minimized_graph(graph, minimized, alphabet):
    final_graph = {}
    for el in minimized:
        temp_dict = {}
        f_q = ''
        for q in el:
            for symbol in alphabet:
                temp_dict[symbol] = graph[q][symbol]
            f_q += q
        final_graph[f_q] = temp_dict
    return final_graph


def check_min_graph(old_graph, min_graph, alphabet):
    flag = True
    for key0 in old_graph:
        for key1 in min_graph:
            if key0 in key1:
                for symbol in alphabet:
                    if old_graph[key0][symbol] != min_graph[key1][symbol]:
                        flag = False
    return flag


if __name__ == '__main__':
    file_open = "graph.csv"
    alphabet, graph_array = csv_read(file_open)
    print("#####-------#####\nОригинальный граф:")
    for key in graph_array:
        print(key, ":", graph_array[key])
    print("#####-------#####\nВведите финаьные состояния: (Вида: A B C D)")
    fin = input().split(' ')
    print("Введённые финальные состояния:", fin)
    P = minimiz_of_graph(alphabet, graph_array, fin)
    print("#####-------#####\nОбъединённые состояния:", P)
    minimized_graph = make_minimized_graph(graph_array, P, alphabet)
    print("#####-------#####\nМинимизированный граф:")
    for key in minimized_graph:
        print(key, ":", minimized_graph[key])
    print("#####-------#####\nпроверка:")
    if not check_min_graph(graph_array, minimized_graph, alphabet):
        print("Граф не эквивалентен")
    else:
        print("Граф эквивалентен")
