import RLstruct as RL


def string_interp(some_string):
    actions = ['+', '.', '*']
    action_array = []
    num = ''
    main_struct = None
    skip_indexes = []

    def find_in_string(start_symbol, flag_first):
        num = ''
        tmp_struct = None
        range_skip = []
        for i in range(start_symbol, len(some_string)):
            if i in range_skip:
                #print("tmp_struct")
                continue
            if some_string[i] in actions:
                if tmp_struct is None:
                    if flag_first:
                        tmp_struct = RL.Char(num)
                        flag_first = False
                if i + 1 < len(some_string):
                    if some_string[i] == actions[0]:
                        # print("+:", tmp_struct)
                        second_num = find_in_string(i + 1, True)
                        tmp_struct = RL.Alternative(tmp_struct, second_num)
                        #print(tmp_struct)
                        return tmp_struct
                    if some_string[i] == actions[1]:
                        second_num = find_in_string(i + 1, True)
                        tmp_struct = RL.Sequence(tmp_struct, second_num)
                        #print(tmp_struct)
                        return tmp_struct
                    if some_string[i] == actions[2]:
                        #print("bef *:", tmp_struct)
                        tmp_struct = RL.Repetition(tmp_struct)
                        #print(tmp_struct)
            elif some_string[i] == '(':
                indexes = 1
                tmp_index = search_skob(i + 1, indexes)
                if tmp_index is None:
                    print("error")
                    return None
                tmp_string = some_string[i+1:tmp_index]
                for j in range(i, tmp_index + 1):
                    range_skip.append(j)
                #print(range_skip)
                # print("tmp_str:", tmp_string)
                tmp_struct = string_interp(tmp_string)
                #print("tmp_struct:", tmp_struct)
                continue
            elif some_string[i] != ' ':
                num += some_string[i]
            main_struct = tmp_struct
        return RL.Char(num)

    def search_skob(start_index, indexes):
        for i in range(start_index, len(some_string)):
            # print(some_string[i])
            if some_string[i] == ')':
                indexes -= 1
            if indexes == 0:
                return i
            if some_string[i] == '(':
                indexes += 1
        return None

    main_struct = find_in_string(0, True)
    # print("m_s:", main_struct)
    return main_struct


if __name__ == '__main__':
    rl = string_interp('0 + (1.0)*')
    print("rl:", rl)
    st = '1'
    print(RL.match(rl, st))
