def multizip_sort_interruptible(x, max_comparisons):
    if not isinstance(x, list):
        raise TypeError("A entrada para multizip_sort deve ser uma lista.")

    start_time = time.perf_counter() # Inicia a contagem do tempo

    comparison_counter = [0]  # encapsulado em lista para ser mutável
    y_lists = [x]

    def merge_interrupt(lista1, lista2):
        result = []
        ptr1 = ptr2 = 0
        while ptr1 < len(lista1) and ptr2 < len(lista2):
            if comparison_counter[0] >= max_comparisons:
                # Interrompe a fusao atual se o limite for atingido
                break
            comparison_counter[0] += 1
            if lista1[ptr1] <= lista2[ptr2]:
                result.append(lista1[ptr1])
                ptr1 += 1
            else:
                result.append(lista2[ptr2])
                ptr2 += 1
        result.extend(lista1[ptr1:])
        result.extend(lista2[ptr2:])
        return result

    # Split até ter listas de tamanho 1
    while any(len(lst) > 1 for lst in y_lists):
        novas = []
        for y in y_lists:
            meio = math.ceil(len(y) / 2)
            novas.append(y[:meio])
            novas.append(y[meio:])
        y_lists = novas

    # Merge com interrupção
    interrupted_merge = False
    while len(y_lists) > 1:
        nova_y = []
        i = 0
        while i + 1 < len(y_lists):
            # Passa o contador de comparacoes para a funcao merge
            merged = merge_interrupt(y_lists[i], y_lists[i + 1])
            nova_y.append(merged)
            i += 2
            if comparison_counter[0] >= max_comparisons:
                interrupted_merge = True
                print(f"--- Interrupção na fusão: Alcançado o limite de {max_comparisons} comparações. ---")
                break # Interrompe o loop de fusao atual
        if i < len(y_lists) and not interrupted_merge:
            nova_y.append(y_lists[i])
        y_lists = nova_y

        if interrupted_merge:
            break # Interrompe o loop principal se a fusao foi interrompida


    end_time = time.perf_counter() # Finaliza a contagem do tempo
    print(f"--- Tempo de execução: {end_time - start_time:.6f} segundos. ---")

    # Junta tudo mesmo se incompleto
    resultado_final = []
    for sub in y_lists:
        resultado_final.extend(sub)

    return resultado_final
