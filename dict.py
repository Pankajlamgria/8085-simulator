register_index={'A':0,'Temp':1,'Instruction':2,'B':3,'C':4,'D':5,'E':6,'H':7,'L':8,'M':(7,8)}
# TODO Create all instructions oppcode and the bytes of instruction to store
register={"000":'B','001':'C','010':'D','011':'E','100':'H','101':'L','110':'M','111':'A'}
register_pairs={"00":'B','01':'D','10':'H','11':'S'}
status_index={'Z':6,'S':7,'C':0,'P':2,'AC':4}
jump_status={"000":'NZ','001':'Z','010':'NC','011':'C','100':"PO",'101':'PE',"110":"P",'111':'M'}


oppcode = {
    'ACI': 'CE', 'ADC A': '8F', 'ADC B': '88', 'ADC C': '89', 'ADC D': '8A', 'ADC E': '8B', 'ADC H': '8C', 'ADC L': '8D', 'ADC M': '8E', 
    'ADD A': '87', 'ADD B': '80', 'ADD C': '81', 'ADD D': '82', 'ADD E': '83', 'ADD H': '84', 'ADD L': '85', 'ADD M': '86', 
    'ADI': 'C6', 'ANA A': 'A7', 'ANA B': 'A0', 'ANA C': 'A1', 'ANA D': 'A2', 'ANA E': 'A3', 'ANA H': 'A4', 'ANA L': 'A5', 
    'ANA M': 'A6', 'ANI': 'E6', 'CALL': 'CD', 'CC': 'DC', 'CM': 'FC', 'CMA': '2F', 'CMC': '3F', 
    'CMP A': 'BF', 'CMP B': 'B8', 'CMP C': 'B9', 'CMP D': 'BA', 'CMP E': 'BB', 'CMP H': 'BC', 'CMP L': 'BD', 'CMP M': 'BE', 
    'CNC': 'D4', 'CNZ': 'C4', 'CP': 'F4', 'CPE': 'EC', 'CPI': 'FE', 'CPO': 'E4', 
    'CZ': 'CC', 'DAA': '27', 'DAD B': '09', 'DAD D': '19', 'DAD H': '29', 'DAD SP': '39', 'DCR A': '3D', 'DCR B': '05', 
    'DCR C': '0D', 'DCR D': '15', 'DCR E': '1D', 'DCR H': '25', 'DCR L': '2D', 'DCR M': '35', 'DCX B': '0B', 'DCX D': '1B', 
    'DCX H': '2B', 'DCX SP': '3B', 'DI': 'F3', 'EI': 'FB', 'HLT': '76', 'IN Port-address': 'DB', 'INR A': '3C', 'INR B': '04', 
    'INR C': '0C', 'INR D': '14', 'INR E': '1C', 'INR H': '24', 'INR L': '2C', 'INR M': '34', 'INX B': '03', 'INX D': '13', 
    'INX H': '23', 'INX SP': '33', 'JC': 'DA', 'JM': 'FA', 'JMP': 'C3', 'JNC': 'D2', 'JNZ': 'C2', 
    'JP': 'F2', 'JPE': 'EA', 'JPO': 'E2', 'JZ': 'CA', 'LDA': '3A', 'LDAX B': '0A', 'LDAX D': '1A', 
    'LHLD': '2A', 'LXI B': '01', 'LXI D': '11', 'LXI H': '21', 'LXI SP': '31', 'MOV A, A': '7F', 'MOV A, B': '78', 
    'MOV A, C': '79', 'MOV A, D': '7A', 'MOV A, E': '7B', 'MOV A, H': '7C', 'MOV A, L': '7D', 'MOV A, M': '7E', 'MOV B, A': '47', 
    'MOV B, B': '40', 'MOV B, C': '41', 'MOV B, D': '42', 'MOV B, E': '43', 'MOV B, H': '44', 'MOV B, L': '45', 'MOV B, M': '46', 
    'MOV C, A': '4F', 'MOV C, B': '48', 'MOV C, C': '49', 'MOV C, D': '4A', 'MOV C, E': '4B', 'MOV C, H': '4C', 'MOV C, L': '4D', 
    'MOV C, M': '4E', 'MOV D, A': '57', 'MOV D, B': '50', 'MOV D, C': '51', 'MOV D, D': '52', 'MOV D, E': '53', 'MOV D, H': '54', 
    'MOV D, L': '55', 'MOV D, M': '56', 'MOV E, A': '5F', 'MOV E, B': '58', 'MOV E, C': '59', 'MOV E, D': '5A', 'MOV E, E': '5B', 
    'MOV E, H': '5C', 'MOV E, L': '5D', 'MOV E, M': '5E', 'MOV H, A': '67', 'MOV H, B': '60', 'MOV H, C': '61', 'MOV H, D': '62', 
    'MOV H, E': '63', 'MOV H, H': '64', 'MOV H, L': '65', 'MOV H, M': '66', 'MOV L, A': '6F', 'MOV L, B': '68', 'MOV L, C': '69', 
    'MOV L, D': '6A', 'MOV L, E': '6B', 'MOV L, H': '6C', 'MOV L, L': '6D', 'MOV L, M': '6E', 'MOV M, A': '77', 'MOV M, B': '70', 
    'MOV M, C': '71', 'MOV M, D': '72', 'MOV M, E': '73', 'MOV M, H': '74', 'MOV M, L': '75', 'MVI A,': '3E', 'MVI B,': '06', 
    'MVI C,': '0E', 'MVI D,': '16', 'MVI E,': '1E', 'MVI H,': '26', 'MVI L,': '2E', 'MVI M,': '36', 
    'NOP': '00', 'ORA A': 'B7', 'ORA B': 'B0','ORA C': 'B1', 'ORA D': 'B2', 'ORA E': 'B3', 'ORA H': 'B4', 'ORA L': 'B5', 'ORA M': 'B6', 'ORI': 'F6', 'OUT Port-Address': 'D3', 
    'PCHL': 'E9', 'POP B': 'C1', 'POP D': 'D1', 'POP H': 'E1', 'POP PSW': 'F1', 'PUSH B': 'C5', 'PUSH D': 'D5', 'PUSH H': 'E5', 
    'PUSH PSW': 'F5', 'RAL': '17', 'RAR': '1F', 'RC': 'D8', 'RET': 'C9', 'RIM': '20', 'RLC': '07', 'RM': 'F8', 'RNC': 'D0', 
    'RNZ': 'C0', 'RP': 'F0', 'RPE': 'E8', 'RPO': 'E0', 'RRC': '0F', 'RST 0': 'C7', 'RST 1': 'CF', 'RST 2': 'D7', 'RST 3': 'DF', 
    'RST 4': 'E7', 'RST 5': 'EF', 'RST 6': 'F7', 'RST 7': 'FF', 'RZ': 'C8', 'SBB A': '9F', 'SBB B': '98', 'SBB C': '99', 
    'SBB D': '9A', 'SBB E': '9B', 'SBB H': '9C', 'SBB L': '9D', 'SBB M': '9E', 'SBI': 'DE', 'SHLD': '22', 
    'SIM': '30', 'SPHL': 'F9', 'STA': '32', 'STAX B': '02', 'STAX D': '12', 'STC': '37', 'SUB A': '97', 'SUB B': '90', 
    'SUB C': '91', 'SUB D': '92', 'SUB E': '93', 'SUB H': '94', 'SUB L': '95', 'SUB M': '96', 'SUI': 'D6', 'XCHG': 'EB', 
    'XRA A': 'AF', 'XRA B': 'A8', 'XRA C': 'A9', 'XRA D': 'AA', 'XRA E': 'AB', 'XRA H': 'AC', 'XRA L': 'AD', 'XRA M': 'AE', 
    'XRI': 'EE'}

instruction_byte={"ACI":2,"ADC":1,"ADD":1,"ADI":2,"ANA":1,'ANI':2,'CALL':3,'CC':3,'CM':3,'CMC':1,'CMA':1,'CMP':1,'CNC':3,'CNZ':3,"CP":3,'CPE':3,'CPI':2,'CPO':3,'CZ':3,'DAA':1,'DAD':1,'DCR':1,'DCX':1,'INR':1,'INX':1,'JC':3,'JM':3,'JMP':3,'JNC':3,'JNZ':3,'JP':3,'JPE':3,'JPO':3,'JZ':3,'LDA':3,'LDAX':1,'LHLD':3,'LXI':3,'MOV':1,'MVI':2,'NOP':1,'ORA':1,'POP':1,'PUSH':1,'RAL':1,'RAR':1,'RC':1,'RET':1,'RIM':1,'RLC':1,'RM':1,'RNC':1,'RNZ':1,'RRC':1,'SBB':1,'SHLD':3,'SBI':2,'STA':3,'STAX':1,'SUB':1,'SBB':1,'SBI':2,'HLT':1,'XCHG':1,'XRA':1,'SUI':2}
    
swapped_opcode = {
    'CE': 'ACI', '8F': 'ADC A', '88': 'ADC B', '89': 'ADC C', '8A': 'ADC D', '8B': 'ADC E', '8C': 'ADC H', '8D': 'ADC L', '8E': 'ADC M', 
    '87': 'ADD A', '80': 'ADD B', '81': 'ADD C', '82': 'ADD D', '83': 'ADD E', '84': 'ADD H', '85': 'ADD L', '86': 'ADD M', 
    'C6': 'ADI', 'A7': 'ANA A', 'A0': 'ANA B', 'A1': 'ANA C', 'A2': 'ANA D', 'A3': 'ANA E', 'A4': 'ANA H', 'A5': 'ANA L', 
    'A6': 'ANA M', 'E6': 'ANI', 'CD': 'CALL', 'DC': 'CC', 'FC': 'CM', '2F': 'CMA', '3F': 'CMC', 
    'BF': 'CMP A', 'B8': 'CMP B', 'B9': 'CMP C', 'BA': 'CMP D', 'BB': 'CMP E', 'BC': 'CMP H', 'BD': 'CMP L', 'BE': 'CMP M', 
    'D4': 'CNC', 'C4': 'CNZ', 'F4': 'CP', 'EC': 'CPE', 'FE': 'CPI', 'E4': 'CPO', 
    'CC': 'CZ', '27': 'DAA', '09': 'DAD B', '19': 'DAD D', '29': 'DAD H', '39': 'DAD SP', '3D': 'DCR A', '05': 'DCR B', 
    '0D': 'DCR C', '15': 'DCR D', '1D': 'DCR E', '25': 'DCR H', '2D': 'DCR L', '35': 'DCR M', '0B': 'DCX B', '1B': 'DCX D', 
    '2B': 'DCX H', '3B': 'DCX SP', 'F3': 'DI', 'FB': 'EI', '76': 'HLT', 'DB': 'IN Port-address', '3C': 'INR A', '04': 'INR B', 
    '0C': 'INR C', '14': 'INR D', '1C': 'INR E', '24': 'INR H', '2C': 'INR L', '34': 'INR M', '03': 'INX B', '13': 'INX D', 
    '23': 'INX H', '33': 'INX SP', 'DA': 'JC', 'FA': 'JM', 'C3': 'JMP', 'D2': 'JNC', 'C2': 'JNZ', 
    'F2': 'JP', 'EA': 'JPE', 'E2': 'JPO', 'CA': 'JZ', '3A': 'LDA', '0A': 'LDAX B', '1A': 'LDAX D', 
    '2A': 'LHLD', '01': 'LXI B', '11': 'LXI D', '21': 'LXI H', '31': 'LXI SP', '7F': 'MOV A, A', '78': 'MOV A, B', 
    '79': 'MOV A, C', '7A': 'MOV A, D', '7B': 'MOV A, E', '7C': 'MOV A, H', '7D': 'MOV A, L', '7E': 'MOV A, M', '47': 'MOV B, A', 
    '40': 'MOV B, B', '41': 'MOV B, C', '42': 'MOV B, D', '43': 'MOV B, E', '44': 'MOV B, H', '45': 'MOV B, L', '46': 'MOV B, M', 
    '4F': 'MOV C, A', '48': 'MOV C, B', '49': 'MOV C, C', '4A': 'MOV C, D', '4B': 'MOV C, E', '4C': 'MOV C, H', '4D': 'MOV C, L', 
    '4E': 'MOV C, M', '57': 'MOV D, A', '50': 'MOV D, B', '51': 'MOV D, C', '52': 'MOV D, D', '53': 'MOV D, E', '54': 'MOV D, H', 
    '55': 'MOV D, L', '56': 'MOV D, M', '5F': 'MOV E, A', '58': 'MOV E, B', '59': 'MOV E, C', '5A': 'MOV E, D', '5B': 'MOV E, E', 
    '5C': 'MOV E, H', '5D': 'MOV E, L', '5E': 'MOV E, M', '67': 'MOV H, A', '60': 'MOV H, B', '61': 'MOV H, C', '62': 'MOV H, D', 
    '63': 'MOV H, E', '64': 'MOV H, H', '65': 'MOV H, L', '66': 'MOV H, M', '6F': 'MOV L, A', '68': 'MOV L, B', '69': 'MOV L, C', 
    '6A': 'MOV L, D', '6B': 'MOV L, E', '6C': 'MOV L, H', '6D': 'MOV L, L', '6E': 'MOV L, M', '77': 'MOV M, A', '70': 'MOV M, B', 
    '71': 'MOV M, C', '72': 'MOV M, D', '73': 'MOV M, E', '74': 'MOV M, H', '75': 'MOV M, L', '3E': 'MVI A,', '06': 'MVI B,', 
    '0E': 'MVI C,', '16': 'MVI D,', '1E': 'MVI E,', '26': 'MVI H,', '2E': 'MVI L,', '36': 'MVI M,', 
    '00': 'NOP', 'B7': 'ORA A', 'B0': 'ORA B', 'B1': 'ORA C', 'B2': 'ORA D', 'B3': 'ORA E', 'B4': 'ORA H','B5': 'ORA L', 'B6': 'ORA M', 'F6': 'ORI', 'D3': 'OUT Port-Address', 'E9': 'PCHL', 'C1': 'POP B', 'D1': 'POP D', 'E1': 'POP H', 
    'F1': 'POP PSW', 'C5': 'PUSH B', 'D5': 'PUSH D', 'E5': 'PUSH H', 'F5': 'PUSH PSW', '17': 'RAL', '1F': 'RAR', 'D8': 'RC', 'C9': 'RET', 
    '20': 'RIM', '07': 'RLC', 'F8': 'RM', 'D0': 'RNC', 'C0': 'RNZ', 'F0': 'RP', 'E8': 'RPE', 'E0': 'RPO', '0F': 'RRC', 'C7': 'RST 0', 
    'CF': 'RST 1', 'D7': 'RST 2', 'DF': 'RST 3', 'E7': 'RST 4', 'EF': 'RST 5', 'F7': 'RST 6', 'FF': 'RST 7', 'C8': 'RZ', '9F': 'SBB A', 
    '98': 'SBB B', '99': 'SBB C', '9A': 'SBB D', '9B': 'SBB E', '9C': 'SBB H', '9D': 'SBB L', '9E': 'SBB M', 'DE': 'SBI', '22': 'SHLD', 
    '30': 'SIM', 'F9': 'SPHL', '32': 'STA', '02': 'STAX B', '12': 'STAX D', '37': 'STC', '97': 'SUB A', '90': 'SUB B', '91': 'SUB C', 
    '92': 'SUB D', '93': 'SUB E', '94': 'SUB H', '95': 'SUB L', '96': 'SUB M', 'D6': 'SUI', 'EB': 'XCHG', 'AF': 'XRA A', 'A8': 'XRA B', 
    'A9': 'XRA C', 'AA': 'XRA D', 'AB': 'XRA E', 'AC': 'XRA H', 'AD': 'XRA L', 'AE': 'XRA M', 'EE': 'XRI'
    }


