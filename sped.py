"""Esse script realiza uma troca de classificação de notas que foram
   registradas com uma alíquota errada. A expectativa de saída é ser um novo
   arquivo SPED que pode ser importado pelo software contábil com as notas na
   classificação tributária correta, porém com uma inconsistência do contador
   que é automaticamente corrigida.

   Esse script só faz algumas substituições muito específicas, pois foi criado
   para um caso específico para uma empresa específica (e em um curtíssimo
   espaço de tempo)."""

import sys

if len(sys.argv) < 2:
    print('Passar o nome do arquivo sped')
    exit(0)

try:
    input_file = open(sys.argv[1], 'r', encoding='windows-1252')
except FileNotFoundError:
    print(f'Arquivo sped ${sys.argv[1]} informado não existe')
finally:
    exit(0)

out_name = 'saida.txt' if len(sys.argv) < 3 else sys.argv[2]
try:
    output_file = open(out_name, 'w', encoding='windows-1252', newline='\r\n')
except IOError:
    print('Sem permissão para gerar o arquivo de saída')
finally:
    exit(0)

flag_nota = False
flag_ajuste = False
reducao = 0.0
reducao_str = ''
valor_total = 0.0
valor_total_str = ''
aliquota = 0.0
aliquota_str = ''
result = 0.0
result_str = ''
icms_total = 0.0
icms_total_str = ''
counter = 0
id_nota = ''
lines_buffer = []
notas_counter = 0

for i, line in enumerate(input_file):
    flag_c100 = (line.find('|C100|') == 0)
    if (not flag_nota and not flag_c100):
        output_file.writelines(line)
        continue

    if (line.find('|C195|000001') != -1 or line.find('|C197|SC') != -1):
        counter = counter + 1
        print(f'Linha {i} desconsiderada: {line}')
        continue

    if (flag_c100 or line.find('|C500|') != -1):
        flag_nota = flag_c100
        if lines_buffer:
            for buffered_lines in lines_buffer:
                output_file.writelines(buffered_lines)

            if flag_ajuste:
                output_file.writelines('|C195|000001||'+'\n')
                output_file.writelines(
                    f'|C197|SC54000001|||{icms_total_str}|{reducao_str}|{result_str}|0|\n'
                )
                output_file.writelines(
                    f'|C197|SC24000001|||{valor_total_str}|{aliquota_str}|{icms_total_str}|0|\n'
                )
                output_file.writelines(
                    f'|C197|SC10000066|||{icms_total_str}|{reducao_str}|{result_str}|0|\n'
                )
                notas_counter = notas_counter + 1

            flag_ajuste = False
            lines_buffer = []

        if not flag_c100:
            output_file.writelines(line)
            continue

        colunas = line.split('|')

        valor_total_str = colunas[12]

        if valor_total_str == '':
            output_file.writelines(line)
            continue

        valor_total = float(colunas[12].replace(',', '.'))
        icms_total = float(colunas[22].replace(',', '.'))
        icms_total_str = colunas[22]
        id_nota = colunas[8]

    if (line.find('|C190|000|6107') != -1 or line.find('|C190|000|6108') != -1):
        flag_ajuste = True
        colunas = line.split('|')
        aliquota_str = colunas[4]
        aliquota = float(colunas[4].replace(',', '.'))
        if aliquota not in (7.0, 12.0):
            print('Alíquota não esperada: ', aliquota)
            exit(0)
        reducao = float('83.33') if aliquota == 12.0 else float('71.43')
        reducao_str = "{:.2f}".format(reducao).replace('.', ',')
        result = icms_total * (reducao / 100)
        result_str = "{:.2f}".format(result).replace('.', ',')

    lines_buffer.append(line)

print('Total de linhas C195 e C197 não consideradas: ', counter)
print('Quantidade de notas alteradas: ', notas_counter)
print('--------------------------------------------------------')
print('')
