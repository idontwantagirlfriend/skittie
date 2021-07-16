def top_n_rank(element_list: list, top_num: int, step_word: set = {"的", "有", "和", "了", "与", "为", "在", "上", "等", "而", "以", "如", "之", "只",
                                                                   "是", "都", "即", "后", "中", "同", "从", "及", "也", "对", "到"}):
    """Applies to any (duplicate) element list. Calculate the top_num most frequent element(s).
    If a negative value is used for top_num, calculate the top_num rarest element(s).
    Return a list.
    This method is initially for calculating word frequency for Chinese text samples."""
    frequency = {}
    for i in element_list:
        frequency[i] = frequency.get(i, 0)+1

    filtered_frequency = []  # is a list
    for i in frequency:
        if not i in step_word:
            filtered_frequency.append([i, frequency[i]])
    filtered_frequency = sorted(
        filtered_frequency, key=lambda x: x[1], reverse=True)

    if (-len(filtered_frequency)-1) < top_num < (len(filtered_frequency)+1):
        if top_num > -1:
            # Top top_num frequent element(s).
            rank = filtered_frequency[:top_num]
        else:
            # Top top_num rare element(s) if top_num is negative.
            rank = filtered_frequency[top_num:]
    else:
        rank = filtered_frequency
        if __name__ == "__main__":
            message = f"Given rank number exceeds max rank ({len(filtered_frequency)})."
            print(message)

    return rank
    print("Calculation terminated.")


def main():
    new_string = r"a;sdlkfjdsa;ldkjfa;slfdknzxmnvcbzxcgjq0iw4uerjaskjdfslzxmvcnlmna;sdkjfqwpwoiertj;dszlxkncv.xmcnvpqwoiejfd;aslkdfas;ldkfjas;gknvc.x,mnv.x,msdnglkwope;gkjfd;lsknbs;lkjg;lkj;ldsakdjg;aslkdjg0[qporitepdfkvcmx.,bmds/.,q[pwejdf;zlkmn;lmnde;qokwj;erlqkajdn;mcxng[pqpkrjtedf;clk;o&ÛP$#@OIWURP(*EUROHFNkdjnsag;laldvjcnx;zlkjg[qeepoi[04ip15"
    make_a_list = list(new_string)
    return top_n_rank(make_a_list, 1000)


print(main())
