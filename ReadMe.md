# Assembler_x86

In the first phase of the project, we generated a machine code for each instruction in the code segment. It supports add,sub,and,or,xor,push,pop,inc,dec and jmp. It also shows the address of each instruction.

In the second phase, we should display the memory and how the machine codes are placed in the memory. It also shows how stack segment, data segment and code segment are filled. There is a microcontroller which consists of 256 bytes of memory. Each segment has 32 bytes. 

---

 the input format is shown below: 

```python
.stack(160)

.data(90)

myByte Byte
myWord Word
Mydword dword

.code(40)

Add ebx, ecx
Push edx
Push 11
Push 12345
Push ecx
Sub ecx, ecx
Pop eax
Push ax
```

The number in the () in front of each segment shows where the segment starts.

- for filling the stack segment: whenever we push or pop, the stack segment changes. if a register is pushed, based on the size of the register, the stack is filled with the name of the reg. if the reg is 4 bytes, it will fill the stack with the name 4 times. if 2 bytes,it will fill it with the name 2times and etc. if an immediate is pushed, based on its size, it fills the segment with num8, num16 or num32.
- for filling the code segment: we use the machine codes generated in phase 1 and place them little endian in the segment.
- for filling the data segment: based on the size of the data, it occupies some bytes of memory. if a word, it gets 2 bytes and etc.

Bytes not used in a segment are filled with 'MM'. Bytes which are not in any segment are filled with 'XX’
