from pymystem3 import Mystem

TOKEN = '396049063:AAHxoiwtiYRGXU2hc808QNUReoJ9vr_KNlU'

WEBHOOK_HOST = 'IAmAgainstHomonymyBot.pythonanywhere.com'
WEBHOOK_PORT = '443'


def LINE_ANALISE(line):
    list_to_reply = []
    m = Mystem()
    ana = m.analyze(line)
    for element in ana:
        ana_line = []
        if 'analysis' in element and element['analysis'] != []:
            gr = element['analysis'][0]['gr']
            part_1 = gr.split('=')[0]
            part_2 = gr.split('=')[1]
            if '(' in part_2:
                part_2 = part_2.strip('(')
                part_2 = part_2.strip(')')
                list_of_part_2 = part_2.split('|')
                ana_line.append(element['text'])
                for el in list_of_part_2:
                    analyze_string = part_1 + ',' + el
                    ana_line.append(analyze_string)
                list_to_reply.append(ana_line)
            elif part_2 == '':
                analyze_string = part_1
                ana_line.append(element['text'])
                ana_line.append(analyze_string)
                list_to_reply.append(ana_line)
            else:
                analyze_string = part_1 + ',' + part_2
                ana_line.append(element['text'])
                ana_line.append(analyze_string)
                list_to_reply.append(ana_line)

    return list_to_reply

STICK_PACK_ERROR = ['CAADAQADaQQAAmbKaAlrVmuiv1v57wI', 'CAADAQADiQQAAmbKaAmZRy2LtCeUQgI',
                    'CAADAQADlwQAAmbKaAk2DoCutNE7sAI', 'CAADAQADRgQAAmbKaAlG9dZcqEgV1QI',
                    'CAADAQADOAQAAmbKaAnD5jO7IweE3AI', 'CAADAQADQAQAAmbKaAnRpZ5QVAktHAI',
                    'CAADAQADRAQAAmbKaAncmzaNpH9HTwI', 'CAADAQADngQAAmbKaAnPpLC0G4wi3QI',
                    'CAADAQADmAQAAmbKaAlkqQZ1T5CsxwI']

STICK_PACK_SUCCESS = ['CAADAQADQgQAAmbKaAn584hN_tAzOwI', 'CAADAQADJwQAAmbKaAkUdaSzyTIdewI',
                      'CAADAQADKQQAAmbKaAlTTXl41rWPkwI', 'CAADAQADbAQAAmbKaAlD-sfI9af9nwI',
                      'CAADAQADbgQAAmbKaAnTHcXFu0tZQwI', 'CAADAQADKAQAAmbKaAm3A55Kf0a6VAI']

STICK_HELP = 'CAADAQADnQQAAmbKaAkCmX6bXOGFlgI'
