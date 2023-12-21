
eight_bit_registers = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]
sixteen_bit_registers =["ax", 'bx', 'cx', 'dx', 'bp', 'di' ,'si']
thirty_two_bit_registers = ["eax", "ecx", "edx", "ebx", "esp", "ebp", "esi", "edi"]


register_map = {
    
    "al": (0, 0, 0),
    "ax": (0, 0, 0),
    "eax": (0, 0, 0),
    
    "cl": (0, 0, 1),
    "cx": (0, 0, 1),
    "ecx": (0, 0, 1),
    
    "dl": (0, 1, 0),
    "dx": (0, 1, 0),
    "edx": (0, 1, 0),
    
    "bl": (0, 1, 1),
    "bx": (0, 1, 1),
    "ebx": (0, 1, 1),        

    "ah": (1, 0, 0),
    "sp": (1, 0, 0),
    "esp": (1, 0, 0),

    "ch": (1, 0, 1),
    "bp": (1, 0, 1),
    "ebp": (1, 0, 1),
    
    "dh": (1, 1, 0),
    "si": (1, 1, 0),
    "esi": (1, 1, 0),
    
    "bh": (1, 1, 1),
    "di": (1, 1, 1),
    "edi": (1, 1, 1),        
    }

memory_map = {

    
    "[al]": (0, 0, 0),
    "[ax]": (0, 0, 0),
    "[eax]": (0, 0, 0),
    
    "[cl]": (0, 0, 1),
    "[cx]": (0, 0, 1),
    "[ecx]": (0, 0, 1),
    
    "[dl]": (0, 1, 0),
    "[dx]": (0, 1, 0),
    "[edx]": (0, 1, 0),
    
    "[bl]": (0, 1, 1),
    "[bx]": (0, 1, 1),
    "[ebx]": (0, 1, 1),        

    "[ah]": (1, 0, 0),
    "[sp]": (1, 0, 0),
    "[esp]": (1, 0, 0),

    "[ch]": (1, 0, 1),
    "[bp]": (1, 0, 1),
    "[ebp]": (1, 0, 1),
    
    "[dh]": (1, 1, 0),
    "[si]": (1, 1, 0),
    "[esi]": (1, 1, 0),
    
    "[bh]": (1, 1, 1),
    "[di]": (1, 1, 1),
    "[edi]": (1, 1, 1),        
    }

rd_rw_map = {
    # Integer values in decimal form
    "ax": 0, "cx": 1, "dx": 2, "bx": 3,
    "sp": 4, "bp": 5, "si": 6, "di": 7,
    "eax": 0, "ecx": 1, "edx": 2, "ebx": 3,
    "esp": 4, "ebp": 5, "esi": 6, "edi": 7,
}
    

def add(instruction, op_code, mod_rm):
    sixteen = False
    
    if instruction[1] not in memory_map and instruction[2] not in memory_map: # both are registers   
        mod_rm[0] = 1
        mod_rm[1] = 1  # for register
        
        register1 = instruction[1].lower()
        register2 = instruction[2].lower()
                     
        if register1 in eight_bit_registers:
            op_code[6] = 0
            op_code[7] = 0  # 8 bit reg
        elif register1 in sixteen_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 16 bit reg
            sixteen = True       
        elif register1 in thirty_two_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 32 bit reg
        if register1 in register_map and register2 in register_map:
            mod_rm[5:8] = register_map[register1]
            mod_rm[2:5] = register_map[register2]
            
            op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
            mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)
            
            if sixteen:
                result = ('66 ' + op_code_hex + " " + mod_rm_hex)
                return result
            else:
                 result=(op_code_hex + " " + mod_rm_hex)
                 return str(result)
                         
    elif instruction[1] in memory_map and (instruction[2] in thirty_two_bit_registers):
    # mem/reg
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling      
        op_code[6] = 0
        
        register = instruction[2]
        memory = instruction[1]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
                            
            if register in register in thirty_two_bit_registers :
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                
                op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
                mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)
                            
                result = (op_code_hex + " " + mod_rm_hex)
                return str(result)                   
                         

    elif instruction[2] in memory_map and ( instruction[1] in thirty_two_bit_registers):
    # reg/mem

        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling

        op_code[6] = 1

        register = instruction[1]
        memory = instruction[2]

        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]

            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]

            op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
            mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)            

            result = (op_code_hex + " " + mod_rm_hex)
            return result
        
#####################################################

def sub(instruction, op_code, mod_rm):
    sixteen = False        
    op_code[2]=1
    op_code[4]=1   
    if instruction[1] not in memory_map and instruction[2] not in memory_map: # both are registers 
    
        mod_rm[0] = 1
        mod_rm[1] = 1  # for register
        
        register1 = instruction[1].lower()
        register2 = instruction[2].lower()
                
        if register1 in eight_bit_registers:
            op_code[6] = 0
            op_code[7] = 0  # 8 bit reg
        elif register1 in sixteen_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 16 bit reg
            sixteen = True       
        elif register1 in thirty_two_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 32 bit reg
            

        if register1 in register_map and register2 in register_map:
            mod_rm[5:8] = register_map[register1]
            mod_rm[2:5] = register_map[register2]            
            
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
            
        if sixteen:

            result = ('66 ' + op_code_hex + " " + mod_rm_hex)
            return result
        
        else:
            result = (op_code_hex + " " + mod_rm_hex)
            return result
                              
    elif instruction[1] in memory_map and (instruction[2] in thirty_two_bit_registers):
    # mem/reg
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling     
        op_code[6] = 0
        
        register = instruction[2]
        memory = instruction[1]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
        
        result = (op_code_hex + " " + mod_rm_hex)
        return result
                                         
    elif instruction[2] in memory_map and (instruction[1] in thirty_two_bit_registers):
    # reg/mem
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling
        
        op_code[6] = 1
        
        register = instruction[1]
        memory = instruction[2]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                    
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
        
        result = (op_code_hex + " " + mod_rm_hex)
        return result
    

    else:
        print("format not supported")
          
#####################################################      

def And(instruction, op_code, mod_rm):
    
    op_code[2]=1
    sixteen = False
        
    if instruction[1] not in memory_map and instruction[2] not in memory_map: # both are registers   
        mod_rm[0] = 1
        mod_rm[1] = 1  # for register
        
        register1 = instruction[1].lower()
        register2 = instruction[2].lower()
           
        if register1 in eight_bit_registers:
            op_code[6] = 0
            op_code[7] = 0  # 8 bit reg
        elif register1 in sixteen_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 16 bit reg
            sixteen = True
        
        elif register1 in thirty_two_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 32 bit reg

        if register1 in register_map and register2 in register_map:
            mod_rm[5:8] = register_map[register1]
            mod_rm[2:5] = register_map[register2]
            
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
            
        if sixteen:

            result = ('66 ' + op_code_hex + " " + mod_rm_hex)
            return result
        
        else:
            result = (op_code_hex + " " + mod_rm_hex)
            return result            
            
    elif instruction[1] in memory_map and (instruction[2] in thirty_two_bit_registers):
    # mem/reg
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling
        
        op_code[6] = 0
        
        register = instruction[2]
        memory = instruction[1]
        
        if memory in memory_map:
        
            mod_rm[5:8] = memory_map[memory]

            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      

        result = (op_code_hex + " " + mod_rm_hex)
        return result
                     
    elif instruction[2] in memory_map and (instruction[1] in thirty_two_bit_registers):
    # reg/mem
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling      
        op_code[6] = 1
        
        register = instruction[1]
        memory = instruction[2]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
               
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)
    
        result = (op_code_hex + " " + mod_rm_hex)
        return result                             

#####################################################
        
def Or(instruction, op_code, mod_rm):
    
    op_code[4]=1
    sixteen = False

    if instruction[1] not in memory_map and instruction[2] not in memory_map: # both are registers     
        mod_rm[0] = 1
        mod_rm[1] = 1  # for register
        
        register1 = instruction[1].lower()
        register2 = instruction[2].lower()
        
        
        if register1 in eight_bit_registers:
            op_code[6] = 0
            op_code[7] = 0  # 8 bit reg
        elif register1 in sixteen_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 16 bit reg
            sixteen = True
        
        elif register1 in thirty_two_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 32 bit reg

        if register1 in register_map and register2 in register_map:
            mod_rm[5:8] = register_map[register1]
            mod_rm[2:5] = register_map[register2]
            
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
            
        if sixteen:

            result = ('66 ' + op_code_hex + " " + mod_rm_hex)
            return result
        
        else:
            result = (op_code_hex + " " + mod_rm_hex)
            return result
        
            
    elif instruction[1] in memory_map and (instruction[2] in thirty_two_bit_registers):
    # mem/reg
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling
        
        op_code[6] = 0
        
        register = instruction[2]
        memory = instruction[1]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]

        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)
        
        result = (op_code_hex + " " + mod_rm_hex)
        return result       
                
    elif instruction[2] in memory_map and (instruction[1] in thirty_two_bit_registers):
    # reg/mem
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling       
        op_code[6] = 1
        
        register = instruction[1]
        memory = instruction[2]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                    
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
            
        result = (op_code_hex + " " + mod_rm_hex)
        return result            
                   
        
#####################################################
        

def Xor(instruction, op_code, mod_rm):
    sixteen = False
    
    op_code[2]=1
    op_code[3]=1
 
    if instruction[1] not in memory_map and instruction[2] not in memory_map: # both are registers 

     
        mod_rm[0] = 1
        mod_rm[1] = 1  # for register
        
        register1 = instruction[1].lower()
        register2 = instruction[2].lower()
        
        
        if register1 in eight_bit_registers:
            op_code[6] = 0
            op_code[7] = 0  # 8 bit reg
        elif register1 in sixteen_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 16 bit reg
            sixteen = True
        
        elif register1 in thirty_two_bit_registers:
            op_code[6] = 0
            op_code[7] = 1  # 32 bit reg

        if register1 in register_map and register2 in register_map:
            mod_rm[5:8] = register_map[register1]
            mod_rm[2:5] = register_map[register2]
            
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
            
        if sixteen:

            result = ('66 ' + op_code_hex + " " + mod_rm_hex)
            return result
        
        else:
            result = (op_code_hex + " " + mod_rm_hex)
            return result
        
            
    elif instruction[1] in memory_map and (instruction[2] in thirty_two_bit_registers):
    # mem/reg
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling
        
        op_code[6] = 0
        
        register = instruction[2]
        memory = instruction[1]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)           

        result = (op_code_hex + " " + mod_rm_hex)
        return result
                      
    elif instruction[2] in memory_map and (instruction[1] in thirty_two_bit_registers):
    # reg/mem
    
        mod_rm[0] = 0
        mod_rm[1] = 0  # for memory handling    
        op_code[6] = 1
        
        register = instruction[1]
        memory = instruction[2]
        
        if memory in memory_map:
            mod_rm[5:8] = memory_map[memory]
            if register in thirty_two_bit_registers:
                op_code[7] =1
                mod_rm [2:5] = register_map[register]
                    
        op_code_hex = hex(int(''.join(map(str, op_code)), 2))[2:].zfill(2)
        mod_rm_hex = hex(int(''.join(map(str, mod_rm)), 2))[2:].zfill(2)      
           
        result = (op_code_hex + " " + mod_rm_hex)
        return result            
                    
#####################################################
def inc(register):
    
    base_opcode = 0x40  # Base opcode 
    register = register.lower()
    
    if register in rd_rw_map:
        opcode = hex(base_opcode + rd_rw_map[register])
        opcode = opcode.replace('0x','')
    elif register in eight_bit_registers:
        
        opcode = 'fe ' + hex(int('11'  + '000' + str(register_map[register][0]) + str(register_map[register][1])+  str(register_map[register][2]),2))
        opcode = opcode.replace('0x','')

    return str(opcode)

#####################################################
def dec(register):
    
    base_opcode = 0x48  # Base opcode

    register = register.lower()
    
    if register in rd_rw_map:
        opcode = hex(base_opcode + rd_rw_map[register])
        opcode = opcode.replace('0x','')
    elif register in eight_bit_registers:
        
        opcode = 'fe ' + hex(int('11'  + '001' + str(register_map[register][0]) + str(register_map[register][1])+  str(register_map[register][2]),2))
        opcode = opcode.replace('0x','')

    return str(opcode)
 
#####################################################
     
def isImmediate(operand):
    for i in range(len(operand)):
        if (operand[i] >='0' and operand[i] <='9') or (operand[i]>='A' and operand[i] <= 'F') or (operand[i]>='a' and operand[i]<='f') or (i==len(operand)-1 and (operand[i] == 'h' or operand[i]=='H')):
            continue
        else:
            return False
    return True

def toLittleEndian32(operand):
    if (operand[-1] == 'h' or operand[-1]== 'H'):
        operand= operand[0:-1]

    val = "" + "0" * (8-len(operand)) + operand
    out = ""
    i=0
    while i < (len(val)):
        out = val[i]  + val[i+1] +" " + out
        i+=2
    return out

#####################################################

def push(value):
    sixteen = False
    result=''
    str=''
    base_opcode = 0x50

    value = value.lower()
    
    if value in rd_rw_map:
        
        opcode = hex(base_opcode + rd_rw_map[value])
        opcode = opcode.replace('0x','')
        return opcode
              
    #handling immediate
        
    elif(isImmediate(value)):
    
        if value[-1] == 'h' or value[-1] == 'H':
            value = value[:-1]
            if (int(value,16) < 2**8):
                result = "6A " + value
            elif (int(value,16) < 2**16):
                result = "68 " + toLittleEndian32(value)
            elif (int(value,16) < 2**32):
                result = "68 " + toLittleEndian32(value)
        elif value[-1] == 'b' or value[-1] == 'B':
                value = value[:-1]
                if (int(value,2) < 2**8):
                    result = "6A " + value
                elif (int(value,2) < 2**16):
                    result = "68 " + toLittleEndian32(value)
                elif (int(value,2) < 2**32):
                    result = "68 " + toLittleEndian32(value)
        elif value[-1] == 'd' or value[-1] == 'D':
            
            value = value[:-1]
            if (int(value,10) < 2**8):
                result = "6A " + value
            elif (int(value,10) < 2**16):
                result = "68 " + toLittleEndian32(value)
            elif (int(value,10) < 2**32):
                result = "68 " + toLittleEndian32(value)
        else:
            str = hex(int(value))[2:]
            if (len(hex(int(value))[2:])) == 1:
                str = "0" + hex(int(value))[2:]
            if (int(value) < 2**8):
                result = "6A " + str
            elif (int(value) < 2**16):
                result = "68 " + toLittleEndian32(str)
            elif (int(value) < 2**32):
                result = "68 " + toLittleEndian32(str)

    return (result)
    
#####################################################
        
def pop(register):
    
    base_opcode = 0x58 # Base opcode in decimal

    register = register.lower()
    
    if register in rd_rw_map:
        opcode = hex(base_opcode + rd_rw_map[register])
        opcode = opcode.replace('0x','')

    return str(opcode)

#####################################################
def  main2():
    inputFile = open("input_assembly.txt", "r")
    outputFile = open("output_assembly.txt", "w")

    op_code = [0] * 8
    mod_rm = [0] * 8
    address = 0x0000000000000000
    machine_code_lines = []
    opcode_str = ""

    labels = {}
    jumps = []
    idx = -1

    for line in inputFile:
        idx+=1
        line = line.rstrip()
        if line == '':
            continue
        
        inp = line.split(' ')
        if inp[0].endswith(':'):
            idx-=1
            label = inp[0][:-1]  # Remove :
            labels[label] = address  # Store the label and its address in the dictionary
            continue
        else:
            inp[1] = inp[1].replace(",", "")
            output_line = ""
            formatted_address = f'0x{address:016x}'
            output_line += formatted_address + '\t'

        
        if inp[0].lower() == 'jmp':
            
            if inp[1] in labels:  # Check if the jump target is a defined label
                jump_target_address = labels[inp[1]]
                if jump_target_address < address:  # Check if it's a backward jump
                  
                    jump_offset = jump_target_address - (address + 2)  # Calculate the jump offset
                    if jump_offset < 0:
                         jump_offset = 256 + jump_offset  
                    output_line += f'eb {jump_offset:02x}'  # backwardJump output
                address+=2
                
            else:  # It's a forward jump
            
                output_line += 'eb 00'  # a placeholder for the forward jump machine code
                jumps.append((idx,formatted_address, inp[1]))  # Store the jump line and label
                machine_code_lines.append(output_line)
                address+=2 
                continue   
        
        elif inp[0].lower() =="add":
            op_code = [0] * 8
            if inp[1] in sixteen_bit_registers:
                address+=3
            else:
                address=address + 2
            output_line+=(add(inp,op_code,mod_rm))
            output_text = '\n'.join(machine_code_lines)
            
            
        elif inp[0].lower() =="sub":
            op_code = [0] * 8
            if inp[1] in sixteen_bit_registers:
                address+=3
            else:
                address+=2
                
            output_line+=(sub(inp,op_code,mod_rm))
            output_text = '\n'.join(machine_code_lines)       
            
        elif inp[0].lower() =="and":
            op_code = [0] * 8
            if inp[1] in sixteen_bit_registers:
                address+=3
            else:
                address=address + 2
            output_line+=(And(inp,op_code,mod_rm))
            output_text = '\n'.join(machine_code_lines)
            
        elif inp[0].lower() =="or":
            op_code = [0] * 8
            if inp[1] in sixteen_bit_registers:
                address+=3
            else:
                address=address + 2
           
            output_line+=(Or(inp,op_code,mod_rm))
            output_text = '\n'.join(machine_code_lines)
            
        elif inp[0].lower() =="xor":
            op_code = [0] * 8
        
            if inp[1] in sixteen_bit_registers:
                address+=3
            else:
                address=address + 2
            output_line+=(Xor(inp,op_code,mod_rm))
            output_text = '\n'.join(machine_code_lines)
            
        elif inp[0].lower() =="inc":
            op_code = [0] * 8
            
            if inp[1] in sixteen_bit_registers:
                address+=2
            else:
                address=address + 1
            if inp[1] in sixteen_bit_registers:
                output_line+=('66 ')
                
            output_line+=(inc(inp[1]))
            output_text = '\n'.join(machine_code_lines)
            
        elif inp[0].lower() =="dec":
            op_code = [0] * 8

            if inp[1] in sixteen_bit_registers:
                address+=2
            else:
                address=address + 1
            if inp[1] in sixteen_bit_registers:
                output_line+=('66 ')
            output_line+=(dec(inp[1]))
            output_text = '\n'.join(machine_code_lines)
                        
        elif inp[0].lower() =="pop":
            op_code = [0] * 8
            if inp[1] in thirty_two_bit_registers:
                address+=2
            else:
                address=address + 1
            if inp[1] in sixteen_bit_registers:
                output_line+=('66 ')
            output_line+=(pop(inp[1]))
            output_text = '\n'.join(machine_code_lines)
                    
        elif inp[0].lower() =="push":
            value_avalie = inp[1]
            op_code = [0] * 8
            if inp[1] in sixteen_bit_registers:
                address+=2
            elif inp[1] in thirty_two_bit_registers:
                address=address + 1
            else:
                if (inp[1][-1] >'9' or inp[1][-1] <'0'):
                    inp[1] = inp[1][:-1]
                if int(inp[1],16)<= 255:
                    address+=2
                elif int(inp[1],16) >255:
                    address+=5
                   
            if inp[1] in sixteen_bit_registers:
                output_line+=('66 ')
            inp[1] = value_avalie
            output_line+=str(push(inp[1]))
            output_text = '\n'.join(machine_code_lines)
                  
        machine_code_lines.append(output_line)
        
    for line_index , jump_line, label in jumps:
        jump_target_address = labels[label]
       # line_index = int(jump_line, 16)
        jump_offset = jump_target_address - (int(jump_line, 16)+2) # to jump to the next line of the jmp instruction 

        # Two's complement
        jump_offset = (~(-jump_offset) + 1) & 0xFF
        formatted_hex_offset = f'{jump_offset:02x}' 
      
        # Replace the placeholder in the specific line and update the list
        machine_code_lines[line_index] = machine_code_lines[line_index].replace('eb 00', f'eb {formatted_hex_offset}')
        #print(machine_code_lines)

    # create the output text by joining all the elements from 'machine_code_lines'
        output_text = '\n'.join(machine_code_lines)
        
    for line in machine_code_lines:
        outputFile.write(output_text)
        print(line)

def main():
    try:
        get_input = int(input("how do you want to give the input? type 1 for typing your input , type 2 for giving a File\n"))
        if (get_input==1):
            print("enter your input:")
            while True:
                instruction = input()
                if instruction =='':
                    return
                inputFile = open("input_assembly.txt","w")
                print(instruction,file=inputFile)
                inputFile.close()
                main2()
                outputFile = open("output_assembly.txt","r")

                outputFile.close()
        elif(get_input==2):
            main2()
        else:
            print("invalid input")
    except:
        print("Error!")
        
main()
                    
                
                    
                    
                    
                    
                    
                    

     
    





