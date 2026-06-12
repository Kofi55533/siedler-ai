# Worker/Camp/Path Branch Matrix

- Binary: `C:\Users\marku\OneDrive\Desktop\Gold edition\bin\SettlersHoK.exe`
- Source CFG Generated: 2026-06-10T22:45:25.591802+00:00
- Generated: 2026-06-10T22:45:34.258549+00:00
- Selected functions: 130
- Anchor functions: 52
- Selected functions with conditional branches: 95
- Total conditional branches (selected): 215
- Switch candidates (selected): 0

## Functions

### 0x004cf6d6
- blocks=31, insns=235, edges=71, jcc=16, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - 0x004cf6e7: je | true=0x004cf8eb | false=0x004cf6ed
    predicate_hint: `0x004cf6e6: push edi`
  - 0x004cf6ee: je | true=0x004cf872 | false=0x004cf6f4
    predicate_hint: `0x004cf6ed: dec eax`
  - 0x004cf6f5: je | true=0x004cf7d3 | false=0x004cf6fb
    predicate_hint: `0x004cf6f4: dec eax`
  - 0x004cf6fc: je | true=0x004cf708 | false=0x004cf6fe
    predicate_hint: `0x004cf6fb: dec eax`
  - 0x004cf717: je | true=0x004cf790 | false=0x004cf719
    predicate_hint: `0x004cf70e: test al, al`
  - 0x004cf737: jle | true=0x004cf73c | false=0x004cf739
    predicate_hint: `0x004cf734: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf74a: jge | true=0x004cf74f | false=0x004cf74c
    predicate_hint: `0x004cf747: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf7ae: jle | true=0x004cf7b3 | false=0x004cf7b0
    predicate_hint: `0x004cf7ab: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf7c1: jge | true=0x004cf7c6 | false=0x004cf7c3
    predicate_hint: `0x004cf7be: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf7e2: je | true=0x004cf845 | false=0x004cf7e4
    predicate_hint: `0x004cf7d9: test al, al`
  - 0x004cf802: jle | true=0x004cf807 | false=0x004cf804
    predicate_hint: `0x004cf7ff: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf863: jle | true=0x004cf868 | false=0x004cf865
    predicate_hint: `0x004cf860: cmp dword ptr [esi + 0x14], eax`
  - 0x004cf879: je | true=0x004cf8c8 | false=0x004cf87b
    predicate_hint: `0x004cf877: test al, al`
  - 0x004cf8cc: jne | true=0x004cf8eb | false=0x004cf8ce
    predicate_hint: `0x004cf8c8: cmp byte ptr [esi + 0x3d], 0`

### 0x0057efde
- blocks=20, insns=235, edges=45, jcc=15, switch_indirect=0, truncated=False
- classes:
  - .?AVCBlockingStatusPredicate@EGL@@
  - .?AVCUnblockedInSectorPredicate@EGL@@
- branch conditions:
  - 0x0057efeb: jne | true=0x0057eff8 | false=0x0057efed
    predicate_hint: `0x0057efe9: test eax, eax`
  - 0x0057eff2: je | true=0x0057f1dc | false=0x0057eff8
    predicate_hint: `0x0057eff0: cmp dword ptr [ecx], eax`
  - 0x0057effe: je | true=0x0057f1db | false=0x0057f004
    predicate_hint: `0x0057effc: test esi, esi`
  - 0x0057f026: jge | true=0x0057f060 | false=0x0057f028
    predicate_hint: `0x0057f01b: cmp esi, 0xffa60000`
  - 0x0057f05e: jne | true=0x0057f043 | false=0x0057f060
    predicate_hint: `0x0057f05b: mov dword ptr [ebp - 0x14], ecx`
  - 0x0057f066: jle | true=0x0057f09f | false=0x0057f068
    predicate_hint: `0x0057f060: cmp esi, 0x5a0000`
  - 0x0057f09d: jne | true=0x0057f082 | false=0x0057f09f
    predicate_hint: `0x0057f09a: mov dword ptr [ebp - 0x14], ecx`
  - 0x0057f0a5: jge | true=0x0057f0d0 | false=0x0057f0a7
    predicate_hint: `0x0057f09f: test esi, esi`
  - 0x0057f124: jge | true=0x0057f152 | false=0x0057f126
    predicate_hint: `0x0057f122: test esi, esi`
  - 0x0057f18d: jle | true=0x0057f115 | false=0x0057f18f
    predicate_hint: `0x0057f186: cmp dword ptr [ebp - 4], 0x16`

### 0x0058024d
- blocks=11, insns=206, edges=34, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0058027d: jge | true=0x00580284 | false=0x0058027f
    predicate_hint: `0x0058027a: mov dword ptr [esi + 0x24], eax`
  - 0x0058028e: jge | true=0x00580294 | false=0x00580290
    predicate_hint: `0x0058028a: cmp ecx, ebx`
  - 0x00580305: je | true=0x0058034c | false=0x00580307
    predicate_hint: `0x00580300: cmp edi, ebx`
  - 0x00580309: jle | true=0x0058030f | false=0x0058030b
    predicate_hint: `0x00580307: mov eax, ecx`
  - 0x00580352: jl | true=0x005802ec | false=0x00580354
    predicate_hint: `0x0058034f: cmp ecx, 4`

### 0x0052390a
- blocks=13, insns=127, edges=49, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00523911: je | true=0x0052399f | false=0x00523917
    predicate_hint: `0x0052390d: cmp dword ptr [esi + 0x5c], 0`
  - 0x00523922: jne | true=0x00523930 | false=0x00523924
    predicate_hint: `0x00523920: test eax, eax`
  - 0x0052396a: je | true=0x0052397b | false=0x0052396c
    predicate_hint: `0x00523968: test al, al`
  - 0x005239a6: je | true=0x005239e7 | false=0x005239a8
    predicate_hint: `0x005239a4: test eax, eax`
  - 0x005239ca: je | true=0x005239e7 | false=0x005239cc
    predicate_hint: `0x005239c8: test eax, eax`
  - 0x005239db: je | true=0x005239e7 | false=0x005239dd
    predicate_hint: `0x005239d9: test eax, eax`
  - 0x005239ee: je | true=0x00523a03 | false=0x005239f0
    predicate_hint: `0x005239e7: cmp dword ptr [0x880ba4], 0`

### 0x00582db4
- blocks=12, insns=81, edges=31, jcc=8, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
  - .?AVCPath@GGL@@
- branch conditions:
  - 0x00582dd9: jne | true=0x00582de2 | false=0x00582ddb
    predicate_hint: `0x00582dd7: mov ecx, esi`
  - 0x00582dfb: je | true=0x00582e6b | false=0x00582dfd
    predicate_hint: `0x00582df9: test eax, eax`
  - 0x00582e07: je | true=0x00582e3f | false=0x00582e09
    predicate_hint: `0x00582e04: cmp eax, 1`
  - 0x00582e0d: je | true=0x00582e45 | false=0x00582e0f
    predicate_hint: `0x00582e09: cmp dword ptr [ebp + 0x10], 1`
  - 0x00582e28: jne | true=0x00582e6b | false=0x00582e2a
    predicate_hint: `0x00582e26: test al, al`
  - 0x00582e43: jne | true=0x00582e60 | false=0x00582e45
    predicate_hint: `0x00582e3f: cmp dword ptr [ebp + 0x10], 1`
  - 0x00582e5e: jne | true=0x00582e6b | false=0x00582e60
    predicate_hint: `0x00582e5c: test al, al`

### 0x00508b37
- blocks=12, insns=125, edges=34, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00508ba9: je | true=0x00508bf1 | false=0x00508bab
    predicate_hint: `0x00508ba4: test eax, eax`
  - 0x00508bae: jne | true=0x00508bdf | false=0x00508bb0
    predicate_hint: `0x00508bab: cmp eax, 1`
  - 0x00508bda: je | true=0x00508bf1 | false=0x00508bdc
    predicate_hint: `0x00508bd7: cmp ax, cx`
  - 0x00508c1f: jle | true=0x00508c62 | false=0x00508c21
    predicate_hint: `0x00508c1c: cmp eax, 1`
  - 0x00508c43: je | true=0x00508c62 | false=0x00508c45
    predicate_hint: `0x00508c3f: test al, al`
  - 0x00508c60: jne | true=0x00508c36 | false=0x00508c62
    predicate_hint: `0x00508c5e: cmp ecx, dword ptr [eax]`

### 0x0049c2a4
- blocks=11, insns=98, edges=30, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0049c2b2: je | true=0x0049c3bd | false=0x0049c2b8
    predicate_hint: `0x0049c2b0: test al, al`
  - 0x0049c2d6: je | true=0x0049c3bd | false=0x0049c2dc
    predicate_hint: `0x0049c2d4: test al, al`
  - 0x0049c2e6: je | true=0x0049c3bd | false=0x0049c2ec
    predicate_hint: `0x0049c2e4: test eax, eax`
  - 0x0049c2f7: je | true=0x0049c3bd | false=0x0049c2fd
    predicate_hint: `0x0049c2f4: test esi, esi`
  - 0x0049c308: je | true=0x0049c38f | false=0x0049c30e
    predicate_hint: `0x0049c305: test eax, eax`
  - 0x0049c31c: je | true=0x0049c3bd | false=0x0049c322
    predicate_hint: `0x0049c31a: test eax, eax`
  - 0x0049c332: je | true=0x0049c3bd | false=0x0049c338
    predicate_hint: `0x0049c32a: cmp byte ptr [edi + 0x13d], 0`
  - 0x0049c39b: je | true=0x0049c3bd | false=0x0049c39d
    predicate_hint: `0x0049c399: test eax, eax`

### 0x0057fee2
- blocks=11, insns=64, edges=21, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057fef8: jg | true=0x0057ff5a | false=0x0057fefa
    predicate_hint: `0x0057fef5: cmp dword ptr [ebp - 0xb], eax`
  - 0x0057ff0a: jg | true=0x0057ff53 | false=0x0057ff0c
    predicate_hint: `0x0057ff07: cmp dword ptr [ebp - 0xf], eax`
  - 0x0057ff28: je | true=0x0057ff2e | false=0x0057ff2a
    predicate_hint: `0x0057ff26: cmp eax, edi`
  - 0x0057ff51: jne | true=0x0057ff03 | false=0x0057ff53
    predicate_hint: `0x0057ff4f: test bl, bl`
  - 0x0057ff58: jne | true=0x0057fef2 | false=0x0057ff5a
    predicate_hint: `0x0057ff56: test bl, bl`

### 0x00589a1d
- blocks=9, insns=54, edges=14, jcc=7, switch_indirect=0, truncated=False
- classes:
  - .?AVCAStar64Normal@EGL@@
- branch conditions:
  - 0x00589a3f: jg | true=0x00589a72 | false=0x00589a41
    predicate_hint: `0x00589a3c: mov dword ptr [ebp - 4], edx`
  - 0x00589a48: jge | true=0x00589a55 | false=0x00589a4a
    predicate_hint: `0x00589a45: cmp esi, dword ptr [ebp + 8]`
  - 0x00589a52: jbe | true=0x00589a55 | false=0x00589a54
    predicate_hint: `0x00589a4e: cmp edx, dword ptr [ecx + esi*8 + 0xc]`
  - 0x00589a5b: jbe | true=0x00589a71 | false=0x00589a5d
    predicate_hint: `0x00589a59: cmp edi, dword ptr [edx]`
  - 0x00589a6f: jle | true=0x00589a42 | false=0x00589a71
    predicate_hint: `0x00589a6d: mov eax, esi`

### 0x0052b39d
- blocks=7, insns=101, edges=23, jcc=5, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
  - .?AVCCamperBehavior@GGL@@
  - .?AVCWorkerAlarmModeBehavior@GGL@@
  - .?AVCWorkerBehavior@GGL@@
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - 0x0052b3ce: jle | true=0x0052b476 | false=0x0052b3d4
    predicate_hint: `0x0052b3cb: cmp dword ptr [ebp + 8], ebx`
  - 0x0052b425: je | true=0x0052b44c | false=0x0052b427
    predicate_hint: `0x0052b424: dec eax`
  - 0x0052b428: jne | true=0x0052b46c | false=0x0052b42a
    predicate_hint: `0x0052b427: dec eax`
  - 0x0052b470: jl | true=0x0052b3d4 | false=0x0052b476
    predicate_hint: `0x0052b46d: cmp ebx, dword ptr [ebp + 8]`

### 0x00577edf
- blocks=10, insns=76, edges=16, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00577f31: jle | true=0x00577f3f | false=0x00577f33
    predicate_hint: `0x00577f2b: cmp dword ptr [ebp + 0xc], 0x1f`
  - 0x00577f4c: je | true=0x00577f6d | false=0x00577f4e
    predicate_hint: `0x00577f4a: mov eax, edi`
  - 0x00577f54: jne | true=0x00577f17 | false=0x00577f56
    predicate_hint: `0x00577f4e: cmp esi, dword ptr [0x897620]`
  - 0x00577f5a: jle | true=0x00577f63 | false=0x00577f5c
    predicate_hint: `0x00577f56: cmp dword ptr [ebx + 0xc], 2`

### 0x004d2925
- blocks=7, insns=48, edges=15, jcc=4, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehavior@GGL@@
- branch conditions:
  - 0x004d292c: jne | true=0x004d2995 | false=0x004d292e
    predicate_hint: `0x004d2928: cmp dword ptr [edi + 0x44], 9`
  - 0x004d2942: jne | true=0x004d2995 | false=0x004d2944
    predicate_hint: `0x004d2940: test eax, eax`
  - 0x004d2954: je | true=0x004d2994 | false=0x004d2956
    predicate_hint: `0x004d2952: test ebx, ebx`
  - 0x004d2964: je | true=0x004d2994 | false=0x004d2966
    predicate_hint: `0x004d2962: test al, al`

### 0x005232f2
- blocks=8, insns=75, edges=13, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005232fe: je | true=0x00523360 | false=0x00523300
    predicate_hint: `0x005232fa: cmp dword ptr [edi + 0x18], 0`
  - 0x0052331a: je | true=0x0052335f | false=0x0052331c
    predicate_hint: `0x00523318: test eax, eax`
  - 0x00523321: je | true=0x0052334b | false=0x00523323
    predicate_hint: `0x0052331f: test eax, eax`
  - 0x0052333f: je | true=0x0052335f | false=0x00523341
    predicate_hint: `0x0052333d: test al, al`

### 0x004cfc94
- blocks=7, insns=55, edges=16, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cfc9e: jne | true=0x004cfcfa | false=0x004cfca0
    predicate_hint: `0x004cfc9c: test al, al`
  - 0x004cfca9: je | true=0x004cfcfa | false=0x004cfcab
    predicate_hint: `0x004cfca7: test al, al`
  - 0x004cfcc1: je | true=0x004cfcfa | false=0x004cfcc3
    predicate_hint: `0x004cfcbf: test eax, eax`
  - 0x004cfcd4: je | true=0x004cfcf9 | false=0x004cfcd6
    predicate_hint: `0x004cfcd2: test esi, esi`

### 0x004cb80b
- blocks=6, insns=122, edges=17, jcc=3, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - 0x004cb896: jne | true=0x004cb852 | false=0x004cb898
    predicate_hint: `0x004cb894: test al, al`
  - 0x004cb927: jne | true=0x004cb934 | false=0x004cb929
    predicate_hint: `0x004cb925: test al, al`

### 0x004d34c9
- blocks=5, insns=53, edges=15, jcc=3, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehavior@GGL@@
- branch conditions:
  - 0x004d34d8: jne | true=0x004d34e1 | false=0x004d34da
    predicate_hint: `0x004d34d6: test al, al`
  - 0x004d34ff: jne | true=0x004d351d | false=0x004d3501
    predicate_hint: `0x004d34fd: test eax, eax`

### 0x005803cf
- blocks=4, insns=135, edges=24, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0058041a: je | true=0x005804b6 | false=0x00580420
    predicate_hint: `0x00580415: cmp edi, ecx`
  - 0x005804b0: jne | true=0x00580426 | false=0x005804b6
    predicate_hint: `0x005804ad: cmp edi, dword ptr [ebp - 0x1c]`

### 0x0058bbce
- blocks=6, insns=93, edges=10, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0058bbf7: je | true=0x0058bc68 | false=0x0058bbf9
    predicate_hint: `0x0058bbf5: cmp esi, ebx`
  - 0x0058bc14: je | true=0x0058bc68 | false=0x0058bc16
    predicate_hint: `0x0058bc11: cmp byte ptr [eax + esi*8], cl`
  - 0x0058bc20: jne | true=0x0058bc2a | false=0x0058bc22
    predicate_hint: `0x0058bc16: test cl, cl`

### 0x004cfacf
- blocks=7, insns=90, edges=15, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cfad9: jne | true=0x004cfb75 | false=0x004cfadf
    predicate_hint: `0x004cfad7: test al, al`
  - 0x004cfb46: jne | true=0x004cfb73 | false=0x004cfb48
    predicate_hint: `0x004cfb43: test ah, 0x41`
  - 0x004cfb56: jnp | true=0x004cfb5b | false=0x004cfb58
    predicate_hint: `0x004cfb50: test ah, 5`

### 0x004cfc0a
- blocks=6, insns=71, edges=18, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cfc14: jne | true=0x004cfc76 | false=0x004cfc16
    predicate_hint: `0x004cfc12: test al, al`
  - 0x004cfc1f: je | true=0x004cfc76 | false=0x004cfc21
    predicate_hint: `0x004cfc1d: test al, al`
  - 0x004cfc3a: je | true=0x004cfc52 | false=0x004cfc3c
    predicate_hint: `0x004cfc38: test esi, esi`

### 0x004cfb89
- blocks=5, insns=43, edges=9, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cfb93: jne | true=0x004cfbec | false=0x004cfb95
    predicate_hint: `0x004cfb91: test al, al`
  - 0x004cfba3: jne | true=0x004cfbec | false=0x004cfba5
    predicate_hint: `0x004cfba0: test ah, 0x41`
  - 0x004cfbac: je | true=0x004cfbec | false=0x004cfbae
    predicate_hint: `0x004cfba8: cmp dword ptr [eax + 0x64], 0`

### 0x004cbb29
- blocks=6, insns=43, edges=12, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cbb3b: je | true=0x004cbb7c | false=0x004cbb3d
    predicate_hint: `0x004cbb39: test esi, esi`
  - 0x004cbb4e: je | true=0x004cbb7b | false=0x004cbb50
    predicate_hint: `0x004cbb4c: test al, al`
  - 0x004cbb5a: je | true=0x004cbb7b | false=0x004cbb5c
    predicate_hint: `0x004cbb58: test eax, eax`

### 0x00579631
- blocks=4, insns=49, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00579643: je | true=0x0057969d | false=0x00579645
    predicate_hint: `0x00579641: test al, al`
  - 0x0057966a: je | true=0x0057969d | false=0x0057966c
    predicate_hint: `0x00579668: test al, al`

### 0x0050256d
- blocks=4, insns=48, edges=12, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0050258d: je | true=0x005025c8 | false=0x0050258f
    predicate_hint: `0x00502588: test eax, eax`
  - 0x00502598: je | true=0x005025c8 | false=0x0050259a
    predicate_hint: `0x00502595: test eax, eax`

### 0x004d0062
- blocks=6, insns=46, edges=11, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004d006c: je | true=0x004d0072 | false=0x004d006e
    predicate_hint: `0x004d006a: test al, al`
  - 0x004d009e: jne | true=0x004d00b1 | false=0x004d00a0
    predicate_hint: `0x004d009a: cmp dword ptr [ebp - 0x10], 0`

### 0x00500212
- blocks=4, insns=36, edges=6, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0050021f: jne | true=0x0050024f | false=0x00500221
    predicate_hint: `0x0050021c: cmp eax, dword ptr [edi + 8]`
  - 0x0050022a: jne | true=0x0050024f | false=0x0050022c
    predicate_hint: `0x00500224: cmp eax, dword ptr [0x877504]`

### 0x004cf5c3
- blocks=5, insns=32, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cf5ca: jne | true=0x004cf613 | false=0x004cf5cc
    predicate_hint: `0x004cf5c6: cmp byte ptr [edi + 0x3d], 0`
  - 0x004cf5fb: je | true=0x004cf612 | false=0x004cf5fd
    predicate_hint: `0x004cf5f9: test al, al`

### 0x00551b7b
- blocks=4, insns=25, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00551b83: jne | true=0x00551b8b | false=0x00551b85
    predicate_hint: `0x00551b7f: cmp dword ptr [ebp + 0xc], 0`
  - 0x00551b89: jbe | true=0x00551bb5 | false=0x00551b8b
    predicate_hint: `0x00551b85: cmp dword ptr [ebp + 0x10], 0`

### 0x0057f2e1
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCBlockingStatusPredicate@EGL@@
  - .?AVCBuildBlockedOnlyPredicate@?A0xfc60cb98@GGL@@
  - .?AVCPotentialCampSitePredicate@GGL@@
  - .?AVCUnblockedInLargeSectorPredicate@EGL@@
  - .?AVCUnblockedInSectorPredicate@EGL@@
- branch conditions:
  - 0x0057f2ee: je | true=0x0057f2f7 | false=0x0057f2f0
    predicate_hint: `0x0057f2e9: test byte ptr [esp + 8], 1`

### 0x004e3340
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehavior@GGL@@
  - .?AVCWorkerAlarmModeBehavior@GGL@@
  - .?AVCWorkerBehavior@GGL@@
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - 0x004e334d: je | true=0x004e3356 | false=0x004e334f
    predicate_hint: `0x004e3348: test byte ptr [esp + 8], 1`

### 0x004da815
- blocks=3, insns=219, edges=8, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - IsPathingUsed
  - NextWayPoint
  - NextWaypointOrientation
- branch conditions:
  - 0x004da822: jne | true=0x004dab1f | false=0x004da828
    predicate_hint: `0x004da81b: test byte ptr [0x86e8a8], 1`

### 0x004e5c2c
- blocks=3, insns=130, edges=2, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - MaximumDistanceWorkerToFarm
  - MaximumDistanceWorkerToResidence
  - ReAttachWorkerFrequency
- branch conditions:
  - 0x004e5c39: jne | true=0x004e5de9 | false=0x004e5c3f
    predicate_hint: `0x004e5c32: test byte ptr [0x871d88], 1`

### 0x004e3324
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - 0x004e3331: je | true=0x004e333a | false=0x004e3333
    predicate_hint: `0x004e332c: test byte ptr [esp + 8], 1`

### 0x004a71d5
- blocks=3, insns=395, edges=14, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - BlockingArea
  - NumBlockedPoints
- branch conditions:
  - 0x004a71e2: jne | true=0x004a7785 | false=0x004a71e8
    predicate_hint: `0x004a71db: test byte ptr [0x85e170], 1`

### 0x004dab46
- blocks=3, insns=128, edges=4, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - WayPoints
  - WaypointsCount
- branch conditions:
  - 0x004dab53: jne | true=0x004dad0a | false=0x004dab59
    predicate_hint: `0x004dab4c: test byte ptr [0x86e9f0], 1`

### 0x004dad86
- blocks=3, insns=92, edges=7, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - CoarsePath
  - FinePath
- branch conditions:
  - 0x004dad93: jne | true=0x004daea1 | false=0x004dad99
    predicate_hint: `0x004dad8c: test byte ptr [0x86eb20], 1`

### 0x00500a1d
- blocks=3, insns=44, edges=10, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - 0x00500a34: je | true=0x00500a80 | false=0x00500a36
    predicate_hint: `0x00500a32: test eax, eax`

### 0x004ffe1f
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - 0x004ffe22: jne | true=0x004ffe2e | false=0x004ffe24
    predicate_hint: `0x004ffe20: mov edi, ecx`

### 0x004fff0d
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCPotentialCampSitePredicate@GGL@@
- branch conditions:
  - 0x004fff1a: je | true=0x004fff23 | false=0x004fff1c
    predicate_hint: `0x004fff15: test byte ptr [esp + 8], 1`

### 0x004b7c82
- blocks=3, insns=412, edges=14, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - 0x004b7c8f: jne | true=0x004b825f | false=0x004b7c95
    predicate_hint: `0x004b7c88: test byte ptr [0x862d34], 1`

### 0x004af71e
- blocks=3, insns=273, edges=9, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - 0x004af72b: jne | true=0x004afaf0 | false=0x004af731
    predicate_hint: `0x004af724: test byte ptr [0x85fc30], 1`

### 0x004cbbbf
- blocks=3, insns=53, edges=6, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - 0x004cbbcc: jne | true=0x004cbc59 | false=0x004cbbd2
    predicate_hint: `0x004cbbc5: test byte ptr [0x86a824], 1`

### 0x00516ab2
- blocks=3, insns=44, edges=5, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - WayPoints
- branch conditions:
  - 0x00516abf: jne | true=0x00516b33 | false=0x00516ac1
    predicate_hint: `0x00516ab8: test byte ptr [0x87e1f8], 1`

### 0x004daf1d
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
- branch conditions:
  - 0x004daf20: jne | true=0x004daf2c | false=0x004daf22
    predicate_hint: `0x004daf1e: mov edi, ecx`

### 0x0058051f
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedBuildingAreasPredicate@EGL@@
- branch conditions:
  - 0x0058052c: je | true=0x00580535 | false=0x0058052e
    predicate_hint: `0x00580527: test byte ptr [esp + 8], 1`

### 0x0057fe7c
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedAreasPredicate@EGL@@
- branch conditions:
  - 0x0057fe89: je | true=0x0057fe92 | false=0x0057fe8b
    predicate_hint: `0x0057fe84: test byte ptr [esp + 8], 1`

### 0x00508a9b
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCoarsePath@EGL@@
- branch conditions:
  - 0x00508aa8: je | true=0x00508ab1 | false=0x00508aaa
    predicate_hint: `0x00508aa3: test byte ptr [esp + 8], 1`

### 0x00500cea
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - 0x00500cf7: je | true=0x00500d00 | false=0x00500cf9
    predicate_hint: `0x00500cf2: test byte ptr [esp + 8], 1`

### 0x00500c65
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
- branch conditions:
  - 0x00500c72: je | true=0x00500c7b | false=0x00500c74
    predicate_hint: `0x00500c6d: test byte ptr [esp + 8], 1`

### 0x005000d8
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampWithFreeSlotPredicate@GGL@@
- branch conditions:
  - 0x005000e5: je | true=0x005000ee | false=0x005000e7
    predicate_hint: `0x005000e0: test byte ptr [esp + 8], 1`

### 0x004e3278
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampWithFreeSlotPredicate@GGL@@
- branch conditions:
  - 0x004e3285: je | true=0x004e328e | false=0x004e3287
    predicate_hint: `0x004e3280: test byte ptr [esp + 8], 1`

### 0x004daf73
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
  - .?AVCPath@GGL@@
- branch conditions:
  - 0x004daf80: je | true=0x004daf89 | false=0x004daf82
    predicate_hint: `0x004daf7b: test byte ptr [esp + 8], 1`

### 0x0074a162
- blocks=3, insns=12, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- branch conditions:
  - 0x0074a16e: jecxz | true=0x0074a16f | false=0x0074a170
    predicate_hint: `0x0074a168: xchg byte ptr [esi + 0x7eb4e800], al`

### 0x0074a12e
- blocks=3, insns=12, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS
- branch conditions:
  - 0x0074a13a: jecxz | true=0x0074a13b | false=0x0074a13c
    predicate_hint: `0x0074a134: xchg byte ptr [esi + 0x7ee8e800], al`

### 0x0074a148
- blocks=3, insns=11, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- branch conditions:
  - 0x0074a154: jecxz | true=0x0074a155 | false=0x0074a156
    predicate_hint: `0x0074a14e: xchg byte ptr [esi + 0x7ecee800], al`

### 0x0074a0ac
- blocks=2, insns=5, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHANGE_WORK_TIME_CAMP
- branch conditions:
  - 0x0074a0ae: ja | true=0x0074a0b0 | false=0x0074a0b0
    predicate_hint: `0x0074a0ac: and al, 0x1d`

### 0x00749ba8
- blocks=2, insns=5, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_GO_TO_CAMP
- branch conditions:
  - 0x00749baa: ja | true=0x00749bac | false=0x00749bac
    predicate_hint: `0x00749ba8: mov byte ptr [edi], dl`

### 0x00749a38
- blocks=2, insns=5, edges=3, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_GO_TO_BLOCKED_PILE
- branch conditions:
  - 0x00749a3a: ja | true=0x00749a3c | false=0x00749a3c
    predicate_hint: `0x00749a38: cmp al, 0x16`

### 0x004b208c
- blocks=3, insns=1164, edges=26, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - WorkTimeBase
  - WorkTimeThresholdCampFire
  - WorkTimeThresholdFarm
  - WorkTimeThresholdResidence
  - WorkTimeThresholdWork
  - WorkerFlightDistance
- branch conditions:
  - 0x004b2099: jne | true=0x004b30d8 | false=0x004b209f
    predicate_hint: `0x004b2092: test byte ptr [0x8614f0], 1`

### 0x004a7e8d
- blocks=3, insns=379, edges=24, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004a7e9a: jne | true=0x004a8406 | false=0x004a7ea0
    predicate_hint: `0x004a7e93: test byte ptr [0x85e5e4], 1`

### 0x0051254c
- blocks=3, insns=142, edges=8, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00512559: jne | true=0x00512725 | false=0x0051255f
    predicate_hint: `0x00512552: test byte ptr [0x87c73c], 1`

### 0x004b8a24
- blocks=3, insns=138, edges=13, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004b8a31: jne | true=0x004b8c04 | false=0x004b8a37
    predicate_hint: `0x004b8a2a: test byte ptr [0x863724], 1`

### 0x004c7e91
- blocks=4, insns=104, edges=15, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004c7f5b: je | true=0x004c7f76 | false=0x004c7f5d
    predicate_hint: `0x004c7f55: test ecx, ecx`

### 0x004fa7ec
- blocks=3, insns=93, edges=10, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004fa7f9: jne | true=0x004fa915 | false=0x004fa7ff
    predicate_hint: `0x004fa7f2: test byte ptr [0x875e80], 1`

### 0x00516b3a
- blocks=3, insns=71, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00516b47: jne | true=0x00516c16 | false=0x00516b4d
    predicate_hint: `0x00516b40: test byte ptr [0x87e290], 1`

### 0x004ae78f
- blocks=3, insns=70, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004ae79c: jne | true=0x004ae87e | false=0x004ae7a2
    predicate_hint: `0x004ae795: test byte ptr [0x85f580], 1`

### 0x004b9179
- blocks=3, insns=53, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004b9186: jne | true=0x004b9216 | false=0x004b918c
    predicate_hint: `0x004b917f: test byte ptr [0x8638c4], 1`

### 0x00508dbc
- blocks=4, insns=36, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00508dd3: jle | true=0x00508de1 | false=0x00508dd5
    predicate_hint: `0x00508dcf: test esi, esi`

### 0x0057fe98
- blocks=4, insns=31, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057feb4: jae | true=0x0057fec5 | false=0x0057feb6
    predicate_hint: `0x0057fead: cmp edi, eax`

### 0x004d0130
- blocks=3, insns=30, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004d013a: jne | true=0x004d0169 | false=0x004d013c
    predicate_hint: `0x004d0138: test al, al`

### 0x004d00e2
- blocks=3, insns=27, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004d00ec: jne | true=0x004d0112 | false=0x004d00ee
    predicate_hint: `0x004d00ea: test al, al`

### 0x005b9756
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005b9759: jne | true=0x005b9765 | false=0x005b975b
    predicate_hint: `0x005b9757: mov edi, ecx`

### 0x00582e8f
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00582e92: jne | true=0x00582e9e | false=0x00582e94
    predicate_hint: `0x00582e90: mov edi, ecx`

### 0x00516dab
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00516dae: jne | true=0x00516dba | false=0x00516db0
    predicate_hint: `0x00516dac: mov edi, ecx`

### 0x00512734
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00512737: jne | true=0x00512743 | false=0x00512739
    predicate_hint: `0x00512735: mov edi, ecx`

### 0x00509274
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00509277: jne | true=0x00509283 | false=0x00509279
    predicate_hint: `0x00509275: mov edi, ecx`

### 0x0050443c
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0050443f: jne | true=0x0050444b | false=0x00504441
    predicate_hint: `0x0050443d: mov edi, ecx`

### 0x004fa924
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004fa927: jne | true=0x004fa933 | false=0x004fa929
    predicate_hint: `0x004fa925: mov edi, ecx`

### 0x004cbe29
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cbe2c: jne | true=0x004cbe38 | false=0x004cbe2e
    predicate_hint: `0x004cbe2a: mov edi, ecx`

### 0x004c7d64
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004c7d67: jne | true=0x004c7d73 | false=0x004c7d69
    predicate_hint: `0x004c7d65: mov edi, ecx`

### 0x004b9225
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004b9228: jne | true=0x004b9234 | false=0x004b922a
    predicate_hint: `0x004b9226: mov edi, ecx`

### 0x004b826e
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004b8271: jne | true=0x004b827d | false=0x004b8273
    predicate_hint: `0x004b826f: mov edi, ecx`

### 0x004b30e7
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004b30ea: jne | true=0x004b30f6 | false=0x004b30ec
    predicate_hint: `0x004b30e8: mov edi, ecx`

### 0x004afaff
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004afb02: jne | true=0x004afb0e | false=0x004afb04
    predicate_hint: `0x004afb00: mov edi, ecx`

### 0x004a85a1
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004a85a4: jne | true=0x004a85b0 | false=0x004a85a6
    predicate_hint: `0x004a85a2: mov edi, ecx`

### 0x004e5df7
- blocks=3, insns=19, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004e5dfa: jne | true=0x004e5e06 | false=0x004e5dfc
    predicate_hint: `0x004e5df8: mov esi, ecx`

### 0x004cfa6f
- blocks=3, insns=15, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004cfa7b: jne | true=0x004cfa84 | false=0x004cfa7d
    predicate_hint: `0x004cfa77: cmp byte ptr [esi + 0x3d], 0`

### 0x00553468
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00553475: je | true=0x0055347e | false=0x00553477
    predicate_hint: `0x00553470: test byte ptr [esp + 8], 1`

### 0x005516e5
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005516f2: je | true=0x005516fb | false=0x005516f4
    predicate_hint: `0x005516ed: test byte ptr [esp + 8], 1`

### 0x0055128b
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00551298: je | true=0x005512a1 | false=0x0055129a
    predicate_hint: `0x00551293: test byte ptr [esp + 8], 1`

### 0x00509d91
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00509d9e: je | true=0x00509da7 | false=0x00509da0
    predicate_hint: `0x00509d99: test byte ptr [esp + 8], 1`

### 0x004eab0b
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004eab18: je | true=0x004eab21 | false=0x004eab1a
    predicate_hint: `0x004eab13: test byte ptr [esp + 8], 1`

### 0x004dc8ec
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x004dc8f9: je | true=0x004dc902 | false=0x004dc8fb
    predicate_hint: `0x004dc8f4: test byte ptr [esp + 8], 1`

### 0x004daf9f
- blocks=3, insns=14, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@GGL@@
- branch conditions:
  - 0x004dafac: je | true=0x004dafb5 | false=0x004dafae
    predicate_hint: `0x004dafa7: test byte ptr [esp + 8], 1`

### 0x00570fd5
- blocks=3, insns=12, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00570fdc: jne | true=0x00570fe6 | false=0x00570fde
    predicate_hint: `0x00570fd8: cmp dword ptr [esi + 0x14], 0`

### 0x00553339
- blocks=1, insns=16, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
  - .?AVCCampBehaviorProperties@GGL@@
  - .?AVCCamperBehavior@GGL@@
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCPath@EGL@@
  - .?AVCPath@GGL@@
  - .?AVCWorkerAlarmModeBehavior@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerBehavior@GGL@@
  - .?AVCWorkerBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehavior@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00550ff0
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x004d41db
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x004cc9c4
- blocks=1, insns=38, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x004cc478
- blocks=1, insns=23, edges=5, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - none

### 0x00500c1e
- blocks=1, insns=16, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
- branch conditions:
  - none

### 0x0057fa63
- blocks=1, insns=12, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedAreasPredicate@EGL@@
- branch conditions:
  - none

### 0x004d02f3
- blocks=1, insns=11, edges=2, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - none

### 0x00500c81
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - none

### 0x004ffee5
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehaviorProperties@GGL@@
- branch conditions:
  - none

### 0x004d2e3f
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x004cba77
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00500d06
- blocks=1, insns=8, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - none

### 0x0057fed8
- blocks=1, insns=5, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedBuildingAreasPredicate@EGL@@
- branch conditions:
  - none

### 0x004e32d2
- blocks=1, insns=26, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004dbbb4
- blocks=1, insns=25, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004f2a63
- blocks=1, insns=17, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004fe0eb
- blocks=1, insns=16, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00513221
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004fc624
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004f0942
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004e5ee1
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004db298
- blocks=1, insns=14, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004d6b26
- blocks=1, insns=12, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0050122b
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004fd227
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004f32ef
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004d4208
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004fe926
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004e3f31
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0057fa9f
- blocks=1, insns=8, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00509d77
- blocks=1, insns=7, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004eaaf1
- blocks=1, insns=7, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004dc8d2
- blocks=1, insns=7, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x004da5e9
- blocks=1, insns=7, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

## Limits

- Static CFG only; no runtime traces.
- Function boundaries and call-chain context are heuristic.
- Predicate hints are inferred from nearby disassembly text.
