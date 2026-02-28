# Worker/Camp/Path Branch Matrix

- Binary: `C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\theSettlers5\bin\SettlersHoK.exe`
- Source CFG Generated: 2026-02-11T20:08:00.465437+00:00
- Generated: 2026-02-11T20:17:34.658836+00:00
- Selected functions: 405
- Anchor functions: 65
- Selected functions with conditional branches: 327
- Total conditional branches (selected): 2015
- Switch candidates (selected): 1

## Functions

### 0x0086da60
- blocks=161, insns=1851, edges=402, jcc=121, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0086da9e: je | true=0x0086dae6 | false=0x0086daa0
    predicate_hint: `0x0086da94: test byte ptr [ebx + 6], 1`
  - 0x0086daa4: je | true=0x0086dac9 | false=0x0086daa6
    predicate_hint: `0x0086daa0: test byte ptr [ebx + 5], 1`
  - 0x0086dafe: jne | true=0x0086de9e | false=0x0086db04
    predicate_hint: `0x0086dafc: cmp al, 0xa`
  - 0x0086db0a: je | true=0x0086dc77 | false=0x0086db10
    predicate_hint: `0x0086db07: cmp edx, -1`
  - 0x0086db13: je | true=0x0086db1d | false=0x0086db15
    predicate_hint: `0x0086db10: test cl, 2`
  - 0x0086db22: jne | true=0x0086dc77 | false=0x0086db28
    predicate_hint: `0x0086db20: cmp edx, eax`
  - 0x0086db39: je | true=0x0086dd02 | false=0x0086db3f
    predicate_hint: `0x0086db37: test al, al`
  - 0x0086db44: jne | true=0x0086dba6 | false=0x0086db46
    predicate_hint: `0x0086db42: test al, 0x40`
  - 0x0086db66: je | true=0x0086dc2c | false=0x0086db6c
    predicate_hint: `0x0086db64: test edi, edi`
  - 0x0086dbaa: je | true=0x0086dd02 | false=0x0086dbb0
    predicate_hint: `0x0086dba6: test byte ptr [ebx + 6], 8`
  - 0x0086dbbb: je | true=0x0086dd02 | false=0x0086dbc1
    predicate_hint: `0x0086dbb9: test al, al`
  - 0x0086dbd2: je | true=0x0086dd02 | false=0x0086dbd8
    predicate_hint: `0x0086dbd0: test al, al`
  - 0x0086dbf3: je | true=0x0086dc2c | false=0x0086dbf5
    predicate_hint: `0x0086dbf1: test edi, edi`
  - 0x0086dc88: je | true=0x0086dd02 | false=0x0086dc8a
    predicate_hint: `0x0086dc86: test al, al`
  - 0x0086dc95: je | true=0x0086dd02 | false=0x0086dc97
    predicate_hint: `0x0086dc93: test al, al`
  - 0x0086dc9c: jae | true=0x0086dcf6 | false=0x0086dc9e
    predicate_hint: `0x0086dc9a: cmp al, 0x80`
  - 0x0086dca4: je | true=0x0086dd02 | false=0x0086dca6
    predicate_hint: `0x0086dca1: test cl, 8`
  - 0x0086dca9: jae | true=0x0086dd02 | false=0x0086dcab
    predicate_hint: `0x0086dca6: cmp cl, 0x80`
  - 0x0086dcad: je | true=0x0086dcb7 | false=0x0086dcaf
    predicate_hint: `0x0086dcab: test al, 2`
  - 0x0086dccc: je | true=0x0086dcf6 | false=0x0086dcce
    predicate_hint: `0x0086dcca: test eax, eax`
  - 0x0086dd08: je | true=0x0086dd23 | false=0x0086dd0a
    predicate_hint: `0x0086dd05: cmp ecx, -1`
  - 0x0086dd0e: je | true=0x0086dd18 | false=0x0086dd10
    predicate_hint: `0x0086dd0a: test byte ptr [ebx + 4], 2`
  - 0x0086dd1d: je | true=0x0086de9e | false=0x0086dd23
    predicate_hint: `0x0086dd1b: cmp ecx, eax`
  - 0x0086dd34: jb | true=0x0086dea1 | false=0x0086dd3a
    predicate_hint: `0x0086dd32: cmp edi, ecx`
  - 0x0086dd3d: ja | true=0x0086dd47 | false=0x0086dd3f
    predicate_hint: `0x0086dd3a: mov edi, dword ptr [ebp - 0x50]`
  - 0x0086dd41: jbe | true=0x0086de9e | false=0x0086dd47
    predicate_hint: `0x0086dd3f: cmp edi, eax`
  - 0x0086dd49: jne | true=0x0086dd53 | false=0x0086dd4b
    predicate_hint: `0x0086dd47: test ecx, ecx`
  - 0x0086dd4d: je | true=0x0086de9e | false=0x0086dd53
    predicate_hint: `0x0086dd4b: test eax, eax`
  - 0x0086dd5a: jbe | true=0x0086ddc7 | false=0x0086dd5c
    predicate_hint: `0x0086dd53: cmp dword ptr [ebx + 0x1cc], 0`
  - 0x0086dd68: je | true=0x0086dda0 | false=0x0086dd6a
    predicate_hint: `0x0086dd62: cmp eax, dword ptr [0xd6b9e8]`
  - 0x0086dd79: je | true=0x0086dda0 | false=0x0086dd7b
    predicate_hint: `0x0086dd77: test al, al`
  - 0x0086ddcb: je | true=0x0086ddd5 | false=0x0086ddcd
    predicate_hint: `0x0086ddc7: test byte ptr [ebx + 4], 2`
  - 0x0086de19: je | true=0x0086de24 | false=0x0086de1b
    predicate_hint: `0x0086de17: test ecx, ecx`
  - 0x0086dea8: jne | true=0x0086deb8 | false=0x0086deaa
    predicate_hint: `0x0086dea1: cmp dword ptr [ebx + 0x1e0], 1`
  - 0x0086debd: je | true=0x0086e142 | false=0x0086dec3
    predicate_hint: `0x0086debb: test al, 2`
  - 0x0086dec9: jb | true=0x0086eb0a | false=0x0086decf
    predicate_hint: `0x0086dec3: cmp edi, dword ptr [ebx + 0x1dc]`
  - 0x0086decf: ja | true=0x0086dee0 | false=0x0086ded1
  - 0x0086deda: jbe | true=0x0086eb0a | false=0x0086dee0
    predicate_hint: `0x0086ded4: cmp ecx, dword ptr [ebx + 0x1d8]`
  - 0x0086dee2: jne | true=0x0086eb0a | false=0x0086dee8
    predicate_hint: `0x0086dee0: test al, 0x40`
  - 0x0086deea: jne | true=0x0086dfb0 | false=0x0086def0
    predicate_hint: `0x0086dee8: test al, 8`
  - 0x0086df0e: je | true=0x0086df47 | false=0x0086df10
    predicate_hint: `0x0086df0c: test ecx, ecx`
  - 0x0086dfbc: je | true=0x0086e064 | false=0x0086dfc2
    predicate_hint: `0x0086dfba: test al, al`
  - 0x0086dfd3: jne | true=0x0086eb0a | false=0x0086dfd9
    predicate_hint: `0x0086dfd1: test al, al`
  - 0x0086dff8: je | true=0x0086e031 | false=0x0086dffa
    predicate_hint: `0x0086dff6: test edi, edi`
  - 0x0086e0aa: je | true=0x0086e0b5 | false=0x0086e0ac
    predicate_hint: `0x0086e0a8: test ecx, ecx`
  - 0x0086e149: jne | true=0x0086e2b7 | false=0x0086e14f
    predicate_hint: `0x0086e142: cmp dword ptr [ebx + 0x1e0], 1`
  - 0x0086e155: jb | true=0x0086eb0a | false=0x0086e15b
    predicate_hint: `0x0086e14f: cmp edi, dword ptr [ebx + 0x194]`
  - 0x0086e15b: ja | true=0x0086e16c | false=0x0086e15d
  - 0x0086e166: jbe | true=0x0086eb0a | false=0x0086e16c
    predicate_hint: `0x0086e160: cmp eax, dword ptr [ebx + 0x190]`
  - 0x0086e17c: je | true=0x0086e267 | false=0x0086e182
    predicate_hint: `0x0086e17a: test eax, eax`
  - 0x0086e25e: jb | true=0x0086e190 | false=0x0086e264
    predicate_hint: `0x0086e25c: cmp edi, eax`
  - 0x0086e2c3: je | true=0x0086eb0a | false=0x0086e2c9
    predicate_hint: `0x0086e2c1: test al, al`
  - 0x0086e2d7: je | true=0x0086e8cc | false=0x0086e2dd
    predicate_hint: `0x0086e2d1: cmp eax, dword ptr [ebx + 0x1e4]`
  - 0x0086e2f1: jb | true=0x0086e8bf | false=0x0086e2f7
    predicate_hint: `0x0086e2ee: cmp eax, dword ptr [edi + 0x2c]`
  - 0x0086e2f7: ja | true=0x0086e305 | false=0x0086e2f9
  - 0x0086e2ff: jbe | true=0x0086e8bf | false=0x0086e305
    predicate_hint: `0x0086e2fc: cmp eax, dword ptr [edi + 0x28]`
  - 0x0086e30b: jne | true=0x0086e5c7 | false=0x0086e311
    predicate_hint: `0x0086e308: cmp eax, 1`
  - 0x0086e338: je | true=0x0086e4f5 | false=0x0086e33e
    predicate_hint: `0x0086e334: cmp byte ptr [edi + 0x40], 0`
  - 0x0086e369: je | true=0x0086e372 | false=0x0086e36b
    predicate_hint: `0x0086e367: test ecx, ecx`
  - 0x0086e3e7: je | true=0x0086e3f3 | false=0x0086e3e9
    predicate_hint: `0x0086e3e5: cmp ecx, eax`
  - 0x0086e406: jb | true=0x0086e416 | false=0x0086e408
    predicate_hint: `0x0086e3fb: cmp dword ptr [ebp - 0x80], 0x10`
  - 0x0086e468: je | true=0x0086e471 | false=0x0086e46a
    predicate_hint: `0x0086e466: test ecx, ecx`
  - 0x0086e520: je | true=0x0086e5b2 | false=0x0086e526
    predicate_hint: `0x0086e51e: test ebx, ebx`
  - 0x0086e5ca: jne | true=0x0086e8bf | false=0x0086e5d0
    predicate_hint: `0x0086e5c7: cmp eax, 3`
  - 0x0086e5d4: jbe | true=0x0086e5f1 | false=0x0086e5d6
    predicate_hint: `0x0086e5d0: cmp dword ptr [edi + 0x60], 0`
  - 0x0086e61a: jae | true=0x0086e6cd | false=0x0086e620
    predicate_hint: `0x0086e617: cmp eax, dword ptr [edi + 0x30]`
  - 0x0086e653: je | true=0x0086e6a5 | false=0x0086e655
    predicate_hint: `0x0086e651: add eax, edx`
  - 0x0086e66b: je | true=0x0086e67d | false=0x0086e66d
    predicate_hint: `0x0086e663: cmp dword ptr [esi + eax + 0xc8], 0`
  - 0x0086e69d: jb | true=0x0086e660 | false=0x0086e69f
    predicate_hint: `0x0086e69b: cmp ebx, eax`
  - 0x0086e6e9: je | true=0x0086e75a | false=0x0086e6eb
    predicate_hint: `0x0086e6e7: add eax, edx`
  - 0x0086e6fb: je | true=0x0086e732 | false=0x0086e6fd
    predicate_hint: `0x0086e6f3: cmp dword ptr [esi + eax + 0xc8], 0`
  - 0x0086e755: jb | true=0x0086e6f0 | false=0x0086e757
    predicate_hint: `0x0086e752: cmp dword ptr [ebp - 0x1c], eax`
  - 0x0086e75e: je | true=0x0086e84f | false=0x0086e764
    predicate_hint: `0x0086e75a: cmp byte ptr [edi + 0x40], 0`
  - 0x0086e78f: je | true=0x0086e7db | false=0x0086e791
    predicate_hint: `0x0086e78d: test ebx, ebx`
  - 0x0086e87d: je | true=0x0086e8a1 | false=0x0086e87f
    predicate_hint: `0x0086e87b: test edx, edx`
  - 0x0086e8c3: jne | true=0x0086e2e3 | false=0x0086e8c9
    predicate_hint: `0x0086e8c1: cmp esi, dword ptr [ecx]`
  - 0x0086e8da: je | true=0x0086eb0a | false=0x0086e8e0
    predicate_hint: `0x0086e8d4: cmp eax, dword ptr [ebx + 0x1ec]`
  - 0x0086e8f4: jb | true=0x0086eb00 | false=0x0086e8fa
    predicate_hint: `0x0086e8f1: cmp edx, dword ptr [eax + 0x2c]`
  - 0x0086e8fa: ja | true=0x0086e908 | false=0x0086e8fc
  - 0x0086e902: jbe | true=0x0086eb00 | false=0x0086e908
    predicate_hint: `0x0086e8ff: cmp edx, dword ptr [eax + 0x28]`
  - 0x0086e90e: je | true=0x0086e96f | false=0x0086e910
    predicate_hint: `0x0086e90b: cmp ecx, 2`
  - 0x0086e913: je | true=0x0086e96f | false=0x0086e915
    predicate_hint: `0x0086e910: cmp ecx, 1`
  - 0x0086e918: je | true=0x0086e93a | false=0x0086e91a
    predicate_hint: `0x0086e915: cmp ecx, 3`
  - 0x0086e91d: je | true=0x0086e93a | false=0x0086e91f
    predicate_hint: `0x0086e91a: cmp ecx, 5`
  - 0x0086e928: jne | true=0x0086eb00 | false=0x0086e92e
    predicate_hint: `0x0086e91f: cmp ecx, 6`
  - 0x0086e98b: je | true=0x0086ea17 | false=0x0086e991
    predicate_hint: `0x0086e987: cmp byte ptr [eax + 0x40], 0`
  - 0x0086ea01: jb | true=0x0086eaad | false=0x0086ea07
    predicate_hint: `0x0086e9f6: cmp dword ptr [ebp - 0x38], 0x10`
  - 0x0086ea9d: jb | true=0x0086eaaa | false=0x0086ea9f
    predicate_hint: `0x0086ea92: cmp dword ptr [ebp - 0x38], 0x10`
  - 0x0086eb04: jne | true=0x0086e8e6 | false=0x0086eb0a
    predicate_hint: `0x0086eb02: cmp edi, dword ptr [ecx]`

### 0x00822f67
- blocks=103, insns=577, edges=252, jcc=84, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00822f72: jne | true=0x00823500 | false=0x00822f78
    predicate_hint: `0x00822f6e: cmp dword ptr [esi + 0x54], 1`
  - 0x00822fc0: je | true=0x00822fc7 | false=0x00822fc2
    predicate_hint: `0x00822fbd: mov dword ptr [esi + 0x5c], ecx`
  - 0x00822fcb: je | true=0x00822fd5 | false=0x00822fcd
    predicate_hint: `0x00822fc7: cmp dword ptr [esi + 0x7c], 0`
  - 0x00822ffa: jne | true=0x00823021 | false=0x00822ffc
    predicate_hint: `0x00822ff7: cmp eax, 2`
  - 0x00823000: jne | true=0x00823021 | false=0x00823002
    predicate_hint: `0x00822ffc: cmp dword ptr [esi + 0x7c], 0`
  - 0x00823006: jne | true=0x00823021 | false=0x00823008
    predicate_hint: `0x00823002: cmp dword ptr [esi + 0x10], 0`
  - 0x0082303b: je | true=0x008234a8 | false=0x00823041
    predicate_hint: `0x00823038: cmp edi, dword ptr [esi + 0x78]`
  - 0x0082305e: jne | true=0x00823067 | false=0x00823060
    predicate_hint: `0x00823059: movq qword ptr [ebp - 0x2c], xmm0`
  - 0x00823075: jb | true=0x0082316b | false=0x0082307b
    predicate_hint: `0x00823071: cmp dword ptr [eax + 8], 2`
  - 0x00823084: jne | true=0x0082316b | false=0x0082308a
    predicate_hint: `0x0082307e: cmp eax, dword ptr [0xf8b764]`
  - 0x008230ac: je | true=0x00823457 | false=0x008230b2
    predicate_hint: `0x008230a9: cmp dword ptr [eax + 0x38], esi`
  - 0x008230e6: jne | true=0x008230ef | false=0x008230e8
    predicate_hint: `0x008230df: cmp dword ptr [0xf8b774], 0`
  - 0x008230fa: jb | true=0x0082344a | false=0x00823100
    predicate_hint: `0x008230f6: cmp dword ptr [eax + 8], 3`
  - 0x00823109: jne | true=0x0082344a | false=0x0082310f
    predicate_hint: `0x00823103: cmp eax, dword ptr [0xf8b788]`
  - 0x00823113: jne | true=0x0082344a | false=0x00823119
    predicate_hint: `0x0082310f: cmp dword ptr [ebp - 8], -1`
  - 0x00823120: jne | true=0x00823129 | false=0x00823122
    predicate_hint: `0x00823119: cmp dword ptr [0xf8b9a0], 0`
  - 0x00823134: jb | true=0x0082344a | false=0x0082313a
    predicate_hint: `0x00823130: cmp dword ptr [eax + 8], 4`
  - 0x00823143: jne | true=0x0082344a | false=0x00823149
    predicate_hint: `0x0082313d: cmp eax, dword ptr [0xf8b9b8]`
  - 0x0082314d: jbe | true=0x0082344a | false=0x00823153
    predicate_hint: `0x00823149: cmp dword ptr [esi + 0x70], 0`
  - 0x0082315c: jb | true=0x0082344a | false=0x00823162
    predicate_hint: `0x00823156: cmp eax, dword ptr [esi + 0x80]`
  - 0x00823172: jne | true=0x0082317b | false=0x00823174
    predicate_hint: `0x0082316b: cmp dword ptr [0xf8bc28], 0`
  - 0x00823186: jb | true=0x008232a4 | false=0x0082318c
    predicate_hint: `0x00823182: cmp dword ptr [eax + 8], 2`
  - 0x00823195: jne | true=0x008232a4 | false=0x0082319b
    predicate_hint: `0x0082318f: cmp eax, dword ptr [0xf8bc38]`
  - 0x008231bd: je | true=0x00823457 | false=0x008231c3
    predicate_hint: `0x008231ba: cmp dword ptr [eax + 0x38], esi`
  - 0x008231f5: jne | true=0x00823212 | false=0x008231f7
    predicate_hint: `0x008231f2: cmp eax, -1`
  - 0x0082320c: jne | true=0x0082345a | false=0x00823212
    predicate_hint: `0x00823209: cmp eax, -1`
  - 0x00823219: jne | true=0x00823222 | false=0x0082321b
    predicate_hint: `0x00823212: cmp dword ptr [0xf8bc6c], 0`
  - 0x0082322d: jb | true=0x0082324f | false=0x0082322f
    predicate_hint: `0x00823229: cmp dword ptr [eax + 8], 3`
  - 0x00823238: jne | true=0x0082324f | false=0x0082323a
    predicate_hint: `0x00823232: cmp eax, dword ptr [0xf8bc80]`
  - 0x00823257: je | true=0x0082348e | false=0x0082325d
    predicate_hint: `0x00823254: cmp ecx, -1`
  - 0x008232ab: jne | true=0x008232b4 | false=0x008232ad
    predicate_hint: `0x008232a4: cmp dword ptr [0xf8c928], 0`
  - 0x008232bf: jb | true=0x008232e9 | false=0x008232c1
    predicate_hint: `0x008232bb: cmp dword ptr [eax + 8], 3`
  - 0x008232ca: jne | true=0x008232e9 | false=0x008232cc
    predicate_hint: `0x008232c4: cmp eax, dword ptr [0xf8c93c]`
  - 0x008232f0: jne | true=0x008232f9 | false=0x008232f2
    predicate_hint: `0x008232e9: cmp dword ptr [0xf8c904], 0`
  - 0x00823304: jb | true=0x00823311 | false=0x00823306
    predicate_hint: `0x00823300: cmp dword ptr [eax + 8], 3`
  - 0x0082330f: je | true=0x008232cc | false=0x00823311
    predicate_hint: `0x00823309: cmp eax, dword ptr [0xf8c918]`
  - 0x00823318: jne | true=0x00823321 | false=0x0082331a
    predicate_hint: `0x00823311: cmp dword ptr [0xf8b178], 0`
  - 0x0082332c: jb | true=0x00823344 | false=0x0082332e
    predicate_hint: `0x00823328: cmp dword ptr [eax + 8], 3`
  - 0x00823337: jne | true=0x00823344 | false=0x00823339
    predicate_hint: `0x00823331: cmp eax, dword ptr [0xf8b18c]`
  - 0x0082334b: jne | true=0x00823354 | false=0x0082334d
    predicate_hint: `0x00823344: cmp dword ptr [0xf8d794], 0`
  - 0x0082335f: jb | true=0x00823377 | false=0x00823361
    predicate_hint: `0x0082335b: cmp dword ptr [eax + 8], 3`
  - 0x0082336a: jne | true=0x00823377 | false=0x0082336c
    predicate_hint: `0x00823364: cmp eax, dword ptr [0xf8d7a8]`
  - 0x0082337e: jne | true=0x00823387 | false=0x00823380
    predicate_hint: `0x00823377: cmp dword ptr [0xf8af38], 0`
  - 0x00823392: jb | true=0x008233aa | false=0x00823394
    predicate_hint: `0x0082338e: cmp dword ptr [eax + 8], 3`
  - 0x0082339d: jne | true=0x008233aa | false=0x0082339f
    predicate_hint: `0x00823397: cmp eax, dword ptr [0xf8af4c]`
  - 0x008233b1: jne | true=0x008233ba | false=0x008233b3
    predicate_hint: `0x008233aa: cmp dword ptr [0xf8af5c], 0`
  - 0x008233c5: jb | true=0x008233dd | false=0x008233c7
    predicate_hint: `0x008233c1: cmp dword ptr [eax + 8], 3`
  - 0x008233d0: jne | true=0x008233dd | false=0x008233d2
    predicate_hint: `0x008233ca: cmp eax, dword ptr [0xf8af70]`
  - 0x008233e4: jne | true=0x008233ed | false=0x008233e6
    predicate_hint: `0x008233dd: cmp dword ptr [0xf8af80], 0`
  - 0x008233f8: jb | true=0x00823410 | false=0x008233fa
    predicate_hint: `0x008233f4: cmp dword ptr [eax + 8], 3`
  - 0x00823403: jne | true=0x00823410 | false=0x00823405
    predicate_hint: `0x008233fd: cmp eax, dword ptr [0xf8af94]`
  - 0x00823417: jne | true=0x00823420 | false=0x00823419
    predicate_hint: `0x00823410: cmp dword ptr [0xf8cd30], 0`
  - 0x0082342b: jb | true=0x00823443 | false=0x0082342d
    predicate_hint: `0x00823427: cmp dword ptr [eax + 8], 3`
  - 0x00823436: jne | true=0x00823443 | false=0x00823438
    predicate_hint: `0x00823430: cmp eax, dword ptr [0xf8cd44]`
  - 0x0082344f: je | true=0x00823251 | false=0x00823455
    predicate_hint: `0x0082344c: cmp byte ptr [ebp - 2], al`
  - 0x00823494: jne | true=0x0082349a | false=0x00823496
    predicate_hint: `0x00823490: cmp byte ptr [ebp - 1], 0`
  - 0x00823498: je | true=0x0082349c | false=0x0082349a
    predicate_hint: `0x00823496: test al, al`
  - 0x008234a2: jne | true=0x00823041 | false=0x008234a8
    predicate_hint: `0x0082349f: cmp edi, dword ptr [esi + 0x78]`
  - 0x008234ac: jne | true=0x008234b2 | false=0x008234ae
    predicate_hint: `0x008234a8: cmp byte ptr [ebp - 3], 0`
  - 0x008234b0: je | true=0x008234be | false=0x008234b2
    predicate_hint: `0x008234ae: test al, al`
  - 0x008234c6: je | true=0x008234f9 | false=0x008234c8
    predicate_hint: `0x008234c2: cmp dword ptr [esi + 0x7c], 0`
  - 0x008234cc: je | true=0x008234f9 | false=0x008234ce
    predicate_hint: `0x008234c8: cmp byte ptr [esi + 0x75], 0`
  - 0x008234db: jbe | true=0x00823500 | false=0x008234dd
    predicate_hint: `0x008234d4: cmp dword ptr [esi + 0x70], 0x7d0`
  - 0x008234e6: jb | true=0x008234f5 | false=0x008234e8
    predicate_hint: `0x008234e0: cmp eax, dword ptr [esi + 0x80]`

### 0x00887fe0
- blocks=93, insns=676, edges=230, jcc=83, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088801d: je | true=0x0088804a | false=0x0088801f
    predicate_hint: `0x0088801b: test esi, esi`
  - 0x00888026: jne | true=0x0088802f | false=0x00888028
    predicate_hint: `0x0088801f: cmp dword ptr [0xf8f4e0], 0`
  - 0x0088803a: jb | true=0x0088804a | false=0x0088803c
    predicate_hint: `0x00888036: cmp dword ptr [eax + 8], 3`
  - 0x00888048: je | true=0x00888051 | false=0x0088804a
    predicate_hint: `0x00888042: cmp eax, dword ptr [0xf8f4f4]`
  - 0x00888053: je | true=0x00888080 | false=0x00888055
    predicate_hint: `0x00888051: test esi, esi`
  - 0x0088805c: jne | true=0x00888065 | false=0x0088805e
    predicate_hint: `0x00888055: cmp dword ptr [0xf8f528], 0`
  - 0x00888070: jb | true=0x00888080 | false=0x00888072
    predicate_hint: `0x0088806c: cmp dword ptr [eax + 8], 3`
  - 0x0088807e: je | true=0x00888087 | false=0x00888080
    predicate_hint: `0x00888078: cmp eax, dword ptr [0xf8f53c]`
  - 0x00888089: je | true=0x008880b6 | false=0x0088808b
    predicate_hint: `0x00888087: test esi, esi`
  - 0x00888092: jne | true=0x0088809b | false=0x00888094
    predicate_hint: `0x0088808b: cmp dword ptr [0xf8f378], 0`
  - 0x008880a6: jb | true=0x008880b6 | false=0x008880a8
    predicate_hint: `0x008880a2: cmp dword ptr [eax + 8], 3`
  - 0x008880b4: je | true=0x008880bd | false=0x008880b6
    predicate_hint: `0x008880ae: cmp eax, dword ptr [0xf8f38c]`
  - 0x008880bf: je | true=0x008880ec | false=0x008880c1
    predicate_hint: `0x008880bd: test esi, esi`
  - 0x008880c8: jne | true=0x008880d1 | false=0x008880ca
    predicate_hint: `0x008880c1: cmp dword ptr [0xf8f39c], 0`
  - 0x008880dc: jb | true=0x008880ec | false=0x008880de
    predicate_hint: `0x008880d8: cmp dword ptr [eax + 8], 3`
  - 0x008880ea: je | true=0x008880f3 | false=0x008880ec
    predicate_hint: `0x008880e4: cmp eax, dword ptr [0xf8f3b0]`
  - 0x008880f5: je | true=0x00888122 | false=0x008880f7
    predicate_hint: `0x008880f3: test esi, esi`
  - 0x008880fe: jne | true=0x00888107 | false=0x00888100
    predicate_hint: `0x008880f7: cmp dword ptr [0xf8f3c0], 0`
  - 0x00888112: jb | true=0x00888122 | false=0x00888114
    predicate_hint: `0x0088810e: cmp dword ptr [eax + 8], 3`
  - 0x00888120: je | true=0x00888129 | false=0x00888122
    predicate_hint: `0x0088811a: cmp eax, dword ptr [0xf8f3d4]`
  - 0x0088812b: je | true=0x00888155 | false=0x0088812d
    predicate_hint: `0x00888129: test esi, esi`
  - 0x00888134: jne | true=0x0088813d | false=0x00888136
    predicate_hint: `0x0088812d: cmp dword ptr [0xf8f3e4], 0`
  - 0x00888148: jb | true=0x00888155 | false=0x0088814a
    predicate_hint: `0x00888144: cmp dword ptr [eax + 8], 3`
  - 0x00888153: je | true=0x00888157 | false=0x00888155
    predicate_hint: `0x0088814d: cmp eax, dword ptr [0xf8f3f8]`
  - 0x0088815c: je | true=0x00888231 | false=0x00888162
    predicate_hint: `0x0088815a: test eax, eax`
  - 0x0088816d: je | true=0x0088817c | false=0x0088816f
    predicate_hint: `0x0088816b: cmp ecx, edx`
  - 0x008881a5: je | true=0x0088831e | false=0x008881ab
    predicate_hint: `0x008881a3: cmp esi, edi`
  - 0x008881b8: je | true=0x008881fd | false=0x008881ba
    predicate_hint: `0x008881b6: test al, 1`
  - 0x008881bc: jne | true=0x008881fd | false=0x008881be
    predicate_hint: `0x008881ba: test al, 0x28`
  - 0x00888201: jne | true=0x00888316 | false=0x00888207
    predicate_hint: `0x008881fd: cmp byte ptr [esi + 0xd], 0`
  - 0x0088820e: jne | true=0x008882fb | false=0x00888214
    predicate_hint: `0x0088820a: cmp byte ptr [eax + 0xd], 0`
  - 0x0088821c: jne | true=0x00888316 | false=0x00888222
    predicate_hint: `0x00888218: cmp byte ptr [eax + 0xd], 0`
  - 0x0088822a: je | true=0x00888222 | false=0x0088822c
    predicate_hint: `0x00888226: cmp byte ptr [eax + 0xd], 0`
  - 0x00888236: je | true=0x0088826b | false=0x00888238
    predicate_hint: `0x00888234: test eax, eax`
  - 0x00888249: je | true=0x00888258 | false=0x0088824b
    predicate_hint: `0x00888247: cmp ecx, edx`
  - 0x00888270: je | true=0x0088829f | false=0x00888272
    predicate_hint: `0x0088826e: test eax, eax`
  - 0x0088827d: je | true=0x0088828c | false=0x0088827f
    predicate_hint: `0x0088827b: cmp ecx, edx`
  - 0x008882a4: je | true=0x008882c3 | false=0x008882a6
    predicate_hint: `0x008882a2: test ecx, ecx`
  - 0x008882c7: je | true=0x008882d9 | false=0x008882c9
    predicate_hint: `0x008882c3: cmp dword ptr [ebp - 0x24], 0`
  - 0x008882db: je | true=0x0088818a | false=0x008882e1
    predicate_hint: `0x008882d9: test esi, esi`
  - 0x00888302: jne | true=0x00888314 | false=0x00888304
    predicate_hint: `0x008882fe: cmp byte ptr [eax + 0xd], 0`
  - 0x00888307: jne | true=0x00888314 | false=0x00888309
    predicate_hint: `0x00888304: cmp esi, dword ptr [eax + 8]`
  - 0x00888312: je | true=0x00888304 | false=0x00888314
    predicate_hint: `0x0088830e: cmp byte ptr [eax + 0xd], 0`
  - 0x00888318: jne | true=0x008881b0 | false=0x0088831e
    predicate_hint: `0x00888316: cmp esi, edi`
  - 0x00888323: jae | true=0x008883d9 | false=0x00888329
    predicate_hint: `0x00888321: cmp al, 0x80`
  - 0x0088832b: jne | true=0x008883d9 | false=0x00888331
    predicate_hint: `0x00888329: test al, 4`
  - 0x00888361: je | true=0x008883d9 | false=0x00888363
    predicate_hint: `0x0088835f: test al, al`
  - 0x00888383: je | true=0x008883d9 | false=0x00888385
    predicate_hint: `0x00888381: test esi, esi`
  - 0x008883e0: je | true=0x00888417 | false=0x008883e2
    predicate_hint: `0x008883d9: cmp dword ptr [ebx + 0x180], 0`
  - 0x0088841f: je | true=0x0088843d | false=0x00888421
    predicate_hint: `0x0088841d: test edi, edi`
  - 0x00888485: je | true=0x00888491 | false=0x00888487
    predicate_hint: `0x00888483: cmp ecx, eax`
  - 0x0088849c: je | true=0x008884a8 | false=0x0088849e
    predicate_hint: `0x0088849a: cmp ecx, eax`
  - 0x008884b3: je | true=0x008884bf | false=0x008884b5
    predicate_hint: `0x008884b1: cmp ecx, eax`
  - 0x008884e5: je | true=0x00888526 | false=0x008884e7
    predicate_hint: `0x008884e3: test al, 0x10`
  - 0x008884e9: jne | true=0x00888526 | false=0x008884eb
    predicate_hint: `0x008884e7: test al, 0x20`
  - 0x0088853f: jne | true=0x00888567 | false=0x00888541
    predicate_hint: `0x0088853b: cmp byte ptr [edi + 0xd], 0`
  - 0x0088855f: je | true=0x00888544 | false=0x00888561
    predicate_hint: `0x0088855b: cmp byte ptr [esi + 0xd], 0`

### 0x00888610
- blocks=83, insns=384, edges=177, jcc=69, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00888635: je | true=0x00888662 | false=0x00888637
    predicate_hint: `0x00888633: test esi, esi`
  - 0x0088863e: jne | true=0x00888647 | false=0x00888640
    predicate_hint: `0x00888637: cmp dword ptr [0xf8f2e8], 0`
  - 0x00888652: jb | true=0x00888662 | false=0x00888654
    predicate_hint: `0x0088864e: cmp dword ptr [eax + 8], 3`
  - 0x00888660: je | true=0x00888669 | false=0x00888662
    predicate_hint: `0x0088865a: cmp eax, dword ptr [0xf8f2fc]`
  - 0x0088866b: je | true=0x00888698 | false=0x0088866d
    predicate_hint: `0x00888669: test esi, esi`
  - 0x00888674: jne | true=0x0088867d | false=0x00888676
    predicate_hint: `0x0088866d: cmp dword ptr [0xf8f3e4], 0`
  - 0x00888688: jb | true=0x00888698 | false=0x0088868a
    predicate_hint: `0x00888684: cmp dword ptr [eax + 8], 3`
  - 0x00888696: je | true=0x0088869f | false=0x00888698
    predicate_hint: `0x00888690: cmp eax, dword ptr [0xf8f3f8]`
  - 0x008886a1: je | true=0x008886ce | false=0x008886a3
    predicate_hint: `0x0088869f: test esi, esi`
  - 0x008886aa: jne | true=0x008886b3 | false=0x008886ac
    predicate_hint: `0x008886a3: cmp dword ptr [0xf8f4e0], 0`
  - 0x008886be: jb | true=0x008886ce | false=0x008886c0
    predicate_hint: `0x008886ba: cmp dword ptr [eax + 8], 3`
  - 0x008886cc: je | true=0x008886d5 | false=0x008886ce
    predicate_hint: `0x008886c6: cmp eax, dword ptr [0xf8f4f4]`
  - 0x008886d7: je | true=0x00888704 | false=0x008886d9
    predicate_hint: `0x008886d5: test esi, esi`
  - 0x008886e0: jne | true=0x008886e9 | false=0x008886e2
    predicate_hint: `0x008886d9: cmp dword ptr [0xf8f528], 0`
  - 0x008886f4: jb | true=0x00888704 | false=0x008886f6
    predicate_hint: `0x008886f0: cmp dword ptr [eax + 8], 3`
  - 0x00888702: je | true=0x0088870b | false=0x00888704
    predicate_hint: `0x008886fc: cmp eax, dword ptr [0xf8f53c]`
  - 0x0088870d: je | true=0x0088873a | false=0x0088870f
    predicate_hint: `0x0088870b: test esi, esi`
  - 0x00888716: jne | true=0x0088871f | false=0x00888718
    predicate_hint: `0x0088870f: cmp dword ptr [0xf8f378], 0`
  - 0x0088872a: jb | true=0x0088873a | false=0x0088872c
    predicate_hint: `0x00888726: cmp dword ptr [eax + 8], 3`
  - 0x00888738: je | true=0x00888741 | false=0x0088873a
    predicate_hint: `0x00888732: cmp eax, dword ptr [0xf8f38c]`
  - 0x00888743: je | true=0x00888770 | false=0x00888745
    predicate_hint: `0x00888741: test esi, esi`
  - 0x0088874c: jne | true=0x00888755 | false=0x0088874e
    predicate_hint: `0x00888745: cmp dword ptr [0xf8f39c], 0`
  - 0x00888760: jb | true=0x00888770 | false=0x00888762
    predicate_hint: `0x0088875c: cmp dword ptr [eax + 8], 3`
  - 0x0088876e: je | true=0x00888777 | false=0x00888770
    predicate_hint: `0x00888768: cmp eax, dword ptr [0xf8f3b0]`
  - 0x00888779: je | true=0x008887a3 | false=0x0088877b
    predicate_hint: `0x00888777: test esi, esi`
  - 0x00888782: jne | true=0x0088878b | false=0x00888784
    predicate_hint: `0x0088877b: cmp dword ptr [0xf8f3c0], 0`
  - 0x00888796: jb | true=0x008887a3 | false=0x00888798
    predicate_hint: `0x00888792: cmp dword ptr [eax + 8], 3`
  - 0x008887a1: je | true=0x008887a5 | false=0x008887a3
    predicate_hint: `0x0088879b: cmp eax, dword ptr [0xf8f3d4]`
  - 0x008887a9: je | true=0x008887b5 | false=0x008887ab
    predicate_hint: `0x008887a5: cmp dword ptr [ebp - 0xc], 0`
  - 0x008887ba: je | true=0x008887cd | false=0x008887bc
    predicate_hint: `0x008887b8: test ecx, ecx`
  - 0x008887d2: je | true=0x008887f3 | false=0x008887d4
    predicate_hint: `0x008887d0: test eax, eax`
  - 0x008887df: je | true=0x008887ee | false=0x008887e1
    predicate_hint: `0x008887dd: cmp ecx, edx`
  - 0x008887f8: je | true=0x0088881e | false=0x008887fa
    predicate_hint: `0x008887f6: test eax, eax`
  - 0x00888805: je | true=0x00888814 | false=0x00888807
    predicate_hint: `0x00888803: cmp ecx, edx`
  - 0x00888823: je | true=0x00888849 | false=0x00888825
    predicate_hint: `0x00888821: test eax, eax`
  - 0x00888830: je | true=0x0088883f | false=0x00888832
    predicate_hint: `0x0088882e: cmp ecx, edx`
  - 0x0088884e: je | true=0x0088885e | false=0x00888850
    predicate_hint: `0x0088884c: test ecx, ecx`
  - 0x00888860: je | true=0x0088886d | false=0x00888862
    predicate_hint: `0x0088885e: test esi, esi`
  - 0x0088887e: je | true=0x008888e9 | false=0x00888880
    predicate_hint: `0x0088887c: test eax, eax`
  - 0x008888f3: je | true=0x008888dd | false=0x008888f5
    predicate_hint: `0x008888f1: cmp esi, edi`
  - 0x008888fd: je | true=0x0088893f | false=0x008888ff
    predicate_hint: `0x008888fb: test al, 1`
  - 0x00888901: jne | true=0x0088893f | false=0x00888903
    predicate_hint: `0x008888ff: test al, 0x28`
  - 0x00888946: jne | true=0x00888987 | false=0x00888948
    predicate_hint: `0x00888942: cmp byte ptr [esi + 0xd], 0`
  - 0x0088894f: jne | true=0x0088896c | false=0x00888951
    predicate_hint: `0x0088894b: cmp byte ptr [eax + 0xd], 0`
  - 0x00888959: jne | true=0x00888987 | false=0x0088895b
    predicate_hint: `0x00888955: cmp byte ptr [eax + 0xd], 0`
  - 0x00888968: je | true=0x00888960 | false=0x0088896a
    predicate_hint: `0x00888964: cmp byte ptr [eax + 0xd], 0`
  - 0x00888973: jne | true=0x00888985 | false=0x00888975
    predicate_hint: `0x0088896f: cmp byte ptr [eax + 0xd], 0`
  - 0x00888978: jne | true=0x00888985 | false=0x0088897a
    predicate_hint: `0x00888975: cmp esi, dword ptr [eax + 8]`
  - 0x00888983: je | true=0x00888975 | false=0x00888985
    predicate_hint: `0x0088897f: cmp byte ptr [eax + 0xd], 0`
  - 0x00888989: jne | true=0x008888f5 | false=0x0088898f
    predicate_hint: `0x00888987: cmp esi, edi`

### 0x0089a3c0
- blocks=71, insns=855, edges=166, jcc=52, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0089a3f5: jne | true=0x0089a40b | false=0x0089a3f7
    predicate_hint: `0x0089a3f1: cmp byte ptr [esi + 0xd], 0`
  - 0x0089a3fa: jae | true=0x0089a401 | false=0x0089a3fc
    predicate_hint: `0x0089a3f7: cmp dword ptr [esi + 0x10], ecx`
  - 0x0089a409: je | true=0x0089a3f7 | false=0x0089a40b
    predicate_hint: `0x0089a405: cmp byte ptr [esi + 0xd], 0`
  - 0x0089a40d: je | true=0x0089a414 | false=0x0089a40f
    predicate_hint: `0x0089a40b: cmp eax, edx`
  - 0x0089a412: jae | true=0x0089a416 | false=0x0089a414
    predicate_hint: `0x0089a40f: cmp ecx, dword ptr [eax + 0x10]`
  - 0x0089a418: je | true=0x0089ab25 | false=0x0089a41e
    predicate_hint: `0x0089a416: cmp eax, edx`
  - 0x0089a423: je | true=0x0089ab25 | false=0x0089a429
    predicate_hint: `0x0089a421: test edx, edx`
  - 0x0089a430: je | true=0x0089a52d | false=0x0089a436
    predicate_hint: `0x0089a429: cmp dword ptr [edx + 0x208], -1`
  - 0x0089a45f: je | true=0x0089a4bc | false=0x0089a461
    predicate_hint: `0x0089a45d: test edi, edi`
  - 0x0089a54f: je | true=0x0089a75a | false=0x0089a555
    predicate_hint: `0x0089a548: cmp dword ptr [ebx + 0x9c], -1`
  - 0x0089a579: je | true=0x0089a5e3 | false=0x0089a57b
    predicate_hint: `0x0089a577: test esi, esi`
  - 0x0089a5d3: jb | true=0x0089a5d7 | false=0x0089a5d5
    predicate_hint: `0x0089a5c8: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0089a60e: jne | true=0x0089a614 | false=0x0089a610
    predicate_hint: `0x0089a60b: cmp byte ptr [edx], 0`
  - 0x0089a625: jne | true=0x0089a620 | false=0x0089a627
    predicate_hint: `0x0089a623: test al, al`
  - 0x0089a671: je | true=0x0089a67d | false=0x0089a673
    predicate_hint: `0x0089a66f: cmp ecx, eax`
  - 0x0089a68e: jb | true=0x0089a69b | false=0x0089a690
    predicate_hint: `0x0089a683: cmp dword ptr [ebp - 0x28], 0x10`
  - 0x0089a6d5: je | true=0x0089a70e | false=0x0089a6d7
    predicate_hint: `0x0089a6d3: test esi, esi`
  - 0x0089a761: je | true=0x0089a96a | false=0x0089a767
    predicate_hint: `0x0089a75a: cmp dword ptr [ebx + 0x98], -1`
  - 0x0089a78b: je | true=0x0089a7f5 | false=0x0089a78d
    predicate_hint: `0x0089a789: test esi, esi`
  - 0x0089a7e5: jb | true=0x0089a7e9 | false=0x0089a7e7
    predicate_hint: `0x0089a7da: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0089a820: jne | true=0x0089a826 | false=0x0089a822
    predicate_hint: `0x0089a81d: cmp byte ptr [edx], 0`
  - 0x0089a835: jne | true=0x0089a830 | false=0x0089a837
    predicate_hint: `0x0089a833: test al, al`
  - 0x0089a881: je | true=0x0089a88d | false=0x0089a883
    predicate_hint: `0x0089a87f: cmp ecx, eax`
  - 0x0089a89e: jb | true=0x0089a8ab | false=0x0089a8a0
    predicate_hint: `0x0089a893: cmp dword ptr [ebp - 0x40], 0x10`
  - 0x0089a8e5: je | true=0x0089a91e | false=0x0089a8e7
    predicate_hint: `0x0089a8e3: test esi, esi`
  - 0x0089a995: je | true=0x0089a9a0 | false=0x0089a997
    predicate_hint: `0x0089a993: test ecx, ecx`
  - 0x0089a9cb: jne | true=0x0089a9d1 | false=0x0089a9cd
    predicate_hint: `0x0089a9c8: cmp byte ptr [edx], 0`
  - 0x0089a9e5: jne | true=0x0089a9e0 | false=0x0089a9e7
    predicate_hint: `0x0089a9e3: test al, al`
  - 0x0089aa31: je | true=0x0089aa3d | false=0x0089aa33
    predicate_hint: `0x0089aa2f: cmp ecx, eax`
  - 0x0089aa4e: jb | true=0x0089aa5b | false=0x0089aa50
    predicate_hint: `0x0089aa43: cmp dword ptr [ebp - 0x58], 0x10`
  - 0x0089aa95: je | true=0x0089aace | false=0x0089aa97
    predicate_hint: `0x0089aa93: test esi, esi`

### 0x00668e1a
- blocks=64, insns=319, edges=120, jcc=46, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00668e37: je | true=0x00668e3e | false=0x00668e39
    predicate_hint: `0x00668e33: cmp byte ptr [ecx + 0xd], 0`
  - 0x00668e45: je | true=0x00668e4b | false=0x00668e47
    predicate_hint: `0x00668e41: cmp byte ptr [eax + 0xd], 0`
  - 0x00668e53: jne | true=0x00668ec9 | false=0x00668e55
    predicate_hint: `0x00668e51: cmp edx, ebx`
  - 0x00668e5c: jne | true=0x00668e61 | false=0x00668e5e
    predicate_hint: `0x00668e55: cmp byte ptr [edi + 0xd], 0`
  - 0x00668e69: jne | true=0x00668e70 | false=0x00668e6b
    predicate_hint: `0x00668e66: cmp dword ptr [eax + 4], ebx`
  - 0x00668e72: jne | true=0x00668e78 | false=0x00668e74
    predicate_hint: `0x00668e70: cmp dword ptr [esi], ebx`
  - 0x00668e7f: jne | true=0x00668e9f | false=0x00668e81
    predicate_hint: `0x00668e7d: cmp dword ptr [eax], ebx`
  - 0x00668e85: je | true=0x00668e8b | false=0x00668e87
    predicate_hint: `0x00668e81: cmp byte ptr [edi + 0xd], 0`
  - 0x00668e99: je | true=0x00668e91 | false=0x00668e9b
    predicate_hint: `0x00668e95: cmp byte ptr [ecx + 0xd], 0`
  - 0x00668ea4: jne | true=0x00668f25 | false=0x00668ea6
    predicate_hint: `0x00668ea1: cmp dword ptr [eax + 8], ebx`
  - 0x00668eaa: je | true=0x00668eb0 | false=0x00668eac
    predicate_hint: `0x00668ea6: cmp byte ptr [edi + 0xd], 0`
  - 0x00668ec0: je | true=0x00668eb7 | false=0x00668ec2
    predicate_hint: `0x00668ebc: cmp byte ptr [ecx + 0xd], 0`
  - 0x00668ed3: jne | true=0x00668ed9 | false=0x00668ed5
    predicate_hint: `0x00668ed0: cmp edx, dword ptr [ebx + 8]`
  - 0x00668ee0: jne | true=0x00668ee5 | false=0x00668ee2
    predicate_hint: `0x00668ed9: cmp byte ptr [edi + 0xd], 0`
  - 0x00668efb: jne | true=0x00668f02 | false=0x00668efd
    predicate_hint: `0x00668ef8: cmp dword ptr [eax + 4], ebx`
  - 0x00668f07: jne | true=0x00668f0d | false=0x00668f09
    predicate_hint: `0x00668f05: cmp dword ptr [eax], ebx`
  - 0x00668f29: jne | true=0x00669018 | false=0x00668f2f
    predicate_hint: `0x00668f25: cmp byte ptr [ebx + 0xc], 1`
  - 0x00668f34: je | true=0x00669014 | false=0x00668f3a
    predicate_hint: `0x00668f31: cmp edi, dword ptr [eax + 4]`
  - 0x00668f47: jne | true=0x00669014 | false=0x00668f4d
    predicate_hint: `0x00668f44: mov dword ptr [ebp - 0x10], esi`
  - 0x00668f51: jne | true=0x00668fc7 | false=0x00668f53
    predicate_hint: `0x00668f4f: cmp edi, ecx`
  - 0x00668f5a: jne | true=0x00668f72 | false=0x00668f5c
    predicate_hint: `0x00668f56: cmp byte ptr [ecx + 0xc], 0`
  - 0x00668f76: jne | true=0x00668ffd | false=0x00668f7c
    predicate_hint: `0x00668f72: cmp byte ptr [ecx + 0xd], 0`
  - 0x00668f82: jne | true=0x00668f8d | false=0x00668f84
    predicate_hint: `0x00668f7e: cmp byte ptr [eax + 0xc], 1`
  - 0x00668f8b: je | true=0x00668ff9 | false=0x00668f8d
    predicate_hint: `0x00668f87: cmp byte ptr [eax + 0xc], 1`
  - 0x00668f94: jne | true=0x00668fab | false=0x00668f96
    predicate_hint: `0x00668f90: cmp byte ptr [eax + 0xc], 1`
  - 0x00668fcb: jne | true=0x00668fe2 | false=0x00668fcd
    predicate_hint: `0x00668fc7: cmp byte ptr [ecx + 0xc], 0`
  - 0x00668fe6: jne | true=0x00668ffd | false=0x00668fe8
    predicate_hint: `0x00668fe2: cmp byte ptr [ecx + 0xd], 0`
  - 0x00668fef: jne | true=0x00669044 | false=0x00668ff1
    predicate_hint: `0x00668feb: cmp byte ptr [eax + 0xc], 1`
  - 0x00668ff7: jne | true=0x00669044 | false=0x00668ff9
    predicate_hint: `0x00668ff3: cmp byte ptr [eax + 0xc], 1`
  - 0x0066900b: jne | true=0x00668f3a | false=0x00669011
    predicate_hint: `0x00669008: cmp ecx, dword ptr [eax + 4]`
  - 0x00669030: je | true=0x00669036 | false=0x00669032
    predicate_hint: `0x0066902e: test eax, eax`
  - 0x0066904a: jne | true=0x00669061 | false=0x0066904c
    predicate_hint: `0x00669046: cmp byte ptr [eax + 0xc], 1`

### 0x00846130
- blocks=44, insns=247, edges=86, jcc=35, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00846146: je | true=0x00846187 | false=0x00846148
    predicate_hint: `0x0084613f: cmp si, word ptr [0xd6b9ec]`
  - 0x0084614f: je | true=0x00846160 | false=0x00846151
    predicate_hint: `0x0084614d: cmp eax, edx`
  - 0x00846158: je | true=0x00846183 | false=0x0084615a
    predicate_hint: `0x00846154: cmp si, word ptr [ecx + 0x30]`
  - 0x0084615e: jne | true=0x00846151 | false=0x00846160
    predicate_hint: `0x0084615c: cmp eax, edx`
  - 0x00846164: jne | true=0x00846217 | false=0x0084616a
    predicate_hint: `0x00846162: test edi, edi`
  - 0x00846191: je | true=0x008461ae | false=0x00846193
    predicate_hint: `0x0084618f: cmp eax, ecx`
  - 0x0084619b: je | true=0x008461a5 | false=0x0084619d
    predicate_hint: `0x00846198: cmp dword ptr [esi + 0xc], edx`
  - 0x008461a1: jne | true=0x00846195 | false=0x008461a3
    predicate_hint: `0x0084619f: cmp eax, ecx`
  - 0x008461a9: jne | true=0x00846217 | false=0x008461ab
    predicate_hint: `0x008461a7: test edi, edi`
  - 0x008461b5: je | true=0x008461ce | false=0x008461b7
    predicate_hint: `0x008461b3: cmp eax, ecx`
  - 0x008461c6: je | true=0x00846211 | false=0x008461c8
    predicate_hint: `0x008461c3: cmp dword ptr [esi + 0xc], edx`
  - 0x008461cc: jne | true=0x008461c0 | false=0x008461ce
    predicate_hint: `0x008461ca: cmp eax, ecx`
  - 0x008461eb: je | true=0x008462d4 | false=0x008461f1
    predicate_hint: `0x008461e9: test edi, edi`
  - 0x008461f5: jne | true=0x008462d4 | false=0x008461fb
    predicate_hint: `0x008461f1: cmp dword ptr [edi + 0x1c], 0`
  - 0x00846202: je | true=0x00846270 | false=0x00846204
    predicate_hint: `0x00846200: cmp eax, ecx`
  - 0x00846207: je | true=0x00846255 | false=0x00846209
    predicate_hint: `0x00846204: cmp dword ptr [eax + 8], edi`
  - 0x0084620d: jne | true=0x00846204 | false=0x0084620f
    predicate_hint: `0x0084620b: cmp eax, ecx`
  - 0x00846215: je | true=0x008461d0 | false=0x00846217
    predicate_hint: `0x00846213: test edi, edi`
  - 0x0084621c: je | true=0x00846222 | false=0x0084621e
    predicate_hint: `0x0084621a: test eax, eax`
  - 0x0084622f: je | true=0x008461d0 | false=0x00846231
    predicate_hint: `0x0084622d: test eax, eax`
  - 0x00846238: je | true=0x008461d0 | false=0x0084623a
    predicate_hint: `0x00846232: cmp dword ptr [esi], -1`
  - 0x0084627a: je | true=0x0084628b | false=0x0084627c
    predicate_hint: `0x00846278: cmp eax, ecx`
  - 0x00846283: je | true=0x008462ed | false=0x00846285
    predicate_hint: `0x00846280: cmp edi, dword ptr [eax + 8]`
  - 0x00846289: jne | true=0x00846280 | false=0x0084628b
    predicate_hint: `0x00846287: cmp eax, ecx`
  - 0x008462aa: je | true=0x008462b6 | false=0x008462ac
    predicate_hint: `0x008462a8: cmp ecx, eax`
  - 0x008462f1: je | true=0x0084628b | false=0x008462f3
    predicate_hint: `0x008462ed: cmp dword ptr [eax + 8], 0`

### 0x00622a98
- blocks=43, insns=843, edges=98, jcc=34, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00622b6d: jb | true=0x00622b82 | false=0x00622b6f
    predicate_hint: `0x00622b6a: comiss xmm1, xmm4`
  - 0x00622bad: jb | true=0x00622bd0 | false=0x00622baf
    predicate_hint: `0x00622ba5: comisd xmm0, xmmword ptr [0xbd56e0]`
  - 0x00622c0a: jp | true=0x00622c1b | false=0x00622c0c
    predicate_hint: `0x00622c07: test ah, 0x44`
  - 0x00622c4f: jl | true=0x00622c61 | false=0x00622c51
    predicate_hint: `0x00622c4c: movaps xmm2, xmm1`
  - 0x00622d65: jae | true=0x00622d79 | false=0x00622d67
    predicate_hint: `0x00622d63: cmp edx, edi`
  - 0x00622d70: jbe | true=0x00622d77 | false=0x00622d72
    predicate_hint: `0x00622d6e: cmp ecx, eax`
  - 0x00622d79: jbe | true=0x00622d8d | false=0x00622d7b
  - 0x00622d84: jbe | true=0x00622d8d | false=0x00622d86
    predicate_hint: `0x00622d82: cmp eax, ecx`
  - 0x00622d9b: jae | true=0x00622dca | false=0x00622d9d
    predicate_hint: `0x00622d99: cmp eax, edi`
  - 0x00622dc5: jne | true=0x00622dac | false=0x00622dc7
    predicate_hint: `0x00622dc2: sub edi, 1`
  - 0x00622de4: jbe | true=0x00623085 | false=0x00622dea
    predicate_hint: `0x00622de0: comiss xmm0, dword ptr [eax + 0x38]`
  - 0x00622df2: jbe | true=0x00622e02 | false=0x00622df4
    predicate_hint: `0x00622def: comiss xmm1, xmm0`
  - 0x006230a2: je | true=0x006231ea | false=0x006230a8
    predicate_hint: `0x006230a0: test edi, edi`
  - 0x006230cb: jb | true=0x006231c8 | false=0x006230d1
    predicate_hint: `0x006230c6: movss dword ptr [ebp - 0x38], xmm0`
  - 0x00623104: jb | true=0x00623145 | false=0x00623106
    predicate_hint: `0x00623100: comiss xmm1, dword ptr [ebp - 0x20]`
  - 0x00623198: jbe | true=0x006231a5 | false=0x0062319a
    predicate_hint: `0x00623195: comiss xmm0, xmm1`
  - 0x006231e1: jne | true=0x006230ad | false=0x006231e7
    predicate_hint: `0x006231dc: movss xmm2, dword ptr [ebp - 0x3c]`
  - 0x00623205: je | true=0x00623245 | false=0x00623207
    predicate_hint: `0x00623203: test edi, edi`
  - 0x00623243: jne | true=0x0062320f | false=0x00623245
    predicate_hint: `0x00623240: sub edx, 1`

### 0x0088adb0
- blocks=41, insns=350, edges=107, jcc=34, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088ade8: je | true=0x0088aff8 | false=0x0088adee
    predicate_hint: `0x0088ade2: cmp esi, dword ptr [ebx + 0xa8]`
  - 0x0088ae1e: jb | true=0x0088afe3 | false=0x0088ae24
    predicate_hint: `0x0088ae1b: cmp edx, dword ptr [esi + 0x24]`
  - 0x0088ae24: ja | true=0x0088ae2f | false=0x0088ae26
  - 0x0088ae29: jbe | true=0x0088afe3 | false=0x0088ae2f
    predicate_hint: `0x0088ae26: cmp eax, dword ptr [esi + 0x20]`
  - 0x0088ae34: je | true=0x0088ae79 | false=0x0088ae36
    predicate_hint: `0x0088ae32: test al, al`
  - 0x0088ae45: jne | true=0x0088ae5b | false=0x0088ae47
    predicate_hint: `0x0088ae41: cmp byte ptr [edx + 0xd], 0`
  - 0x0088ae4a: jae | true=0x0088ae51 | false=0x0088ae4c
    predicate_hint: `0x0088ae47: cmp dword ptr [edx + 0x10], edi`
  - 0x0088ae59: je | true=0x0088ae47 | false=0x0088ae5b
    predicate_hint: `0x0088ae55: cmp byte ptr [edx + 0xd], 0`
  - 0x0088ae5d: je | true=0x0088ae64 | false=0x0088ae5f
    predicate_hint: `0x0088ae5b: cmp eax, ecx`
  - 0x0088ae62: jae | true=0x0088ae66 | false=0x0088ae64
    predicate_hint: `0x0088ae5f: cmp edi, dword ptr [eax + 0x10]`
  - 0x0088ae68: je | true=0x0088ae84 | false=0x0088ae6a
    predicate_hint: `0x0088ae66: cmp eax, ecx`
  - 0x0088ae6f: je | true=0x0088ae84 | false=0x0088ae71
    predicate_hint: `0x0088ae6d: test ecx, ecx`
  - 0x0088af42: jb | true=0x0088af4f | false=0x0088af44
    predicate_hint: `0x0088af3a: cmp dword ptr [ebp - 0x2c], 0x10`
  - 0x0088afcd: jb | true=0x0088afda | false=0x0088afcf
    predicate_hint: `0x0088afc5: cmp dword ptr [ebp - 0x4c], 0x10`
  - 0x0088aff2: jne | true=0x0088adf0 | false=0x0088aff8
    predicate_hint: `0x0088afec: cmp esi, dword ptr [ebx + 0xa8]`
  - 0x0088afff: je | true=0x0088b0a9 | false=0x0088b005
    predicate_hint: `0x0088affd: cmp esi, eax`
  - 0x0088b036: jb | true=0x0088b05a | false=0x0088b038
    predicate_hint: `0x0088b033: cmp edx, dword ptr [edi + 4]`
  - 0x0088b038: ja | true=0x0088b03e | false=0x0088b03a
  - 0x0088b03c: jbe | true=0x0088b05a | false=0x0088b03e
    predicate_hint: `0x0088b03a: cmp eax, dword ptr [edi]`
  - 0x0088b05e: jne | true=0x0088b09a | false=0x0088b060
    predicate_hint: `0x0088b05a: cmp byte ptr [esi + 0xd], 0`
  - 0x0088b067: jne | true=0x0088b07f | false=0x0088b069
    predicate_hint: `0x0088b063: cmp byte ptr [eax + 0xd], 0`
  - 0x0088b071: jne | true=0x0088b09a | false=0x0088b073
    predicate_hint: `0x0088b06d: cmp byte ptr [eax + 0xd], 0`
  - 0x0088b07b: je | true=0x0088b073 | false=0x0088b07d
    predicate_hint: `0x0088b077: cmp byte ptr [eax + 0xd], 0`
  - 0x0088b086: jne | true=0x0088b098 | false=0x0088b088
    predicate_hint: `0x0088b082: cmp byte ptr [eax + 0xd], 0`
  - 0x0088b08b: jne | true=0x0088b098 | false=0x0088b08d
    predicate_hint: `0x0088b088: cmp esi, dword ptr [eax + 8]`
  - 0x0088b096: je | true=0x0088b088 | false=0x0088b098
    predicate_hint: `0x0088b092: cmp byte ptr [eax + 0xd], 0`
  - 0x0088b0a3: jne | true=0x0088b005 | false=0x0088b0a9
    predicate_hint: `0x0088b0a0: cmp esi, dword ptr [ebx + 0x48]`

### 0x0086b64c
- blocks=40, insns=246, edges=91, jcc=32, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0086b675: jne | true=0x0086b6aa | false=0x0086b677
    predicate_hint: `0x0086b661: cmp dword ptr [edi + 0x9c], 0`
  - 0x0086b680: jne | true=0x0086b690 | false=0x0086b682
    predicate_hint: `0x0086b67d: cmp byte ptr [edx], 0`
  - 0x0086b69a: jne | true=0x0086b695 | false=0x0086b69c
    predicate_hint: `0x0086b698: test al, al`
  - 0x0086b6c1: jb | true=0x0086b707 | false=0x0086b6c3
    predicate_hint: `0x0086b6b7: cmp dword ptr [edi + 0xb4], 5`
  - 0x0086b6dc: jb | true=0x0086b6e0 | false=0x0086b6de
    predicate_hint: `0x0086b6cf: cmp dword ptr [edi + 0xb8], 0x10`
  - 0x0086b6e7: jne | true=0x0086b6f2 | false=0x0086b6e9
    predicate_hint: `0x0086b6e0: cmp byte ptr [eax + 5], 0`
  - 0x0086b6fc: jne | true=0x0086b6f7 | false=0x0086b6fe
    predicate_hint: `0x0086b6fa: test al, al`
  - 0x0086b721: je | true=0x0086b7ab | false=0x0086b727
    predicate_hint: `0x0086b71e: test ax, ax`
  - 0x0086b75b: jb | true=0x0086b75f | false=0x0086b75d
    predicate_hint: `0x0086b753: cmp dword ptr [edx + 0x14], 0x10`
  - 0x0086b762: jne | true=0x0086b768 | false=0x0086b764
    predicate_hint: `0x0086b75f: cmp byte ptr [edx], 0`
  - 0x0086b775: jne | true=0x0086b770 | false=0x0086b777
    predicate_hint: `0x0086b773: test al, al`
  - 0x0086b78d: jb | true=0x0086b79c | false=0x0086b78f
    predicate_hint: `0x0086b78a: cmp eax, 0x10`
  - 0x0086b7bd: jb | true=0x0086b7c6 | false=0x0086b7bf
    predicate_hint: `0x0086b7b9: cmp dword ptr [esi + 0x14], 0x10`
  - 0x0086b7e4: jne | true=0x0086b7ef | false=0x0086b7e6
    predicate_hint: `0x0086b7e2: test eax, eax`
  - 0x0086b7eb: jb | true=0x0086b7ef | false=0x0086b7ed
    predicate_hint: `0x0086b7e9: cmp ebx, eax`
  - 0x0086b7ed: jbe | true=0x0086b802 | false=0x0086b7ef
  - 0x0086b7f4: je | true=0x0086b802 | false=0x0086b7f6
    predicate_hint: `0x0086b7f2: cmp esi, eax`
  - 0x0086b807: je | true=0x0086b818 | false=0x0086b809
    predicate_hint: `0x0086b802: cmp byte ptr [edi + 0x1d], 0`
  - 0x0086b825: jb | true=0x0086b832 | false=0x0086b827
    predicate_hint: `0x0086b824: pop esi`

### 0x008992b0
- blocks=38, insns=504, edges=103, jcc=31, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008992eb: je | true=0x00899506 | false=0x008992f1
    predicate_hint: `0x008992e5: cmp esi, dword ptr [ebx + 0xa8]`
  - 0x0089930b: jne | true=0x008994f1 | false=0x00899311
    predicate_hint: `0x00899309: cmp edi, eax`
  - 0x00899316: jb | true=0x00899329 | false=0x00899318
    predicate_hint: `0x00899313: sub ebx, 4`
  - 0x0089931c: jne | true=0x0089932e | false=0x0089931e
    predicate_hint: `0x0089931a: cmp eax, dword ptr [ecx]`
  - 0x00899327: jae | true=0x00899318 | false=0x00899329
    predicate_hint: `0x00899324: sub ebx, 4`
  - 0x0089932c: je | true=0x0089936b | false=0x0089932e
    predicate_hint: `0x00899329: cmp ebx, -4`
  - 0x00899332: jne | true=0x008994f1 | false=0x00899338
    predicate_hint: `0x00899330: cmp al, byte ptr [ecx]`
  - 0x0089933b: je | true=0x0089936b | false=0x0089933d
    predicate_hint: `0x00899338: cmp ebx, -3`
  - 0x00899343: jne | true=0x008994f1 | false=0x00899349
    predicate_hint: `0x00899340: cmp al, byte ptr [ecx + 1]`
  - 0x0089934c: je | true=0x0089936b | false=0x0089934e
    predicate_hint: `0x00899349: cmp ebx, -2`
  - 0x00899354: jne | true=0x008994f1 | false=0x0089935a
    predicate_hint: `0x00899351: cmp al, byte ptr [ecx + 2]`
  - 0x0089935d: je | true=0x0089936b | false=0x0089935f
    predicate_hint: `0x0089935a: cmp ebx, -1`
  - 0x00899365: jne | true=0x008994f1 | false=0x0089936b
    predicate_hint: `0x00899362: cmp al, byte ptr [ecx + 3]`
  - 0x00899374: jne | true=0x008994f1 | false=0x0089937a
    predicate_hint: `0x00899371: cmp eax, dword ptr [ebx + 0x20]`
  - 0x0089937f: je | true=0x00899389 | false=0x00899381
    predicate_hint: `0x0089937d: test ecx, ecx`
  - 0x00899450: jb | true=0x00899460 | false=0x00899452
    predicate_hint: `0x00899445: cmp dword ptr [ebp - 0xd4], 0x10`
  - 0x008994db: jb | true=0x008994e8 | false=0x008994dd
    predicate_hint: `0x008994d3: cmp dword ptr [ebp - 0x3c], 0x10`
  - 0x00899500: jne | true=0x008992f1 | false=0x00899506
    predicate_hint: `0x008994fa: cmp esi, dword ptr [ebx + 0xa8]`
  - 0x00899515: jne | true=0x0089952b | false=0x00899517
    predicate_hint: `0x00899511: cmp byte ptr [edx + 0xd], 0`
  - 0x0089951a: jae | true=0x00899521 | false=0x0089951c
    predicate_hint: `0x00899517: cmp dword ptr [edx + 0x10], esi`
  - 0x00899529: je | true=0x00899517 | false=0x0089952b
    predicate_hint: `0x00899525: cmp byte ptr [edx + 0xd], 0`
  - 0x0089952d: je | true=0x00899534 | false=0x0089952f
    predicate_hint: `0x0089952b: cmp eax, ecx`
  - 0x00899532: jae | true=0x00899536 | false=0x00899534
    predicate_hint: `0x0089952f: cmp esi, dword ptr [eax + 0x10]`
  - 0x00899538: je | true=0x008996df | false=0x0089953e
    predicate_hint: `0x00899536: cmp eax, ecx`
  - 0x00899543: je | true=0x008996df | false=0x00899549
    predicate_hint: `0x00899541: test esi, esi`
  - 0x008995b0: jb | true=0x008995c0 | false=0x008995b2
    predicate_hint: `0x008995a2: cmp dword ptr [ebp - 0xec], 0x10`

### 0x00852c50
- blocks=47, insns=564, edges=96, jcc=30, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00852c75: jne | true=0x00853141 | false=0x00852c7b
    predicate_hint: `0x00852c73: test al, 0x10`
  - 0x00852c8c: jne | true=0x00852d84 | false=0x00852c92
    predicate_hint: `0x00852c8a: test al, 1`
  - 0x00852cb6: je | true=0x00852d12 | false=0x00852cb8
    predicate_hint: `0x00852cb4: test edi, edi`
  - 0x00852d02: jb | true=0x00852d06 | false=0x00852d04
    predicate_hint: `0x00852cfe: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00852d52: je | true=0x00852d5e | false=0x00852d54
    predicate_hint: `0x00852d50: cmp ecx, eax`
  - 0x00852d88: je | true=0x00852e79 | false=0x00852d8e
    predicate_hint: `0x00852d84: cmp dword ptr [ebx + 0x48], -1`
  - 0x00852db2: je | true=0x00852e0e | false=0x00852db4
    predicate_hint: `0x00852db0: test edi, edi`
  - 0x00852dfe: jb | true=0x00852e02 | false=0x00852e00
    predicate_hint: `0x00852dfa: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00852e4e: je | true=0x00852e5a | false=0x00852e50
    predicate_hint: `0x00852e4c: cmp ecx, eax`
  - 0x00852e80: je | true=0x00852f6c | false=0x00852e86
    predicate_hint: `0x00852e7c: cmp dword ptr [ebx + 0x4c], -1`
  - 0x00852eaa: je | true=0x00852f06 | false=0x00852eac
    predicate_hint: `0x00852ea8: test edi, edi`
  - 0x00852ef6: jb | true=0x00852efa | false=0x00852ef8
    predicate_hint: `0x00852ef2: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00852f43: je | true=0x00852f4f | false=0x00852f45
    predicate_hint: `0x00852f41: cmp ecx, eax`
  - 0x00852f70: je | true=0x0085305a | false=0x00852f76
    predicate_hint: `0x00852f6c: cmp dword ptr [ebx + 0x50], -1`
  - 0x00852f9a: je | true=0x00852ff6 | false=0x00852f9c
    predicate_hint: `0x00852f98: test edi, edi`
  - 0x00852fe6: jb | true=0x00852fea | false=0x00852fe8
    predicate_hint: `0x00852fe2: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00853033: je | true=0x0085303f | false=0x00853035
    predicate_hint: `0x00853031: cmp ecx, eax`
  - 0x0085307e: je | true=0x008530da | false=0x00853080
    predicate_hint: `0x0085307c: test edi, edi`
  - 0x008530ca: jb | true=0x008530ce | false=0x008530cc
    predicate_hint: `0x008530c6: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0085311a: je | true=0x00853126 | false=0x0085311c
    predicate_hint: `0x00853118: cmp ecx, eax`

### 0x0083c324
- blocks=27, insns=484, edges=56, jcc=25, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0083c353: jne | true=0x0083c347 | false=0x0083c355
    predicate_hint: `0x0083c350: sub ebx, 1`
  - 0x0083c371: jne | true=0x0083c365 | false=0x0083c373
    predicate_hint: `0x0083c36e: sub ebx, 1`
  - 0x0083c39c: jne | true=0x0083c390 | false=0x0083c39e
    predicate_hint: `0x0083c399: sub ebx, 1`
  - 0x0083c3dc: jne | true=0x0083c3d0 | false=0x0083c3de
    predicate_hint: `0x0083c3d9: sub ebx, 1`
  - 0x0083c48c: jne | true=0x0083c480 | false=0x0083c48e
    predicate_hint: `0x0083c489: sub ebx, 1`
  - 0x0083c4ac: jne | true=0x0083c4a0 | false=0x0083c4ae
    predicate_hint: `0x0083c4a9: sub ebx, 1`
  - 0x0083c4cc: jne | true=0x0083c4c0 | false=0x0083c4ce
    predicate_hint: `0x0083c4c9: sub ebx, 1`
  - 0x0083c589: je | true=0x0083c594 | false=0x0083c58b
    predicate_hint: `0x0083c587: cmp ecx, eax`
  - 0x0083c5a2: je | true=0x0083c5ae | false=0x0083c5a4
    predicate_hint: `0x0083c5a0: cmp ecx, eax`
  - 0x0083c5bc: je | true=0x0083c5c8 | false=0x0083c5be
    predicate_hint: `0x0083c5ba: cmp ecx, eax`
  - 0x0083c5d6: je | true=0x0083c5e2 | false=0x0083c5d8
    predicate_hint: `0x0083c5d4: cmp ecx, eax`
  - 0x0083c5f0: je | true=0x0083c5fc | false=0x0083c5f2
    predicate_hint: `0x0083c5ee: cmp ecx, eax`
  - 0x0083c60a: je | true=0x0083c616 | false=0x0083c60c
    predicate_hint: `0x0083c608: cmp ecx, eax`

### 0x0089ab50
- blocks=31, insns=368, edges=80, jcc=24, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0089ab89: jne | true=0x0089aba4 | false=0x0089ab8b
    predicate_hint: `0x0089ab85: cmp byte ptr [esi + 0xd], 0`
  - 0x0089ab93: jae | true=0x0089ab9a | false=0x0089ab95
    predicate_hint: `0x0089ab90: cmp dword ptr [esi + 0x10], edi`
  - 0x0089aba2: je | true=0x0089ab90 | false=0x0089aba4
    predicate_hint: `0x0089ab9e: cmp byte ptr [esi + 0xd], 0`
  - 0x0089aba6: je | true=0x0089abad | false=0x0089aba8
    predicate_hint: `0x0089aba4: cmp eax, edx`
  - 0x0089abab: jae | true=0x0089abaf | false=0x0089abad
    predicate_hint: `0x0089aba8: cmp edi, dword ptr [eax + 0x10]`
  - 0x0089abb1: je | true=0x0089ade8 | false=0x0089abb7
    predicate_hint: `0x0089abaf: cmp eax, edx`
  - 0x0089abbc: je | true=0x0089ade8 | false=0x0089abc2
    predicate_hint: `0x0089abba: test esi, esi`
  - 0x0089abdc: jb | true=0x0089abe0 | false=0x0089abde
    predicate_hint: `0x0089abd5: cmp dword ptr [ebx + 0x40], 0x10`
  - 0x0089abf5: jne | true=0x0089abfb | false=0x0089abf7
    predicate_hint: `0x0089abf2: cmp byte ptr [edx], 0`
  - 0x0089ac05: jne | true=0x0089ac00 | false=0x0089ac07
    predicate_hint: `0x0089ac03: test al, al`
  - 0x0089ac3f: jb | true=0x0089ac4c | false=0x0089ac41
    predicate_hint: `0x0089ac34: cmp dword ptr [ebp - 0x2c], 0x10`
  - 0x0089ac5d: jns | true=0x0089ad4d | false=0x0089ac63
    predicate_hint: `0x0089ac5b: test eax, eax`
  - 0x0089acf4: jb | true=0x0089ad04 | false=0x0089acf6
    predicate_hint: `0x0089ace9: cmp dword ptr [ebp - 0xbc], 0x10`
  - 0x0089ae92: jb | true=0x0089ae9f | false=0x0089ae94
    predicate_hint: `0x0089ae8a: cmp dword ptr [ebp - 0x44], 0x10`
  - 0x0089aee7: jb | true=0x0089aef4 | false=0x0089aee9
    predicate_hint: `0x0089aee3: cmp dword ptr [ebp - 0x68], 0x10`

### 0x008604d7
- blocks=34, insns=350, edges=74, jcc=24, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008604e9: jne | true=0x00860504 | false=0x008604eb
    predicate_hint: `0x008604e2: cmp dword ptr [esi + 0x1e0], 3`
  - 0x00860509: je | true=0x008604eb | false=0x0086050b
    predicate_hint: `0x00860507: test edi, edi`
  - 0x0086050f: je | true=0x00860519 | false=0x00860511
    predicate_hint: `0x0086050b: test byte ptr [esi + 4], 2`
  - 0x00860521: jne | true=0x008604eb | false=0x00860523
    predicate_hint: `0x0086051f: cmp ecx, dword ptr [eax]`
  - 0x00860531: jne | true=0x0086054e | false=0x00860533
    predicate_hint: `0x00860527: test byte ptr [edi + 0x4a], 4`
  - 0x0086053d: je | true=0x0086054e | false=0x0086053f
    predicate_hint: `0x0086053b: cmp eax, ebx`
  - 0x00860554: jne | true=0x00860719 | false=0x0086055a
    predicate_hint: `0x00860551: cmp eax, dword ptr [esi + 0x60]`
  - 0x0086055f: jne | true=0x008604eb | false=0x00860561
    predicate_hint: `0x0086055d: test al, 4`
  - 0x0086058e: jne | true=0x008606c8 | false=0x00860594
    predicate_hint: `0x00860587: cmp dword ptr [esi + 0x1e0], 1`
  - 0x00860598: jne | true=0x008606c8 | false=0x0086059e
    predicate_hint: `0x00860594: test byte ptr [esi + 4], 2`
  - 0x008605a2: je | true=0x008605e2 | false=0x008605a4
    predicate_hint: `0x0086059e: test byte ptr [esi + 5], 0x20`
  - 0x008605f4: je | true=0x008606a7 | false=0x008605fa
    predicate_hint: `0x008605f2: test eax, eax`
  - 0x0086069b: jb | true=0x00860600 | false=0x008606a1
    predicate_hint: `0x00860699: cmp ebx, eax`
  - 0x008606cc: jne | true=0x008605c9 | false=0x008606d2
    predicate_hint: `0x008606c8: test byte ptr [esi + 6], 2`
  - 0x008606d6: jb | true=0x008606f7 | false=0x008606d8
    predicate_hint: `0x008606d2: cmp byte ptr [esi + 5], 0x80`
  - 0x0086071d: jne | true=0x0086075d | false=0x0086071f
    predicate_hint: `0x00860719: cmp byte ptr [ebp + 0x28], 1`
  - 0x00860723: jne | true=0x0086075d | false=0x00860725
    predicate_hint: `0x0086071f: cmp dword ptr [edi + 0x3c], 3`
  - 0x00860761: jne | true=0x008604eb | false=0x00860767
    predicate_hint: `0x0086075d: test byte ptr [edi + 0x4a], 4`
  - 0x0086076b: je | true=0x00860777 | false=0x0086076d
    predicate_hint: `0x00860767: test byte ptr [esi + 4], 2`
  - 0x00860771: je | true=0x008605c9 | false=0x00860777
    predicate_hint: `0x0086076d: test byte ptr [esi + 5], 0x40`

### 0x00865fc0
- blocks=31, insns=385, edges=73, jcc=23, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00865fef: jae | true=0x00866003 | false=0x00865ff1
    predicate_hint: `0x00865fe9: cmp edx, 0x80`
  - 0x00865ff7: je | true=0x00866003 | false=0x00865ff9
    predicate_hint: `0x00865ff5: test ecx, ecx`
  - 0x00866050: jne | true=0x00866192 | false=0x00866056
    predicate_hint: `0x0086604e: cmp ecx, eax`
  - 0x008660ad: jb | true=0x008660b1 | false=0x008660af
    predicate_hint: `0x008660a9: mov byte ptr [ebp - 0x5c], 1`
  - 0x008660c9: jne | true=0x008660cf | false=0x008660cb
    predicate_hint: `0x008660c6: cmp byte ptr [edx], 0`
  - 0x008660d9: jne | true=0x008660d4 | false=0x008660db
    predicate_hint: `0x008660d7: test al, al`
  - 0x0086613b: jb | true=0x0086614b | false=0x0086613d
    predicate_hint: `0x00866133: cmp dword ptr [ebp - 0x78], 0x10`
  - 0x0086617c: jb | true=0x008662f0 | false=0x00866182
    predicate_hint: `0x00866171: cmp dword ptr [ebp - 0x38], 0x10`
  - 0x008661b6: je | true=0x00866212 | false=0x008661b8
    predicate_hint: `0x008661b4: test edi, edi`
  - 0x00866202: jb | true=0x00866206 | false=0x00866204
    predicate_hint: `0x008661fe: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0086623d: jne | true=0x00866243 | false=0x0086623f
    predicate_hint: `0x0086623a: cmp byte ptr [edx], 0`
  - 0x00866255: jne | true=0x00866250 | false=0x00866257
    predicate_hint: `0x00866253: test al, al`
  - 0x008662a1: je | true=0x008662ad | false=0x008662a3
    predicate_hint: `0x0086629f: cmp ecx, eax`
  - 0x008662c1: jb | true=0x008662ce | false=0x008662c3
    predicate_hint: `0x008662b6: cmp dword ptr [ebp - 0x18], 0x10`

### 0x0088f9cf
- blocks=25, insns=297, edges=74, jcc=22, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088f9e3: je | true=0x0088fc60 | false=0x0088f9e9
    predicate_hint: `0x0088f9e1: test eax, eax`
  - 0x0088fa04: je | true=0x0088fc60 | false=0x0088fa0a
    predicate_hint: `0x0088fa02: test ecx, ecx`
  - 0x0088fa39: je | true=0x0088fa57 | false=0x0088fa3b
    predicate_hint: `0x0088fa32: cmp di, word ptr [0xd6ba64]`
  - 0x0088fa42: je | true=0x0088fa57 | false=0x0088fa44
    predicate_hint: `0x0088fa3b: cmp di, word ptr [0xd6ba68]`
  - 0x0088fa55: je | true=0x0088fa62 | false=0x0088fa57
    predicate_hint: `0x0088fa53: test eax, eax`
  - 0x0088fa60: jb | true=0x0088fa20 | false=0x0088fa62
    predicate_hint: `0x0088fa5d: cmp bx, ax`
  - 0x0088fad5: je | true=0x0088fadb | false=0x0088fad7
    predicate_hint: `0x0088fad3: test eax, eax`
  - 0x0088faf2: je | true=0x0088fb14 | false=0x0088faf4
    predicate_hint: `0x0088faf0: test ecx, ecx`
  - 0x0088fafc: jne | true=0x0088fb14 | false=0x0088fafe
    predicate_hint: `0x0088faf7: lock xadd dword ptr [ecx + 4], eax`
  - 0x0088fb0d: jne | true=0x0088fb14 | false=0x0088fb0f
    predicate_hint: `0x0088fb08: lock xadd dword ptr [ecx + 8], eax`
  - 0x0088fb34: je | true=0x0088fb40 | false=0x0088fb36
    predicate_hint: `0x0088fb32: cmp ecx, eax`
  - 0x0088fb4b: je | true=0x0088fb57 | false=0x0088fb4d
    predicate_hint: `0x0088fb49: cmp ecx, eax`
  - 0x0088fb62: je | true=0x0088fb6e | false=0x0088fb64
    predicate_hint: `0x0088fb60: cmp ecx, eax`
  - 0x0088fbe8: je | true=0x0088fc08 | false=0x0088fbea
    predicate_hint: `0x0088fbe2: cmp eax, dword ptr [0xd6ba60]`
  - 0x0088fc17: je | true=0x0088fc31 | false=0x0088fc19
    predicate_hint: `0x0088fc14: cmp ecx, dword ptr [eax + 4]`

### 0x008395da
- blocks=26, insns=307, edges=64, jcc=21, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0083961c: je | true=0x00839622 | false=0x0083961e
    predicate_hint: `0x0083961a: test ebx, ebx`
  - 0x0083962a: je | true=0x0083964b | false=0x0083962c
    predicate_hint: `0x00839628: test edi, edi`
  - 0x00839633: jne | true=0x0083964b | false=0x00839635
    predicate_hint: `0x0083962e: lock xadd dword ptr [edi + 4], eax`
  - 0x00839642: jne | true=0x0083964b | false=0x00839644
    predicate_hint: `0x0083963d: lock xadd dword ptr [edi + 8], eax`
  - 0x008396d3: jb | true=0x008396da | false=0x008396d5
    predicate_hint: `0x008396cf: cmp dword ptr [esi + 0x68], 0x10`
  - 0x0083971e: jb | true=0x00839725 | false=0x00839720
    predicate_hint: `0x00839717: cmp dword ptr [esi + 0x80], 0x10`
  - 0x0083976c: jb | true=0x00839772 | false=0x0083976e
    predicate_hint: `0x00839768: cmp dword ptr [edi + 0x14], 0x10`
  - 0x008397b9: je | true=0x008397d9 | false=0x008397bb
    predicate_hint: `0x008397b7: test edi, edi`
  - 0x008397c2: jne | true=0x008397d9 | false=0x008397c4
    predicate_hint: `0x008397bd: lock xadd dword ptr [edi + 4], eax`
  - 0x008397d0: jne | true=0x008397d9 | false=0x008397d2
    predicate_hint: `0x008397cf: dec ebx`
  - 0x008397e1: jb | true=0x008397ee | false=0x008397e3
    predicate_hint: `0x008397d9: cmp dword ptr [ebp + 0x68], 0x10`
  - 0x0083980b: jb | true=0x00839818 | false=0x0083980d
    predicate_hint: `0x00839800: cmp dword ptr [ebp + 0x80], 0x10`
  - 0x0083983b: jb | true=0x0083984b | false=0x0083983d
    predicate_hint: `0x0083982d: cmp dword ptr [ebp + 0x98], 0x10`

### 0x008e6903
- blocks=28, insns=176, edges=56, jcc=18, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008e690d: je | true=0x008e6924 | false=0x008e690f
    predicate_hint: `0x008e6909: cmp dword ptr [eax + 4], 3`
  - 0x008e692b: jne | true=0x008e6934 | false=0x008e692d
    predicate_hint: `0x008e6924: cmp dword ptr [0xf8bc48], 0`
  - 0x008e6943: jb | true=0x008e6964 | false=0x008e6945
    predicate_hint: `0x008e693f: cmp dword ptr [eax + 8], 3`
  - 0x008e694e: jne | true=0x008e6964 | false=0x008e6950
    predicate_hint: `0x008e6948: cmp eax, dword ptr [0xf8bc5c]`
  - 0x008e696b: jne | true=0x008e6974 | false=0x008e696d
    predicate_hint: `0x008e6964: cmp dword ptr [0xf8bc6c], 0`
  - 0x008e697f: jb | true=0x008e69a0 | false=0x008e6981
    predicate_hint: `0x008e697b: cmp dword ptr [eax + 8], 3`
  - 0x008e698a: jne | true=0x008e69a0 | false=0x008e698c
    predicate_hint: `0x008e6984: cmp eax, dword ptr [0xf8bc80]`
  - 0x008e69a7: jne | true=0x008e69b0 | false=0x008e69a9
    predicate_hint: `0x008e69a0: cmp dword ptr [0xf8d824], 0`
  - 0x008e69bb: jb | true=0x008e69dc | false=0x008e69bd
    predicate_hint: `0x008e69b7: cmp dword ptr [eax + 8], 3`
  - 0x008e69c6: jne | true=0x008e69dc | false=0x008e69c8
    predicate_hint: `0x008e69c0: cmp eax, dword ptr [0xf8d838]`
  - 0x008e69e9: je | true=0x008e6a01 | false=0x008e69eb
    predicate_hint: `0x008e69e7: test al, al`
  - 0x008e6a0e: je | true=0x008e6a24 | false=0x008e6a10
    predicate_hint: `0x008e6a0c: test al, al`
  - 0x008e6a31: je | true=0x008e6a47 | false=0x008e6a33
    predicate_hint: `0x008e6a2f: test al, al`
  - 0x008e6a54: je | true=0x008e6a6a | false=0x008e6a56
    predicate_hint: `0x008e6a52: test al, al`
  - 0x008e6a7a: jne | true=0x008e69ee | false=0x008e6a80
    predicate_hint: `0x008e6a75: test al, al`

### 0x00862c30
- blocks=28, insns=463, edges=65, jcc=17, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00862c6d: jne | true=0x00862ca5 | false=0x00862c6f
    predicate_hint: `0x00862c6a: cmp esi, -1`
  - 0x00862c71: jne | true=0x00862c9f | false=0x00862c73
    predicate_hint: `0x00862c6f: test edi, edi`
  - 0x00862ca9: je | true=0x00862ed7 | false=0x00862caf
    predicate_hint: `0x00862ca5: cmp byte ptr [ebp + 0x1c], 0`
  - 0x00862cda: je | true=0x00862d49 | false=0x00862cdc
    predicate_hint: `0x00862cd8: test edi, edi`
  - 0x00862d39: jb | true=0x00862d3d | false=0x00862d3b
    predicate_hint: `0x00862d35: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00862da3: je | true=0x00862daf | false=0x00862da5
    predicate_hint: `0x00862da1: cmp ecx, eax`
  - 0x00862dd6: je | true=0x00862fb5 | false=0x00862ddc
    predicate_hint: `0x00862dd2: cmp byte ptr [ebp + 0x28], 0`
  - 0x00862e04: je | true=0x00862e50 | false=0x00862e06
    predicate_hint: `0x00862e02: test edi, edi`
  - 0x00862ec2: je | true=0x00862fb5 | false=0x00862ec8
    predicate_hint: `0x00862ec0: test eax, eax`
  - 0x00862eec: jne | true=0x00862f4f | false=0x00862eee
    predicate_hint: `0x00862eea: test ecx, ecx`
  - 0x00862f2e: je | true=0x00862ff0 | false=0x00862f34
    predicate_hint: `0x00862f2c: test edi, edi`
  - 0x00862f78: je | true=0x00862fb5 | false=0x00862f7a
    predicate_hint: `0x00862f74: cmp byte ptr [ebp + 0x28], 0`
  - 0x00862f9d: je | true=0x00862fb5 | false=0x00862f9f
    predicate_hint: `0x00862f9b: test edi, edi`

### 0x00845c30
- blocks=25, insns=347, edges=64, jcc=17, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00845c57: je | true=0x00845f73 | false=0x00845c5d
    predicate_hint: `0x00845c50: cmp dword ptr [ebx + 0x1e8], 0`
  - 0x00845c72: jne | true=0x00845df2 | false=0x00845c78
    predicate_hint: `0x00845c6e: cmp dword ptr [edi + 0x1c], 1`
  - 0x00845c7c: je | true=0x00845da6 | false=0x00845c82
    predicate_hint: `0x00845c78: cmp byte ptr [edi + 0x40], 0`
  - 0x00845cad: je | true=0x00845d1c | false=0x00845caf
    predicate_hint: `0x00845cab: test edi, edi`
  - 0x00845d0c: jb | true=0x00845d10 | false=0x00845d0e
    predicate_hint: `0x00845d08: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00845d74: je | true=0x00845d80 | false=0x00845d76
    predicate_hint: `0x00845d72: cmp ecx, esi`
  - 0x00845dc9: je | true=0x00845df2 | false=0x00845dcb
    predicate_hint: `0x00845dc7: test eax, eax`
  - 0x00845df8: je | true=0x00845f31 | false=0x00845dfe
    predicate_hint: `0x00845df5: cmp eax, 6`
  - 0x00845e00: je | true=0x00845f31 | false=0x00845e06
    predicate_hint: `0x00845dfe: test eax, eax`
  - 0x00845e0a: je | true=0x00845eec | false=0x00845e10
    predicate_hint: `0x00845e06: cmp byte ptr [edi + 0x40], 0`
  - 0x00845e38: je | true=0x00845e84 | false=0x00845e3a
    predicate_hint: `0x00845e36: test esi, esi`
  - 0x00845f0f: je | true=0x00845f31 | false=0x00845f11
    predicate_hint: `0x00845f0d: test eax, eax`
  - 0x00845f6d: jne | true=0x00845c60 | false=0x00845f73
    predicate_hint: `0x00845f66: cmp dword ptr [ebx + 0x1e8], 0`

### 0x00856eb6
- blocks=26, insns=241, edges=62, jcc=16, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00856ec0: je | true=0x00856ee9 | false=0x00856ec2
    predicate_hint: `0x00856eb9: cmp byte ptr [esi + 0x140], 0`
  - 0x00856f0e: jns | true=0x00856fc9 | false=0x00856f14
    predicate_hint: `0x00856f0c: test eax, eax`
  - 0x00856f21: jne | true=0x00856f2c | false=0x00856f23
    predicate_hint: `0x00856f1c: cmp eax, 0xfff0be33`
  - 0x00856f59: jne | true=0x008570bc | false=0x00856f5f
    predicate_hint: `0x00856f52: cmp dword ptr [esi + 0x160], 2`
  - 0x00856f66: jne | true=0x008570bc | false=0x00856f6c
    predicate_hint: `0x00856f5f: cmp dword ptr [esi + 0x164], 0`
  - 0x00856f85: je | true=0x00856f93 | false=0x00856f87
    predicate_hint: `0x00856f83: cmp edi, eax`
  - 0x00857002: jne | true=0x008570b5 | false=0x00857008
    predicate_hint: `0x00856ffb: cmp ax, word ptr [esi + 0x136]`
  - 0x00857015: je | true=0x00857028 | false=0x00857017
    predicate_hint: `0x0085700f: cmp dword ptr [esi + 0x13c], eax`
  - 0x00857041: je | true=0x0085708d | false=0x00857043
    predicate_hint: `0x0085703f: test al, al`
  - 0x0085704c: je | true=0x0085705a | false=0x0085704e
    predicate_hint: `0x0085704a: cmp ebx, eax`
  - 0x00857091: je | true=0x008570b5 | false=0x00857093
    predicate_hint: `0x0085708d: cmp byte ptr [ebp + 0xf], 0`
  - 0x0085709b: je | true=0x008570b5 | false=0x0085709d
    predicate_hint: `0x00857099: test ecx, ecx`
  - 0x008570a5: je | true=0x008570b5 | false=0x008570a7
    predicate_hint: `0x008570a3: test eax, eax`
  - 0x008570a9: jge | true=0x008570b5 | false=0x008570ab
    predicate_hint: `0x008570a7: cmp ecx, eax`

### 0x0069c9d5
- blocks=32, insns=237, edges=72, jcc=16, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069c9e5: je | true=0x0069cbf3 | false=0x0069c9eb
    predicate_hint: `0x0069c9e2: sub eax, 0`
  - 0x0069c9ee: je | true=0x0069cb80 | false=0x0069c9f4
    predicate_hint: `0x0069c9eb: sub eax, 1`
  - 0x0069c9f7: je | true=0x0069cae1 | false=0x0069c9fd
    predicate_hint: `0x0069c9f4: sub eax, 1`
  - 0x0069ca00: je | true=0x0069ca0c | false=0x0069ca02
    predicate_hint: `0x0069c9fd: sub eax, 1`
  - 0x0069ca1b: je | true=0x0069ca9a | false=0x0069ca1d
    predicate_hint: `0x0069ca12: test al, al`
  - 0x0069ca3f: jle | true=0x0069ca44 | false=0x0069ca41
    predicate_hint: `0x0069ca3c: cmp dword ptr [edi + 0x14], eax`
  - 0x0069ca52: jge | true=0x0069ca57 | false=0x0069ca54
    predicate_hint: `0x0069ca4f: cmp dword ptr [edi + 0x14], eax`
  - 0x0069cabc: jle | true=0x0069cac1 | false=0x0069cabe
    predicate_hint: `0x0069cab9: cmp dword ptr [edi + 0x14], eax`
  - 0x0069cacf: jge | true=0x0069cad4 | false=0x0069cad1
    predicate_hint: `0x0069cacc: cmp dword ptr [edi + 0x14], eax`
  - 0x0069caf0: je | true=0x0069cb4f | false=0x0069caf2
    predicate_hint: `0x0069cae7: test al, al`
  - 0x0069cb14: jle | true=0x0069cb19 | false=0x0069cb16
    predicate_hint: `0x0069cb11: cmp dword ptr [edi + 0x14], eax`
  - 0x0069cb71: jle | true=0x0069cb76 | false=0x0069cb73
    predicate_hint: `0x0069cb6e: cmp dword ptr [edi + 0x14], eax`
  - 0x0069cb87: je | true=0x0069cbd0 | false=0x0069cb89
    predicate_hint: `0x0069cb85: test al, al`
  - 0x0069cbd4: jne | true=0x0069cbf3 | false=0x0069cbd6
    predicate_hint: `0x0069cbd0: cmp byte ptr [edi + 0x3d], 0`

### 0x00675d4e
- blocks=26, insns=218, edges=64, jcc=16, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00675d58: jne | true=0x00675f74 | false=0x00675d5e
    predicate_hint: `0x00675d56: test al, al`
  - 0x00675d79: jne | true=0x00675f73 | false=0x00675d7f
    predicate_hint: `0x00675d77: test edx, edx`
  - 0x00675d82: jne | true=0x00675dac | false=0x00675d84
    predicate_hint: `0x00675d7f: cmp byte ptr [edi + 0x10], dl`
  - 0x00675d8a: je | true=0x00675f73 | false=0x00675d90
    predicate_hint: `0x00675d87: cmp eax, dword ptr [edi + 0x38]`
  - 0x00675da4: jle | true=0x00675f73 | false=0x00675daa
    predicate_hint: `0x00675da2: test esi, esi`
  - 0x00675db2: jne | true=0x00675dc0 | false=0x00675db4
    predicate_hint: `0x00675daf: cmp eax, dword ptr [edi + 0x2c]`
  - 0x00675dba: je | true=0x00675f73 | false=0x00675dc0
    predicate_hint: `0x00675db7: cmp eax, dword ptr [edi + 0x38]`
  - 0x00675de7: je | true=0x00675f5b | false=0x00675ded
    predicate_hint: `0x00675de4: cmp dword ptr [ebp - 0x18], ebx`
  - 0x00675df4: je | true=0x00675f5b | false=0x00675dfa
    predicate_hint: `0x00675df2: cmp esi, eax`
  - 0x00675e33: jne | true=0x00675e4e | false=0x00675e35
    predicate_hint: `0x00675e31: test ebx, ebx`
  - 0x00675e48: je | true=0x00675f3e | false=0x00675e4e
    predicate_hint: `0x00675e46: test ebx, ebx`
  - 0x00675e6b: jne | true=0x00675f3e | false=0x00675e71
    predicate_hint: `0x00675e69: test cl, cl`
  - 0x00675ede: jne | true=0x00675ee6 | false=0x00675ee0
    predicate_hint: `0x00675edc: test eax, eax`
  - 0x00675ef7: jne | true=0x00675eff | false=0x00675ef9
    predicate_hint: `0x00675ef5: test eax, eax`
  - 0x00675f25: jne | true=0x00675f48 | false=0x00675f27
    predicate_hint: `0x00675f23: test al, al`

### 0x008908ec
- blocks=20, insns=166, edges=44, jcc=16, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00890910: je | true=0x00890950 | false=0x00890912
    predicate_hint: `0x0089090e: cmp eax, dword ptr [ebx]`
  - 0x00890934: je | true=0x00890950 | false=0x00890936
    predicate_hint: `0x00890931: and bl, 1`
  - 0x0089095a: je | true=0x00890975 | false=0x0089095c
    predicate_hint: `0x00890958: test eax, eax`
  - 0x0089095f: jne | true=0x00890977 | false=0x00890961
    predicate_hint: `0x0089095c: cmp eax, 1`
  - 0x0089096d: jne | true=0x00890977 | false=0x0089096f
    predicate_hint: `0x00890969: cmp dword ptr [eax + 0x10], 0x75`
  - 0x00890973: jne | true=0x00890977 | false=0x00890975
    predicate_hint: `0x0089096f: cmp dword ptr [eax + 0x14], 0`
  - 0x0089097f: je | true=0x0089098b | false=0x00890981
    predicate_hint: `0x0089097d: cmp ecx, edi`
  - 0x00890998: je | true=0x00890a39 | false=0x0089099e
    predicate_hint: `0x00890996: test bl, bl`
  - 0x008909e4: je | true=0x008909f2 | false=0x008909e6
    predicate_hint: `0x008909e2: cmp eax, edi`
  - 0x00890a23: jb | true=0x00890a30 | false=0x00890a25
    predicate_hint: `0x00890a18: cmp dword ptr [ebp - 0x34], 0x10`
  - 0x00890a40: je | true=0x00890a5d | false=0x00890a42
    predicate_hint: `0x00890a3c: cmp byte ptr [ebp - 0xd], 0`

### 0x00890750
- blocks=18, insns=156, edges=37, jcc=16, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00890779: je | true=0x0089089e | false=0x0089077f
    predicate_hint: `0x00890776: cmp esi, dword ptr [ecx + 4]`
  - 0x0089080b: je | true=0x00890817 | false=0x0089080d
    predicate_hint: `0x00890809: cmp ecx, eax`
  - 0x00890837: jb | true=0x00890844 | false=0x00890839
    predicate_hint: `0x0089082c: cmp dword ptr [ebp - 0x24], 0x10`
  - 0x0089084f: jne | true=0x00890892 | false=0x00890851
    predicate_hint: `0x00890844: cmp byte ptr [esi + 0xd], 0`
  - 0x00890858: jne | true=0x00890870 | false=0x0089085a
    predicate_hint: `0x00890854: cmp byte ptr [eax + 0xd], 0`
  - 0x00890862: jne | true=0x00890892 | false=0x00890864
    predicate_hint: `0x0089085e: cmp byte ptr [eax + 0xd], 0`
  - 0x0089086c: je | true=0x00890864 | false=0x0089086e
    predicate_hint: `0x00890868: cmp byte ptr [eax + 0xd], 0`
  - 0x00890877: jne | true=0x00890890 | false=0x00890879
    predicate_hint: `0x00890873: cmp byte ptr [eax + 0xd], 0`
  - 0x00890883: jne | true=0x00890890 | false=0x00890885
    predicate_hint: `0x00890880: cmp esi, dword ptr [eax + 8]`
  - 0x0089088e: je | true=0x00890880 | false=0x00890890
    predicate_hint: `0x0089088a: cmp byte ptr [eax + 0xd], 0`
  - 0x00890898: jne | true=0x00890780 | false=0x0089089e
    predicate_hint: `0x00890895: cmp esi, dword ptr [ecx + 4]`

### 0x005ad530
- blocks=26, insns=497, edges=138, jcc=14, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005ad551: ja | true=0x005ad56a | false=0x005ad553
    predicate_hint: `0x005ad54f: cmp esi, dword ptr [eax]`
  - 0x005ad5b5: jne | true=0x005ad5e0 | false=0x005ad5b7
    predicate_hint: `0x005ad5b3: cmp edx, dword ptr [eax]`
  - 0x005ad5e6: je | true=0x005ad617 | false=0x005ad5e8
    predicate_hint: `0x005ad5e4: test edx, edx`
  - 0x005ad606: jne | true=0x005ad615 | false=0x005ad608
    predicate_hint: `0x005ad604: cmp edx, dword ptr [eax]`
  - 0x005ad635: jne | true=0x005ad644 | false=0x005ad637
    predicate_hint: `0x005ad633: cmp edx, dword ptr [eax]`
  - 0x005ad666: jne | true=0x005ad93a | false=0x005ad66c
    predicate_hint: `0x005ad664: test edx, edx`
  - 0x005ad6a0: jne | true=0x005ad7f0 | false=0x005ad6a6
    predicate_hint: `0x005ad69e: cmp ecx, dword ptr [eax]`
  - 0x005ad6de: jne | true=0x005ad74f | false=0x005ad6e0
    predicate_hint: `0x005ad6dc: test ecx, ecx`
  - 0x005ad76b: jne | true=0x005ad78a | false=0x005ad76d
    predicate_hint: `0x005ad769: cmp ecx, dword ptr [eax]`
  - 0x005ad828: jne | true=0x005ad899 | false=0x005ad82a
    predicate_hint: `0x005ad826: test eax, eax`
  - 0x005ad8b5: jne | true=0x005ad8d4 | false=0x005ad8b7
    predicate_hint: `0x005ad8b3: cmp ecx, dword ptr [eax]`

### 0x00898c43
- blocks=21, insns=308, edges=66, jcc=14, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00898c55: jne | true=0x00898c6b | false=0x00898c57
    predicate_hint: `0x00898c51: cmp byte ptr [esi + 0xd], 0`
  - 0x00898c5a: jae | true=0x00898c61 | false=0x00898c5c
    predicate_hint: `0x00898c57: cmp dword ptr [esi + 0x10], ecx`
  - 0x00898c69: je | true=0x00898c57 | false=0x00898c6b
    predicate_hint: `0x00898c65: cmp byte ptr [esi + 0xd], 0`
  - 0x00898c6d: je | true=0x00898c74 | false=0x00898c6f
    predicate_hint: `0x00898c6b: cmp eax, edx`
  - 0x00898c72: jae | true=0x00898c76 | false=0x00898c74
    predicate_hint: `0x00898c6f: cmp ecx, dword ptr [eax + 0x10]`
  - 0x00898c78: je | true=0x00899002 | false=0x00898c7e
    predicate_hint: `0x00898c76: cmp eax, edx`
  - 0x00898c83: je | true=0x00899002 | false=0x00898c89
    predicate_hint: `0x00898c81: test ebx, ebx`
  - 0x00898ca9: je | true=0x00899002 | false=0x00898caf
    predicate_hint: `0x00898ca6: cmp esi, dword ptr [edi + 0x48]`
  - 0x00898cf7: je | true=0x00898de5 | false=0x00898cfd
    predicate_hint: `0x00898cf5: test eax, eax`
  - 0x00898e1d: js | true=0x00898f43 | false=0x00898e23
    predicate_hint: `0x00898e1b: test eax, eax`
  - 0x00898e2c: jne | true=0x00898f43 | false=0x00898e32
    predicate_hint: `0x00898e29: cmp dword ptr [ebp - 0x10], eax`
  - 0x00898e66: je | true=0x00898f1b | false=0x00898e6c
    predicate_hint: `0x00898e63: cmp dword ptr [eax], 1`

### 0x00896d80
- blocks=17, insns=273, edges=53, jcc=14, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00896db7: je | true=0x00896ed9 | false=0x00896dbd
    predicate_hint: `0x00896da6: cmp dword ptr [esi + 0x4c], 0`
  - 0x00896dfd: jne | true=0x00896e0c | false=0x00896dff
    predicate_hint: `0x00896dfa: cmp eax, dword ptr [ebp - 0x10]`
  - 0x00896e2e: jb | true=0x00896e3e | false=0x00896e30
    predicate_hint: `0x00896e26: cmp dword ptr [ebp - 0x1c], 0x10`
  - 0x00896e45: jne | true=0x00896e54 | false=0x00896e47
    predicate_hint: `0x00896e42: cmp eax, dword ptr [ebp - 0x10]`
  - 0x00896ebd: jb | true=0x00896eca | false=0x00896ebf
    predicate_hint: `0x00896eb5: cmp dword ptr [ebp - 0x1c], 0x10`
  - 0x00896ee5: je | true=0x00897027 | false=0x00896eeb
    predicate_hint: `0x00896edf: cmp eax, dword ptr [esi + 0x110]`
  - 0x00896fb4: je | true=0x00896fc2 | false=0x00896fb6
    predicate_hint: `0x00896fb2: cmp eax, ebx`
  - 0x00896ff6: jb | true=0x00897003 | false=0x00896ff8
    predicate_hint: `0x00896feb: cmp dword ptr [ebp - 0x3c], 0x10`

### 0x0058288e
- blocks=16, insns=106, edges=34, jcc=14, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005828b8: jge | true=0x00582928 | false=0x005828ba
    predicate_hint: `0x005828b6: cmp esi, eax`
  - 0x005828bf: jge | true=0x00582922 | false=0x005828c1
    predicate_hint: `0x005828bd: cmp ebx, ecx`
  - 0x005828c6: jle | true=0x00582917 | false=0x005828c8
    predicate_hint: `0x005828c4: test edi, edi`
  - 0x005828ca: jle | true=0x00582917 | false=0x005828cc
    predicate_hint: `0x005828c8: test esi, esi`
  - 0x005828d4: jge | true=0x00582917 | false=0x005828d6
    predicate_hint: `0x005828d2: cmp edi, eax`
  - 0x005828d8: jge | true=0x00582917 | false=0x005828da
    predicate_hint: `0x005828d6: cmp esi, eax`
  - 0x005828e4: je | true=0x005828f0 | false=0x005828e6
    predicate_hint: `0x005828e2: test al, al`
  - 0x0058291a: jl | true=0x005828c4 | false=0x0058291c
    predicate_hint: `0x00582918: cmp edi, ecx`
  - 0x00582925: jl | true=0x005828bb | false=0x00582927
    predicate_hint: `0x00582923: cmp esi, eax`

### 0x008224f0
- blocks=16, insns=568, edges=37, jcc=13, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00822658: jne | true=0x00822662 | false=0x0082265a
    predicate_hint: `0x00822656: test dl, dl`
  - 0x008226f2: je | true=0x008226fe | false=0x008226f4
    predicate_hint: `0x008226f0: cmp ecx, eax`
  - 0x0082270c: je | true=0x00822718 | false=0x0082270e
    predicate_hint: `0x0082270a: cmp ecx, eax`
  - 0x00822726: je | true=0x00822732 | false=0x00822728
    predicate_hint: `0x00822724: cmp ecx, eax`
  - 0x00822947: je | true=0x00822953 | false=0x00822949
    predicate_hint: `0x00822945: cmp ecx, eax`
  - 0x00822961: je | true=0x0082296d | false=0x00822963
    predicate_hint: `0x0082295f: cmp ecx, eax`
  - 0x0082297b: je | true=0x00822987 | false=0x0082297d
    predicate_hint: `0x00822979: cmp ecx, eax`

### 0x00552615
- blocks=22, insns=328, edges=88, jcc=13, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00552697: je | true=0x005526ad | false=0x00552699
    predicate_hint: `0x00552695: test edi, edi`
  - 0x005526f1: je | true=0x005526ff | false=0x005526f3
    predicate_hint: `0x005526ef: test eax, eax`
  - 0x00552719: je | true=0x00552736 | false=0x0055271b
    predicate_hint: `0x00552717: test eax, eax`
  - 0x0055276e: je | true=0x00552779 | false=0x00552770
    predicate_hint: `0x0055276c: test eax, eax`
  - 0x005527a0: je | true=0x005527af | false=0x005527a2
    predicate_hint: `0x0055279e: test eax, eax`
  - 0x005527dd: je | true=0x005527ec | false=0x005527df
    predicate_hint: `0x005527db: test eax, eax`
  - 0x00552806: je | true=0x00552811 | false=0x00552808
    predicate_hint: `0x00552804: test eax, eax`

### 0x0053e7e1
- blocks=16, insns=121, edges=40, jcc=13, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0053e7e9: je | true=0x0053e8ce | false=0x0053e7ef
    predicate_hint: `0x0053e7e6: cmp dword ptr [esi + 0x30], ebx`
  - 0x0053e808: je | true=0x0053e85a | false=0x0053e80a
    predicate_hint: `0x0053e806: test eax, eax`
  - 0x0053e81d: je | true=0x0053e82f | false=0x0053e81f
    predicate_hint: `0x0053e81a: cmp dword ptr [esi + 0x3c], ebx`
  - 0x0053e840: je | true=0x0053e858 | false=0x0053e842
    predicate_hint: `0x0053e83d: cmp dword ptr [esi + 0x40], ebx`
  - 0x0053e872: je | true=0x0053e89c | false=0x0053e874
    predicate_hint: `0x0053e870: test eax, eax`
  - 0x0053e888: je | true=0x0053e89a | false=0x0053e88a
    predicate_hint: `0x0053e884: cmp dword ptr [esi + 0x44], 0`
  - 0x0053e89e: je | true=0x0053e8cd | false=0x0053e8a0
    predicate_hint: `0x0053e89c: test bl, bl`
  - 0x0053e8bb: je | true=0x0053e8cd | false=0x0053e8bd
    predicate_hint: `0x0053e8b7: cmp dword ptr [esi + 0x48], 0`

### 0x005ad970
- blocks=23, insns=301, edges=73, jcc=11, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005ad9d7: jne | true=0x005adac4 | false=0x005ad9dd
    predicate_hint: `0x005ad9d5: test edx, edx`
  - 0x005ad9e9: je | true=0x005ada43 | false=0x005ad9eb
    predicate_hint: `0x005ad9e7: test ecx, ecx`
  - 0x005ada29: jne | true=0x005ada34 | false=0x005ada2b
    predicate_hint: `0x005ada27: test eax, eax`
  - 0x005ada87: je | true=0x005adaa2 | false=0x005ada89
    predicate_hint: `0x005ada85: test ecx, ecx`
  - 0x005adac6: je | true=0x005adb13 | false=0x005adac8
    predicate_hint: `0x005adac4: xor eax, eax`
  - 0x005adb2e: jne | true=0x005adb32 | false=0x005adb30
    predicate_hint: `0x005adb2c: test eax, eax`
  - 0x005adb50: je | true=0x005adb97 | false=0x005adb52
    predicate_hint: `0x005adb4e: test edx, edx`
  - 0x005adbe8: je | true=0x005adc2f | false=0x005adbea
    predicate_hint: `0x005adbe6: test ecx, ecx`

### 0x00814070
- blocks=17, insns=202, edges=38, jcc=11, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0081409d: je | true=0x00814207 | false=0x008140a3
    predicate_hint: `0x0081409b: test ebx, ebx`
  - 0x008140ce: je | true=0x00814136 | false=0x008140d0
    predicate_hint: `0x008140cc: test esi, esi`
  - 0x00814126: jb | true=0x0081412a | false=0x00814128
    predicate_hint: `0x00814122: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0081415b: jne | true=0x00814161 | false=0x0081415d
    predicate_hint: `0x0081414d: cmp byte ptr [edx], 0`
  - 0x0081416b: jne | true=0x00814166 | false=0x0081416d
    predicate_hint: `0x00814169: test al, al`
  - 0x008141be: je | true=0x008141ca | false=0x008141c0
    predicate_hint: `0x008141bc: cmp ecx, eax`
  - 0x008141dd: jb | true=0x008141ea | false=0x008141df
    predicate_hint: `0x008141d2: cmp dword ptr [ebp - 0x1c], 0x10`

### 0x008856a3
- blocks=13, insns=159, edges=27, jcc=11, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008856c4: je | true=0x008856ca | false=0x008856c6
    predicate_hint: `0x008856c2: test eax, eax`
  - 0x008856d6: je | true=0x008856f9 | false=0x008856d8
    predicate_hint: `0x008856d4: test ebx, ebx`
  - 0x008856e0: jne | true=0x008856f9 | false=0x008856e2
    predicate_hint: `0x008856db: lock xadd dword ptr [ebx + 4], eax`
  - 0x008856f0: jne | true=0x008856f9 | false=0x008856f2
    predicate_hint: `0x008856eb: lock xadd dword ptr [ebx + 8], eax`
  - 0x0088575c: je | true=0x00885768 | false=0x0088575e
    predicate_hint: `0x0088575a: cmp ecx, eax`
  - 0x00885770: je | true=0x0088577c | false=0x00885772
    predicate_hint: `0x0088576e: cmp ecx, eax`
  - 0x0088578a: je | true=0x00885796 | false=0x0088578c
    predicate_hint: `0x00885788: cmp ecx, eax`

### 0x00885423
- blocks=13, insns=127, edges=29, jcc=11, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00885450: je | true=0x00885456 | false=0x00885452
    predicate_hint: `0x0088544e: test eax, eax`
  - 0x00885462: je | true=0x00885485 | false=0x00885464
    predicate_hint: `0x00885460: test ebx, ebx`
  - 0x0088546c: jne | true=0x00885485 | false=0x0088546e
    predicate_hint: `0x00885467: lock xadd dword ptr [ebx + 4], eax`
  - 0x0088547c: jne | true=0x00885485 | false=0x0088547e
    predicate_hint: `0x00885477: lock xadd dword ptr [ebx + 8], eax`
  - 0x0088549a: je | true=0x008854a6 | false=0x0088549c
    predicate_hint: `0x00885498: cmp ecx, eax`
  - 0x008854ae: je | true=0x008854ba | false=0x008854b0
    predicate_hint: `0x008854ac: cmp ecx, eax`
  - 0x008854c2: je | true=0x008854ce | false=0x008854c4
    predicate_hint: `0x008854c0: cmp ecx, eax`

### 0x00890620
- blocks=15, insns=123, edges=28, jcc=11, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0089064f: jne | true=0x00890665 | false=0x00890651
    predicate_hint: `0x0089064b: cmp byte ptr [esi + 0xd], 0`
  - 0x00890654: jae | true=0x0089065b | false=0x00890656
    predicate_hint: `0x00890651: cmp dword ptr [esi + 0x10], edi`
  - 0x00890663: je | true=0x00890651 | false=0x00890665
    predicate_hint: `0x0089065f: cmp byte ptr [esi + 0xd], 0`
  - 0x00890667: je | true=0x0089066e | false=0x00890669
    predicate_hint: `0x00890665: cmp eax, edx`
  - 0x0089066c: jae | true=0x00890670 | false=0x0089066e
    predicate_hint: `0x00890669: cmp edi, dword ptr [eax + 0x10]`
  - 0x00890672: jne | true=0x00890697 | false=0x00890674
    predicate_hint: `0x00890670: cmp eax, edx`
  - 0x008906eb: je | true=0x008906f7 | false=0x008906ed
    predicate_hint: `0x008906e9: cmp ecx, eax`
  - 0x00890727: jb | true=0x00890734 | false=0x00890729
    predicate_hint: `0x0089071c: cmp dword ptr [ebp - 0x20], 0x10`

### 0x007de650
- blocks=15, insns=178, edges=34, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007de694: je | true=0x007de71e | false=0x007de69a
    predicate_hint: `0x007de692: test esi, esi`
  - 0x007de6e4: jb | true=0x007de6e8 | false=0x007de6e6
    predicate_hint: `0x007de6e0: cmp dword ptr [eax + 0x14], 0x10`
  - 0x007de749: jne | true=0x007de74f | false=0x007de74b
    predicate_hint: `0x007de746: cmp byte ptr [edx], 0`
  - 0x007de759: jne | true=0x007de754 | false=0x007de75b
    predicate_hint: `0x007de757: test al, al`
  - 0x007de79b: je | true=0x007de7a7 | false=0x007de79d
    predicate_hint: `0x007de799: cmp ecx, eax`
  - 0x007de7d0: jb | true=0x007de7dd | false=0x007de7d2
    predicate_hint: `0x007de7c5: cmp dword ptr [ebp - 0x14], 0x10`

### 0x0088d7c0
- blocks=15, insns=168, edges=33, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088d80e: je | true=0x0088d876 | false=0x0088d810
    predicate_hint: `0x0088d80c: test edi, edi`
  - 0x0088d866: jb | true=0x0088d86a | false=0x0088d868
    predicate_hint: `0x0088d862: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088d8a1: jne | true=0x0088d8a7 | false=0x0088d8a3
    predicate_hint: `0x0088d89e: cmp byte ptr [edx], 0`
  - 0x0088d8b5: jne | true=0x0088d8b0 | false=0x0088d8b7
    predicate_hint: `0x0088d8b3: test al, al`
  - 0x0088d90c: je | true=0x0088d918 | false=0x0088d90e
    predicate_hint: `0x0088d90a: cmp ecx, eax`
  - 0x0088d926: jb | true=0x0088d933 | false=0x0088d928
    predicate_hint: `0x0088d91b: cmp dword ptr [ebp - 0x1c], 0x10`

### 0x007e1f00
- blocks=15, insns=167, edges=30, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007e1f47: je | true=0x007e1fae | false=0x007e1f49
    predicate_hint: `0x007e1f45: test esi, esi`
  - 0x007e1f9e: jb | true=0x007e1fa2 | false=0x007e1fa0
    predicate_hint: `0x007e1f9a: cmp dword ptr [eax + 0x14], 0x10`
  - 0x007e1fd9: jne | true=0x007e1fdf | false=0x007e1fdb
    predicate_hint: `0x007e1fd6: cmp byte ptr [edx], 0`
  - 0x007e1fe9: jne | true=0x007e1fe4 | false=0x007e1feb
    predicate_hint: `0x007e1fe7: test al, al`
  - 0x007e2036: je | true=0x007e2042 | false=0x007e2038
    predicate_hint: `0x007e2034: cmp ecx, eax`
  - 0x007e2053: jb | true=0x007e2060 | false=0x007e2055
    predicate_hint: `0x007e2048: cmp dword ptr [ebp - 0x18], 0x10`

### 0x00807360
- blocks=15, insns=163, edges=33, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008073ab: je | true=0x00807413 | false=0x008073ad
    predicate_hint: `0x008073a9: test esi, esi`
  - 0x00807403: jb | true=0x00807407 | false=0x00807405
    predicate_hint: `0x008073ff: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0080743e: jne | true=0x00807444 | false=0x00807440
    predicate_hint: `0x0080743b: cmp byte ptr [edx], 0`
  - 0x00807455: jne | true=0x00807450 | false=0x00807457
    predicate_hint: `0x00807453: test al, al`
  - 0x008074a3: je | true=0x008074af | false=0x008074a5
    predicate_hint: `0x008074a1: cmp ecx, eax`
  - 0x008074c0: jb | true=0x008074cd | false=0x008074c2
    predicate_hint: `0x008074b5: cmp dword ptr [ebp - 0x18], 0x10`

### 0x0053416f
- blocks=13, insns=146, edges=35, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00534188: je | true=0x0053423b | false=0x0053418e
    predicate_hint: `0x00534186: test edi, edi`
  - 0x005341c9: jbe | true=0x0053421e | false=0x005341cb
    predicate_hint: `0x005341c7: cmp eax, ecx`
  - 0x005341d6: jae | true=0x005341e0 | false=0x005341d8
    predicate_hint: `0x005341d4: cmp ecx, eax`
  - 0x005341e7: je | true=0x0053420a | false=0x005341e9
    predicate_hint: `0x005341e5: test eax, eax`
  - 0x00534219: jb | true=0x005341cb | false=0x0053421b
    predicate_hint: `0x00534217: cmp ecx, eax`
  - 0x00534234: jne | true=0x00534192 | false=0x0053423a
    predicate_hint: `0x00534232: test edi, edi`

### 0x008600e6
- blocks=14, insns=118, edges=25, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008600f0: je | true=0x008601f2 | false=0x008600f6
    predicate_hint: `0x008600e9: cmp dword ptr [edi + 0x1e0], 3`
  - 0x008600fa: jne | true=0x008601f2 | false=0x00860100
    predicate_hint: `0x008600f6: test byte ptr [edi + 6], 2`
  - 0x00860106: je | true=0x0086010f | false=0x00860108
    predicate_hint: `0x00860104: test esi, esi`
  - 0x0086010d: je | true=0x00860127 | false=0x0086010f
    predicate_hint: `0x0086010b: test al, 4`
  - 0x00860134: je | true=0x0086013c | false=0x00860136
    predicate_hint: `0x00860130: test byte ptr [edi + 4], 2`
  - 0x0086013a: je | true=0x00860140 | false=0x0086013c
    predicate_hint: `0x00860136: test byte ptr [edi + 5], 0x40`
  - 0x00860151: je | true=0x0086015d | false=0x00860153
    predicate_hint: `0x0086014f: cmp ecx, ebx`
  - 0x0086017a: je | true=0x00860195 | false=0x0086017c
    predicate_hint: `0x00860176: test byte ptr [esi + 0x4a], 2`

### 0x00894396
- blocks=15, insns=111, edges=30, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008943a0: jne | true=0x00894481 | false=0x008943a6
    predicate_hint: `0x00894399: cmp dword ptr [esi + 0x838], 0`
  - 0x008943b5: jne | true=0x008943ca | false=0x008943b7
    predicate_hint: `0x008943b3: test ecx, ecx`
  - 0x008943e7: js | true=0x0089449e | false=0x008943ed
    predicate_hint: `0x008943e5: test eax, eax`
  - 0x008943f4: je | true=0x00894498 | false=0x008943fa
    predicate_hint: `0x008943f2: test al, al`
  - 0x00894404: je | true=0x00894498 | false=0x0089440a
    predicate_hint: `0x00894400: cmp dword ptr [eax + 0x4c], 0`
  - 0x00894412: je | true=0x0089441e | false=0x00894414
    predicate_hint: `0x00894410: cmp ecx, eax`
  - 0x0089442c: je | true=0x00894438 | false=0x0089442e
    predicate_hint: `0x0089442a: cmp ecx, eax`
  - 0x0089443f: je | true=0x00894481 | false=0x00894441
    predicate_hint: `0x00894438: cmp dword ptr [esi + 0x864], 0`

### 0x00693aa7
- blocks=15, insns=100, edges=34, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00693aca: je | true=0x00693add | false=0x00693acc
    predicate_hint: `0x00693ac7: cmp byte ptr [ebp - 0x10], bl`
  - 0x00693ae1: jle | true=0x00693b5f | false=0x00693ae3
    predicate_hint: `0x00693ade: cmp dword ptr [esi + 0x20], ebx`
  - 0x00693aee: je | true=0x00693b78 | false=0x00693af4
    predicate_hint: `0x00693aec: test edi, edi`
  - 0x00693b0b: je | true=0x00693b59 | false=0x00693b0d
    predicate_hint: `0x00693b09: test eax, eax`
  - 0x00693b62: je | true=0x00693b6f | false=0x00693b64
    predicate_hint: `0x00693b5f: cmp dword ptr [esi + 0x24], ebx`
  - 0x00693b6d: je | true=0x00693b78 | false=0x00693b6f
    predicate_hint: `0x00693b6b: test al, al`
  - 0x00693b7e: je | true=0x00693ba1 | false=0x00693b80
    predicate_hint: `0x00693b7c: test eax, eax`
  - 0x00693b86: jne | true=0x00693ba1 | false=0x00693b88
    predicate_hint: `0x00693b83: mov dword ptr [esi + 0x24], eax`
  - 0x00693b98: je | true=0x00693ba1 | false=0x00693b9a
    predicate_hint: `0x00693b96: test al, al`

### 0x006373f4
- blocks=11, insns=93, edges=30, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00637452: je | true=0x006374cd | false=0x00637454
    predicate_hint: `0x00637450: test ebx, ebx`
  - 0x0063748b: jle | true=0x006374c1 | false=0x0063748d
    predicate_hint: `0x00637489: test ebx, ebx`
  - 0x006374a1: je | true=0x006374b9 | false=0x006374a3
    predicate_hint: `0x0063749f: test eax, eax`
  - 0x006374a8: je | true=0x006374af | false=0x006374aa
    predicate_hint: `0x006374a6: test ecx, ecx`
  - 0x006374ad: je | true=0x006374b9 | false=0x006374af
    predicate_hint: `0x006374aa: cmp ecx, dword ptr [eax + 0x18]`
  - 0x006374bc: jl | true=0x00637490 | false=0x006374be
    predicate_hint: `0x006374ba: cmp esi, ebx`
  - 0x006374cb: jb | true=0x00637454 | false=0x006374cd
    predicate_hint: `0x006374c8: cmp edi, dword ptr [ebp - 0x14]`

### 0x0086a6e0
- blocks=14, insns=84, edges=26, jcc=10, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0086a6f7: jb | true=0x0086a700 | false=0x0086a6f9
    predicate_hint: `0x0086a6f3: cmp dword ptr [edi + 0x14], 0x10`
  - 0x0086a707: jb | true=0x0086a70d | false=0x0086a709
    predicate_hint: `0x0086a703: cmp dword ptr [esi + 0x14], 0x10`
  - 0x0086a72a: jne | true=0x0086a735 | false=0x0086a72c
    predicate_hint: `0x0086a728: test eax, eax`
  - 0x0086a731: jb | true=0x0086a735 | false=0x0086a733
    predicate_hint: `0x0086a72f: cmp eax, ebx`
  - 0x0086a733: jbe | true=0x0086a757 | false=0x0086a735
  - 0x0086a737: je | true=0x0086a745 | false=0x0086a739
    predicate_hint: `0x0086a735: cmp esi, edi`
  - 0x0086a74c: je | true=0x0086a757 | false=0x0086a74e
    predicate_hint: `0x0086a748: cmp byte ptr [ecx + 0x15], 0`

### 0x005804f4
- blocks=11, insns=76, edges=22, jcc=9, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedBuildingAreasPredicate@EGL@@
- branch conditions:
  - 0x00580511: jg | true=0x00580585 | false=0x00580513
    predicate_hint: `0x0058050f: cmp esi, eax`
  - 0x0058051e: je | true=0x0058057a | false=0x00580520
    predicate_hint: `0x0058051c: test bl, bl`
  - 0x00580526: jg | true=0x0058057a | false=0x00580528
    predicate_hint: `0x00580524: cmp edi, eax`
  - 0x00580548: je | true=0x0058054e | false=0x0058054a
    predicate_hint: `0x00580545: cmp eax, dword ptr [ecx + 0x28]`
  - 0x00580578: jne | true=0x00580524 | false=0x0058057a
    predicate_hint: `0x00580576: test bl, bl`
  - 0x00580583: jne | true=0x0058050f | false=0x00580585
    predicate_hint: `0x00580581: test bl, bl`

### 0x00843ec0
- blocks=18, insns=324, edges=46, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00843f01: jne | true=0x00843fa0 | false=0x00843f07
    predicate_hint: `0x00843efe: cmp eax, 1`
  - 0x00843f1e: je | true=0x00843f29 | false=0x00843f20
    predicate_hint: `0x00843f1c: test eax, eax`
  - 0x00843fa7: jne | true=0x00844064 | false=0x00843fad
    predicate_hint: `0x00843fa0: cmp dword ptr [ebx + 0x108], -1`
  - 0x00843fc4: je | true=0x00843fcf | false=0x00843fc6
    predicate_hint: `0x00843fc2: test eax, eax`
  - 0x0084403f: je | true=0x0084404b | false=0x00844041
    predicate_hint: `0x0084403d: cmp ecx, eax`
  - 0x0084407b: je | true=0x00844086 | false=0x0084407d
    predicate_hint: `0x00844079: test eax, eax`
  - 0x00844108: je | true=0x00844114 | false=0x0084410a
    predicate_hint: `0x00844106: cmp ecx, eax`

### 0x00887c20
- blocks=14, insns=166, edges=40, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00887c45: je | true=0x00887d76 | false=0x00887c4b
    predicate_hint: `0x00887c43: test esi, esi`
  - 0x00887c52: jne | true=0x00887c5b | false=0x00887c54
    predicate_hint: `0x00887c4b: cmp dword ptr [0xf8fd24], 0`
  - 0x00887c66: jb | true=0x00887d76 | false=0x00887c6c
    predicate_hint: `0x00887c62: cmp dword ptr [eax + 8], 3`
  - 0x00887c75: jne | true=0x00887d76 | false=0x00887c7b
    predicate_hint: `0x00887c6f: cmp eax, dword ptr [0xf8fd38]`
  - 0x00887c83: je | true=0x00887c91 | false=0x00887c85
    predicate_hint: `0x00887c81: cmp eax, ecx`
  - 0x00887caa: jne | true=0x00887d64 | false=0x00887cb0
    predicate_hint: `0x00887ca4: cmp eax, dword ptr [0xd6ba18]`
  - 0x00887d20: je | true=0x00887d2c | false=0x00887d22
    predicate_hint: `0x00887d1e: cmp ecx, eax`

### 0x00887e70
- blocks=14, insns=158, edges=37, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00887e95: je | true=0x00887fb8 | false=0x00887e9b
    predicate_hint: `0x00887e93: test esi, esi`
  - 0x00887ea2: jne | true=0x00887eab | false=0x00887ea4
    predicate_hint: `0x00887e9b: cmp dword ptr [0xf8fd48], 0`
  - 0x00887eb6: jb | true=0x00887fb8 | false=0x00887ebc
    predicate_hint: `0x00887eb2: cmp dword ptr [eax + 8], 3`
  - 0x00887ec5: jne | true=0x00887fb8 | false=0x00887ecb
    predicate_hint: `0x00887ebf: cmp eax, dword ptr [0xf8fd5c]`
  - 0x00887ed3: je | true=0x00887ee1 | false=0x00887ed5
    predicate_hint: `0x00887ed1: cmp eax, ecx`
  - 0x00887efa: jne | true=0x00887fad | false=0x00887f00
    predicate_hint: `0x00887ef4: cmp eax, dword ptr [0xd6ba18]`
  - 0x00887f70: je | true=0x00887f7c | false=0x00887f72
    predicate_hint: `0x00887f6e: cmp ecx, eax`

### 0x006342eb
- blocks=12, insns=134, edges=36, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063435f: je | true=0x006343a8 | false=0x00634361
    predicate_hint: `0x00634355: cmp dword ptr [ebx + 0x60], 0`
  - 0x00634365: jne | true=0x00634391 | false=0x00634367
    predicate_hint: `0x00634361: cmp dword ptr [ebx + 0x60], 1`
  - 0x0063438f: je | true=0x006343a5 | false=0x00634391
    predicate_hint: `0x0063438c: cmp ax, si`
  - 0x006343d4: jle | true=0x00634415 | false=0x006343d6
    predicate_hint: `0x006343d1: cmp eax, 1`
  - 0x006343f6: je | true=0x00634415 | false=0x006343f8
    predicate_hint: `0x006343f4: test al, al`
  - 0x00634413: jne | true=0x006343eb | false=0x00634415
    predicate_hint: `0x00634411: cmp ecx, dword ptr [eax]`

### 0x00699bad
- blocks=11, insns=118, edges=34, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00699bcd: jne | true=0x00699c00 | false=0x00699bcf
    predicate_hint: `0x00699bcb: cmp eax, ebx`
  - 0x00699be4: je | true=0x00699c00 | false=0x00699be6
    predicate_hint: `0x00699be2: test eax, eax`
  - 0x00699c0f: je | true=0x00699c3c | false=0x00699c11
    predicate_hint: `0x00699c0d: test al, al`
  - 0x00699c48: je | true=0x00699c78 | false=0x00699c4a
    predicate_hint: `0x00699c46: test al, al`
  - 0x00699c84: je | true=0x00699ca0 | false=0x00699c86
    predicate_hint: `0x00699c82: test al, al`
  - 0x00699c91: jne | true=0x00699ca0 | false=0x00699c93
    predicate_hint: `0x00699c89: cmp dword ptr [eax*4 + 0xbe1434], 1`

### 0x007f6bd0
- blocks=14, insns=113, edges=27, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007f6be9: jb | true=0x007f6bf2 | false=0x007f6beb
    predicate_hint: `0x007f6be6: cmp ecx, 0x10`
  - 0x007f6bf8: jb | true=0x007f6bfe | false=0x007f6bfa
    predicate_hint: `0x007f6bf5: cmp ecx, 0x10`
  - 0x007f6c08: jb | true=0x007f6c0e | false=0x007f6c0a
    predicate_hint: `0x007f6c05: cmp ecx, 0x10`
  - 0x007f6c22: je | true=0x007f6c41 | false=0x007f6c24
    predicate_hint: `0x007f6c20: test ecx, ecx`
  - 0x007f6c3c: jne | true=0x007f6c26 | false=0x007f6c3e
    predicate_hint: `0x007f6c3a: cmp esi, edi`

### 0x00888ef0
- blocks=13, insns=87, edges=28, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00888efe: jne | true=0x00888f07 | false=0x00888f00
    predicate_hint: `0x00888efc: mov esi, ecx`
  - 0x00888f15: jb | true=0x00888f45 | false=0x00888f17
    predicate_hint: `0x00888f11: cmp dword ptr [eax + 8], 3`
  - 0x00888f20: jne | true=0x00888f45 | false=0x00888f22
    predicate_hint: `0x00888f1a: cmp eax, dword ptr [0xf8fc84]`
  - 0x00888f4c: jne | true=0x00888f55 | false=0x00888f4e
    predicate_hint: `0x00888f45: cmp dword ptr [0xf8fc94], 0`
  - 0x00888f60: jb | true=0x00888fa4 | false=0x00888f62
    predicate_hint: `0x00888f5c: cmp dword ptr [eax + 8], 3`
  - 0x00888f6b: jne | true=0x00888fa4 | false=0x00888f6d
    predicate_hint: `0x00888f65: cmp eax, dword ptr [0xf8fca8]`
  - 0x00888f7b: je | true=0x00888f87 | false=0x00888f7d
    predicate_hint: `0x00888f79: cmp ecx, edi`

### 0x005c4dd0
- blocks=16, insns=78, edges=34, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c4de4: jae | true=0x005c4dee | false=0x005c4de6
    predicate_hint: `0x005c4de1: cmp eax, dword ptr [ebp + 8]`
  - 0x005c4dfb: jae | true=0x005c4e16 | false=0x005c4dfd
    predicate_hint: `0x005c4df8: cmp eax, dword ptr [ebp + 8]`
  - 0x005c4e1c: je | true=0x005c4e58 | false=0x005c4e1e
    predicate_hint: `0x005c4e1a: test eax, eax`
  - 0x005c4e22: jae | true=0x005c4e58 | false=0x005c4e24
    predicate_hint: `0x005c4e1e: cmp dword ptr [ebp + 8], 0x10`
  - 0x005c4e31: jae | true=0x005c4e3b | false=0x005c4e33
    predicate_hint: `0x005c4e2f: cmp ecx, dword ptr [eax]`
  - 0x005c4e5c: jne | true=0x005c4e68 | false=0x005c4e5e
    predicate_hint: `0x005c4e58: cmp dword ptr [ebp + 8], 0`
  - 0x005c4e6c: jbe | true=0x005c4e77 | false=0x005c4e6e
    predicate_hint: `0x005c4e68: cmp dword ptr [ebp + 8], 0`

### 0x0069ae9e
- blocks=12, insns=63, edges=26, jcc=9, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069aea5: jne | true=0x0069af46 | false=0x0069aeab
    predicate_hint: `0x0069aea1: cmp byte ptr [edi + 0x3d], 0`
  - 0x0069aebb: je | true=0x0069aef8 | false=0x0069aebd
    predicate_hint: `0x0069aeb7: cmp dword ptr [eax + 0x7c], 0`
  - 0x0069aed0: je | true=0x0069aef8 | false=0x0069aed2
    predicate_hint: `0x0069aece: test eax, eax`
  - 0x0069aef6: je | true=0x0069af45 | false=0x0069aef8
    predicate_hint: `0x0069aef3: cmp esi, eax`
  - 0x0069af29: jne | true=0x0069af3e | false=0x0069af2b
    predicate_hint: `0x0069af25: cmp dword ptr [edi + 0x20], -1`
  - 0x0069af33: jne | true=0x0069af38 | false=0x0069af35
    predicate_hint: `0x0069af2b: cmp dword ptr [eax*4 + 0xbe1434], 0`
  - 0x0069af3c: jl | true=0x0069af25 | false=0x0069af3e
    predicate_hint: `0x0069af39: cmp eax, 6`

### 0x00899970
- blocks=12, insns=174, edges=26, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008999c2: je | true=0x00899a3c | false=0x008999c4
    predicate_hint: `0x008999c0: test edi, edi`
  - 0x00899a2c: jb | true=0x00899a30 | false=0x00899a2e
    predicate_hint: `0x00899a28: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00899abe: je | true=0x00899aca | false=0x00899ac0
    predicate_hint: `0x00899abc: cmp ecx, eax`
  - 0x00899ada: jb | true=0x00899ae7 | false=0x00899adc
    predicate_hint: `0x00899ad2: cmp dword ptr [ebp - 0x18], 0x10`
  - 0x00899b0a: je | true=0x00899b24 | false=0x00899b0c
    predicate_hint: `0x00899b08: test ecx, ecx`

### 0x0057624f
- blocks=10, insns=84, edges=18, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00576257: jne | true=0x0057626d | false=0x00576259
    predicate_hint: `0x00576253: test byte ptr [esi + 0xc], 1`
  - 0x00576264: ja | true=0x0057626d | false=0x00576266
    predicate_hint: `0x00576261: cmp dword ptr [esi + 8], eax`
  - 0x0057627d: jne | true=0x00576284 | false=0x0057627f
    predicate_hint: `0x0057627a: mov edi, dword ptr [esi + 0xc]`
  - 0x00576297: jne | true=0x005762ad | false=0x00576299
    predicate_hint: `0x00576293: cmp dword ptr [eax + ebx*4], 0`
  - 0x005762be: je | true=0x005762cd | false=0x005762c0
    predicate_hint: `0x005762bc: test edx, edx`

### 0x005a4bf0
- blocks=15, insns=70, edges=27, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005a4bfe: jne | true=0x005a4c05 | false=0x005a4c00
    predicate_hint: `0x005a4bfa: cmp dword ptr [eax + 0x18], 5`
  - 0x005a4c0c: jne | true=0x005a4c20 | false=0x005a4c0e
    predicate_hint: `0x005a4c08: cmp dword ptr [ecx + 0x14], 0xc`
  - 0x005a4c15: je | true=0x005a4c32 | false=0x005a4c17
    predicate_hint: `0x005a4c11: cmp dword ptr [edx + 0x18], 3`
  - 0x005a4c1e: je | true=0x005a4c32 | false=0x005a4c20
    predicate_hint: `0x005a4c1a: cmp dword ptr [eax + 0x18], 2`
  - 0x005a4c4a: jne | true=0x005a4c5b | false=0x005a4c4c
    predicate_hint: `0x005a4c48: test eax, eax`
  - 0x005a4c6f: jne | true=0x005a4c80 | false=0x005a4c71
    predicate_hint: `0x005a4c6d: test edx, edx`
  - 0x005a4c92: jne | true=0x005a4ca0 | false=0x005a4c94
    predicate_hint: `0x005a4c8e: cmp dword ptr [eax + 0x18], 3`
  - 0x005a4ca7: jne | true=0x005a4cb3 | false=0x005a4ca9
    predicate_hint: `0x005a4ca3: cmp dword ptr [edx + 0x18], 2`

### 0x006164a9
- blocks=11, insns=54, edges=19, jcc=8, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006164b2: je | true=0x00616512 | false=0x006164b4
    predicate_hint: `0x006164af: cmp eax, dword ptr [esi + 0x28]`
  - 0x006164b8: je | true=0x006164ca | false=0x006164ba
    predicate_hint: `0x006164b4: cmp dword ptr [esi + 4], -1`
  - 0x006164c8: jbe | true=0x00616512 | false=0x006164ca
    predicate_hint: `0x006164c1: comiss xmm0, dword ptr [0xbbf608]`
  - 0x006164dc: je | true=0x006164f6 | false=0x006164de
    predicate_hint: `0x006164da: test eax, eax`
  - 0x006164e2: jb | true=0x006164e6 | false=0x006164e4
    predicate_hint: `0x006164de: cmp dword ptr [edi + 0x14], 0x10`
  - 0x006164f4: jne | true=0x00616511 | false=0x006164f6
    predicate_hint: `0x006164f1: cmp eax, 1`
  - 0x00616508: jl | true=0x00616511 | false=0x0061650a
    predicate_hint: `0x00616505: cmp dword ptr [esi + 4], eax`

### 0x0069c652
- blocks=8, insns=63, edges=22, jcc=7, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - 0x0069c677: je | true=0x0069c6ab | false=0x0069c679
    predicate_hint: `0x0069c675: test ebx, ebx`
  - 0x0069c6c1: jne | true=0x0069c6d6 | false=0x0069c6c3
    predicate_hint: `0x0069c6bd: cmp dword ptr [edi + 0x20], -1`
  - 0x0069c6cb: jne | true=0x0069c6d0 | false=0x0069c6cd
    predicate_hint: `0x0069c6c3: cmp dword ptr [esi*4 + 0xbe1434], -1`
  - 0x0069c6d4: jl | true=0x0069c6bd | false=0x0069c6d6
    predicate_hint: `0x0069c6d1: cmp esi, 6`

### 0x005ac180
- blocks=15, insns=185, edges=64, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005ac1bd: jbe | true=0x005ac1db | false=0x005ac1bf
    predicate_hint: `0x005ac1bb: test eax, eax`
  - 0x005ac211: je | true=0x005ac300 | false=0x005ac217
    predicate_hint: `0x005ac20f: test eax, eax`
  - 0x005ac223: jne | true=0x005ac260 | false=0x005ac225
    predicate_hint: `0x005ac21f: cmp dword ptr [eax + 0x1c], 1`
  - 0x005ac26c: jne | true=0x005ac2b2 | false=0x005ac26e
    predicate_hint: `0x005ac268: cmp dword ptr [eax + 0x20], 1`
  - 0x005ac30a: jbe | true=0x005ac33f | false=0x005ac30c
    predicate_hint: `0x005ac308: test eax, eax`
  - 0x005ac31f: je | true=0x005ac33f | false=0x005ac321
    predicate_hint: `0x005ac31d: test ecx, ecx`

### 0x0058012c
- blocks=9, insns=155, edges=24, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005801ef: jns | true=0x005801f6 | false=0x005801f1
    predicate_hint: `0x005801e9: and ebx, 0x80000003`
  - 0x005801fe: je | true=0x0058023e | false=0x00580200
    predicate_hint: `0x005801fa: cmp dword ptr [ebp + eax*4 - 0x24], edx`
  - 0x00580243: jl | true=0x005801e1 | false=0x00580245
    predicate_hint: `0x00580240: cmp eax, 4`
  - 0x00580267: je | true=0x00580273 | false=0x00580269
    predicate_hint: `0x00580263: cmp dword ptr [edi + 4], 0`

### 0x005b8190
- blocks=15, insns=144, edges=46, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005b81ed: je | true=0x005b821d | false=0x005b81ef
    predicate_hint: `0x005b81eb: test edx, edx`
  - 0x005b820d: jge | true=0x005b821b | false=0x005b820f
    predicate_hint: `0x005b820a: cmp ecx, dword ptr [ebp + 8]`
  - 0x005b824d: je | true=0x005b82ed | false=0x005b8253
    predicate_hint: `0x005b824b: test edx, edx`
  - 0x005b82a8: je | true=0x005b82e8 | false=0x005b82aa
    predicate_hint: `0x005b82a6: test edx, edx`
  - 0x005b82d0: je | true=0x005b82e1 | false=0x005b82d2
    predicate_hint: `0x005b82cc: cmp dword ptr [ebp - 0x28], 0`

### 0x00576019
- blocks=12, insns=128, edges=26, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00576035: jb | true=0x0057603c | false=0x00576037
    predicate_hint: `0x00576032: cmp eax, dword ptr [ebp + 8]`
  - 0x0057603a: jae | true=0x0057604f | false=0x0057603c
    predicate_hint: `0x00576037: cmp edi, 8`
  - 0x00576045: jb | true=0x00576123 | false=0x0057604b
    predicate_hint: `0x00576043: cmp eax, edi`
  - 0x00576091: ja | true=0x005760c7 | false=0x00576093
    predicate_hint: `0x0057608f: cmp eax, edi`
  - 0x00576102: je | true=0x00576114 | false=0x00576104
    predicate_hint: `0x005760fe: cmp dword ptr [ebx + 4], 0`

### 0x0060d008
- blocks=12, insns=123, edges=26, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060d023: jb | true=0x0060d02a | false=0x0060d025
    predicate_hint: `0x0060d020: cmp eax, dword ptr [ebp + 8]`
  - 0x0060d028: jae | true=0x0060d03d | false=0x0060d02a
    predicate_hint: `0x0060d025: cmp edi, 8`
  - 0x0060d033: jb | true=0x0060d107 | false=0x0060d039
    predicate_hint: `0x0060d031: cmp eax, edi`
  - 0x0060d079: ja | true=0x0060d0ac | false=0x0060d07b
    predicate_hint: `0x0060d077: cmp ecx, edi`
  - 0x0060d0e6: je | true=0x0060d0f8 | false=0x0060d0e8
    predicate_hint: `0x0060d0e2: cmp dword ptr [ebx + 4], 0`

### 0x0065b4db
- blocks=14, insns=121, edges=24, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065b4e6: je | true=0x0065b593 | false=0x0065b4ec
    predicate_hint: `0x0065b4e4: cmp edi, ebx`
  - 0x0065b4f1: jne | true=0x0065b4fa | false=0x0065b4f3
    predicate_hint: `0x0065b4ee: cmp eax, dword ptr [ebx + 4]`
  - 0x0065b50c: ja | true=0x0065b52b | false=0x0065b50e
    predicate_hint: `0x0065b50a: cmp edx, esi`
  - 0x0065b535: ja | true=0x0065b552 | false=0x0065b537
    predicate_hint: `0x0065b533: cmp edx, ecx`
  - 0x0065b555: je | true=0x0065b564 | false=0x0065b557
    predicate_hint: `0x0065b552: cmp dword ptr [edi], 0`
  - 0x0065b576: je | true=0x0065b593 | false=0x0065b578
    predicate_hint: `0x0065b574: test al, al`

### 0x0085ed08
- blocks=11, insns=114, edges=19, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0085ed12: je | true=0x0085ede9 | false=0x0085ed18
    predicate_hint: `0x0085ed0b: cmp dword ptr [edi + 0x1e0], 3`
  - 0x0085ed31: jne | true=0x0085ede9 | false=0x0085ed37
    predicate_hint: `0x0085ed2f: cmp dword ptr [ebx], eax`
  - 0x0085ed3b: jne | true=0x0085ede9 | false=0x0085ed41
    predicate_hint: `0x0085ed37: test byte ptr [edi + 6], 2`
  - 0x0085ed55: je | true=0x0085ede9 | false=0x0085ed5b
    predicate_hint: `0x0085ed53: test esi, esi`
  - 0x0085ed78: je | true=0x0085ed8c | false=0x0085ed7a
    predicate_hint: `0x0085ed76: cmp eax, ecx`
  - 0x0085ed9f: je | true=0x0085eda7 | false=0x0085eda1
    predicate_hint: `0x0085ed9d: test eax, eax`

### 0x00577c3d
- blocks=14, insns=99, edges=24, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00577c42: je | true=0x00577ced | false=0x00577c48
    predicate_hint: `0x00577c40: cmp edi, ebx`
  - 0x00577c4d: jne | true=0x00577c59 | false=0x00577c4f
    predicate_hint: `0x00577c4a: cmp ecx, dword ptr [ebx + 4]`
  - 0x00577c6c: ja | true=0x00577c8b | false=0x00577c6e
    predicate_hint: `0x00577c6a: cmp edx, esi`
  - 0x00577c95: ja | true=0x00577cb4 | false=0x00577c97
    predicate_hint: `0x00577c93: cmp edx, eax`
  - 0x00577cb7: je | true=0x00577cc6 | false=0x00577cb9
    predicate_hint: `0x00577cb4: cmp dword ptr [edi], 0`
  - 0x00577cd8: je | true=0x00577cec | false=0x00577cda
    predicate_hint: `0x00577cd6: test al, al`

### 0x00559d42
- blocks=9, insns=69, edges=20, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00559d60: je | true=0x00559d7d | false=0x00559d62
    predicate_hint: `0x00559d5e: test ebx, ebx`
  - 0x00559d6f: je | true=0x00559d75 | false=0x00559d71
    predicate_hint: `0x00559d6d: test eax, eax`
  - 0x00559d7b: jb | true=0x00559d62 | false=0x00559d7d
    predicate_hint: `0x00559d79: cmp edi, ebx`
  - 0x00559d82: je | true=0x00559d8e | false=0x00559d84
    predicate_hint: `0x00559d80: test ecx, ecx`
  - 0x00559d93: je | true=0x00559d9f | false=0x00559d95
    predicate_hint: `0x00559d91: test ecx, ecx`

### 0x008570e0
- blocks=10, insns=66, edges=22, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008570f3: jne | true=0x00857155 | false=0x008570f5
    predicate_hint: `0x008570f1: test eax, eax`
  - 0x00857102: je | true=0x00857155 | false=0x00857104
    predicate_hint: `0x008570fc: cmp dword ptr [esi + 0x138], eax`
  - 0x00857120: je | true=0x0085712c | false=0x00857122
    predicate_hint: `0x0085711e: cmp ecx, eax`
  - 0x00857134: je | true=0x0085714e | false=0x00857136
    predicate_hint: `0x00857132: test eax, eax`
  - 0x0085713e: je | true=0x0085714e | false=0x00857140
    predicate_hint: `0x0085713c: test ecx, ecx`
  - 0x00857142: jge | true=0x0085714e | false=0x00857144
    predicate_hint: `0x00857140: cmp eax, ecx`

### 0x005558d0
- blocks=10, insns=61, edges=18, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005558de: je | true=0x00555934 | false=0x005558e0
    predicate_hint: `0x005558dc: test al, al`
  - 0x005558fb: je | true=0x0055592d | false=0x005558fd
    predicate_hint: `0x005558f9: test edi, edi`
  - 0x00555917: je | true=0x00555924 | false=0x00555919
    predicate_hint: `0x00555915: test ecx, ecx`
  - 0x0055591d: je | true=0x00555924 | false=0x0055591f
    predicate_hint: `0x00555919: cmp byte ptr [ecx + 5], 0`
  - 0x0055592a: jne | true=0x00555900 | false=0x0055592c
    predicate_hint: `0x00555927: sub edi, 1`

### 0x00531750
- blocks=10, insns=49, edges=18, jcc=7, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00531758: je | true=0x005317ac | false=0x0053175a
    predicate_hint: `0x00531756: test ecx, ecx`
  - 0x00531767: je | true=0x005317ac | false=0x00531769
    predicate_hint: `0x00531765: test eax, eax`
  - 0x00531788: je | true=0x0053178f | false=0x0053178a
    predicate_hint: `0x00531785: cmp eax, dword ptr [esi + 4]`
  - 0x0053178d: jge | true=0x00531792 | false=0x0053178f
    predicate_hint: `0x0053178a: cmp edi, dword ptr [eax + 0x10]`
  - 0x00531795: je | true=0x005317aa | false=0x00531797
    predicate_hint: `0x00531792: cmp eax, dword ptr [esi + 4]`
  - 0x0053179b: jne | true=0x005317aa | false=0x0053179d
    predicate_hint: `0x00531797: cmp byte ptr [eax + 0x18], 0`

### 0x00574ef4
- blocks=10, insns=178, edges=26, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00574f03: je | true=0x00574f0c | false=0x00574f05
    predicate_hint: `0x00574eff: cmp byte ptr [esi + 0x5e], 0`
  - 0x00574ff1: je | true=0x0057500e | false=0x00574ff3
    predicate_hint: `0x00574fef: test eax, eax`
  - 0x00574ffc: je | true=0x0057500e | false=0x00574ffe
    predicate_hint: `0x00574ffa: test eax, eax`
  - 0x00575062: jne | true=0x00575054 | false=0x00575064
    predicate_hint: `0x0057505f: cmp esi, dword ptr [ebx + 0x6c]`

### 0x0055dd7c
- blocks=12, insns=136, edges=29, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055dd8c: jne | true=0x0055de8c | false=0x0055dd92
    predicate_hint: `0x0055dd85: test dword ptr [ebx + 4], 0x8000000`
  - 0x0055ddad: je | true=0x0055ddfc | false=0x0055ddaf
    predicate_hint: `0x0055ddab: cmp ecx, eax`
  - 0x0055ddd7: jb | true=0x0055ddde | false=0x0055ddd9
    predicate_hint: `0x0055ddd4: comiss xmm2, xmm1`
  - 0x0055dde8: jb | true=0x0055ddef | false=0x0055ddea
    predicate_hint: `0x0055dde5: comiss xmm1, xmm0`
  - 0x0055de4a: je | true=0x0055de55 | false=0x0055de4c
    predicate_hint: `0x0055de46: cmp byte ptr [ebp - 0x30], 0`

### 0x006c5a1f
- blocks=8, insns=128, edges=35, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006c5ae9: jb | true=0x006c5aed | false=0x006c5aeb
    predicate_hint: `0x006c5ae5: cmp dword ptr [edi + 0x14], 0x10`
  - 0x006c5b17: jne | true=0x006c5b27 | false=0x006c5b19
    predicate_hint: `0x006c5b15: test al, al`
  - 0x006c5b34: jne | true=0x006c5a68 | false=0x006c5b3a
    predicate_hint: `0x006c5b32: cmp edi, ebx`

### 0x00581d66
- blocks=9, insns=88, edges=20, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00581d74: je | true=0x00581d80 | false=0x00581d76
    predicate_hint: `0x00581d72: mov esi, ecx`
  - 0x00581d8d: jle | true=0x00581db6 | false=0x00581d8f
    predicate_hint: `0x00581d8b: test ebx, ebx`
  - 0x00581d96: jle | true=0x00581db1 | false=0x00581d98
    predicate_hint: `0x00581d94: test ebx, ebx`
  - 0x00581daf: jl | true=0x00581d98 | false=0x00581db1
    predicate_hint: `0x00581dad: cmp eax, ebx`
  - 0x00581db4: jl | true=0x00581d8f | false=0x00581db6
    predicate_hint: `0x00581db2: cmp edi, ebx`
  - 0x00581de5: je | true=0x00581df4 | false=0x00581de7
    predicate_hint: `0x00581de1: cmp byte ptr [ebp + 8], 0`

### 0x005761c7
- blocks=8, insns=80, edges=14, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005761d4: jne | true=0x005761e9 | false=0x005761d6
    predicate_hint: `0x005761d2: test al, 1`
  - 0x005761de: ja | true=0x005761e9 | false=0x005761e0
    predicate_hint: `0x005761db: cmp dword ptr [esi + 8], eax`
  - 0x0057620f: jne | true=0x00576225 | false=0x00576211
    predicate_hint: `0x0057620b: cmp dword ptr [eax + edi*4], 0`
  - 0x00576235: je | true=0x00576244 | false=0x00576237
    predicate_hint: `0x00576233: test edx, edx`

### 0x0084b9d0
- blocks=10, insns=67, edges=17, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0084b9f8: je | true=0x0084ba08 | false=0x0084b9fa
    predicate_hint: `0x0084b9f5: cmp eax, 3`
  - 0x0084b9fd: je | true=0x0084ba08 | false=0x0084b9ff
    predicate_hint: `0x0084b9fa: cmp eax, 6`
  - 0x0084ba1b: jne | true=0x0084ba5b | false=0x0084ba1d
    predicate_hint: `0x0084ba17: test byte ptr [esi + 0x4a], 6`
  - 0x0084ba21: jne | true=0x0084ba5b | false=0x0084ba23
    predicate_hint: `0x0084ba1d: test byte ptr [esi + 0x48], 4`
  - 0x0084ba3f: je | true=0x0084ba4b | false=0x0084ba41
    predicate_hint: `0x0084ba3d: cmp ecx, eax`

### 0x006c7bef
- blocks=9, insns=61, edges=15, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006c7c0c: je | true=0x006c7c3c | false=0x006c7c0e
    predicate_hint: `0x006c7c0a: test eax, eax`
  - 0x006c7c1d: jb | true=0x006c7c21 | false=0x006c7c1f
    predicate_hint: `0x006c7c19: cmp dword ptr [eax + 0x14], 0x10`
  - 0x006c7c2e: je | true=0x006c7c48 | false=0x006c7c30
    predicate_hint: `0x006c7c2c: test eax, eax`
  - 0x006c7c3a: jb | true=0x006c7c10 | false=0x006c7c3c
    predicate_hint: `0x006c7c37: cmp esi, dword ptr [ebp - 4]`

### 0x0061d303
- blocks=7, insns=41, edges=17, jcc=6, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0061d30f: je | true=0x0061d341 | false=0x0061d311
    predicate_hint: `0x0061d30d: cmp edx, eax`
  - 0x0061d321: jp | true=0x0061d332 | false=0x0061d323
    predicate_hint: `0x0061d31e: test ah, 0x44`
  - 0x0061d327: jb | true=0x0061d32b | false=0x0061d329
    predicate_hint: `0x0061d323: cmp dword ptr [edx + 0x14], 0x10`
  - 0x0061d33f: jne | true=0x0061d311 | false=0x0061d341
    predicate_hint: `0x0061d33d: cmp edx, dword ptr [esi]`

### 0x00b4b114
- blocks=8, insns=66, edges=20, jcc=5, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - 0x00b4b121: jne | true=0x00b4b12a | false=0x00b4b123
    predicate_hint: `0x00b4b11e: mov dword ptr [ebp - 0x10], esi`
  - 0x00b4b14d: je | true=0x00b4b158 | false=0x00b4b14f
    predicate_hint: `0x00b4b14b: test eax, eax`
  - 0x00b4b16f: jne | true=0x00b4b178 | false=0x00b4b171
    predicate_hint: `0x00b4b168: cmp byte ptr [0xfb036c], 0`

### 0x007e03bc
- blocks=11, insns=318, edges=34, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007e03ea: jne | true=0x007e056b | false=0x007e03f0
    predicate_hint: `0x007e03e4: lea ecx, [ecx + 0x80]`
  - 0x007e040a: je | true=0x007e049d | false=0x007e0410
    predicate_hint: `0x007e0408: test ebx, ebx`
  - 0x007e0582: je | true=0x007e0618 | false=0x007e0588
    predicate_hint: `0x007e0580: test ebx, ebx`
  - 0x007e0672: je | true=0x007e067e | false=0x007e0674
    predicate_hint: `0x007e0670: cmp ecx, eax`

### 0x0088e7cd
- blocks=11, insns=193, edges=26, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088e7f7: jne | true=0x0088e887 | false=0x0088e7fd
    predicate_hint: `0x0088e7f4: lea ecx, [ecx + 0x40]`
  - 0x0088e814: je | true=0x0088e81d | false=0x0088e816
    predicate_hint: `0x0088e812: test ecx, ecx`
  - 0x0088e89e: je | true=0x0088e8a9 | false=0x0088e8a0
    predicate_hint: `0x0088e89c: test ecx, ecx`
  - 0x0088e8f1: je | true=0x0088e8fd | false=0x0088e8f3
    predicate_hint: `0x0088e8ef: cmp ecx, eax`

### 0x0088c470
- blocks=11, insns=184, edges=22, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088c4b7: jne | true=0x0088c52f | false=0x0088c4b9
    predicate_hint: `0x0088c4b4: lea ecx, [ecx + 0x40]`
  - 0x0088c4d0: je | true=0x0088c4d9 | false=0x0088c4d2
    predicate_hint: `0x0088c4ce: test ecx, ecx`
  - 0x0088c546: je | true=0x0088c54f | false=0x0088c548
    predicate_hint: `0x0088c544: test ecx, ecx`
  - 0x0088c59d: je | true=0x0088c5a9 | false=0x0088c59f
    predicate_hint: `0x0088c59b: cmp ecx, eax`

### 0x0088b460
- blocks=11, insns=177, edges=26, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088b49f: jne | true=0x0088b514 | false=0x0088b4a1
    predicate_hint: `0x0088b49c: lea ecx, [ecx + 0x40]`
  - 0x0088b4b8: je | true=0x0088b4c1 | false=0x0088b4ba
    predicate_hint: `0x0088b4b6: test ecx, ecx`
  - 0x0088b52b: je | true=0x0088b534 | false=0x0088b52d
    predicate_hint: `0x0088b529: test ecx, ecx`
  - 0x0088b57c: je | true=0x0088b588 | false=0x0088b57e
    predicate_hint: `0x0088b57a: cmp ecx, eax`

### 0x007dcf10
- blocks=11, insns=177, edges=26, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007dcf4f: jne | true=0x007dcfc4 | false=0x007dcf51
    predicate_hint: `0x007dcf4c: lea ecx, [ecx + 0x40]`
  - 0x007dcf68: je | true=0x007dcf71 | false=0x007dcf6a
    predicate_hint: `0x007dcf66: test ecx, ecx`
  - 0x007dcfdb: je | true=0x007dcfe4 | false=0x007dcfdd
    predicate_hint: `0x007dcfd9: test ecx, ecx`
  - 0x007dd02c: je | true=0x007dd038 | false=0x007dd02e
    predicate_hint: `0x007dd02a: cmp ecx, eax`

### 0x00688ed1
- blocks=9, insns=126, edges=26, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00688ee7: jne | true=0x00688f01 | false=0x00688ee9
    predicate_hint: `0x00688ee5: test esi, esi`
  - 0x00688efb: je | true=0x00688ffa | false=0x00688f01
    predicate_hint: `0x00688ef9: test esi, esi`
  - 0x00688f0f: je | true=0x00688ffa | false=0x00688f15
    predicate_hint: `0x00688f0d: test eax, eax`
  - 0x00688f21: je | true=0x00688ffa | false=0x00688f27
    predicate_hint: `0x00688f1f: test eax, eax`
  - 0x00688f2a: jne | true=0x00688fb8 | false=0x00688f30
    predicate_hint: `0x00688f27: cmp byte ptr [ebp - 0xd], bl`

### 0x00688cd7
- blocks=11, insns=102, edges=25, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00688ceb: jl | true=0x00688da7 | false=0x00688cf1
    predicate_hint: `0x00688ce5: cmp eax, dword ptr [edi + 0x1f4]`
  - 0x00688d00: je | true=0x00688dca | false=0x00688d06
    predicate_hint: `0x00688cfe: test eax, eax`
  - 0x00688d14: je | true=0x00688da7 | false=0x00688d1a
    predicate_hint: `0x00688d12: test eax, eax`
  - 0x00688d26: je | true=0x00688da6 | false=0x00688d28
    predicate_hint: `0x00688d24: test ebx, ebx`
  - 0x00688d31: je | true=0x00688dbb | false=0x00688d37
    predicate_hint: `0x00688d2f: test al, al`

### 0x0063b62a
- blocks=8, insns=93, edges=25, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063b639: jne | true=0x0063b6f4 | false=0x0063b63f
    predicate_hint: `0x0063b637: test eax, eax`
  - 0x0063b6ac: je | true=0x0063b6c7 | false=0x0063b6ae
    predicate_hint: `0x0063b6a5: cmp byte ptr [eax + 0x124], 0`
  - 0x0063b6be: je | true=0x0063b6c7 | false=0x0063b6c0
    predicate_hint: `0x0063b6bc: test eax, eax`
  - 0x0063b6d5: je | true=0x0063b6e5 | false=0x0063b6d7
    predicate_hint: `0x0063b6d1: cmp byte ptr [ebp + 8], 0`

### 0x0085e137
- blocks=8, insns=92, edges=15, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0085e154: je | true=0x0085e186 | false=0x0085e156
    predicate_hint: `0x0085e152: test edx, edx`
  - 0x0085e166: jne | true=0x0085e180 | false=0x0085e168
    predicate_hint: `0x0085e15f: test byte ptr [edx + 0x4a], 0xe`
  - 0x0085e172: je | true=0x0085e186 | false=0x0085e174
    predicate_hint: `0x0085e170: cmp ecx, edi`
  - 0x0085e1a1: jne | true=0x0085e1a9 | false=0x0085e1a3
    predicate_hint: `0x0085e19f: cmp dword ptr [edx], eax`

### 0x0056815d
- blocks=8, insns=87, edges=20, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00568180: je | true=0x00568239 | false=0x00568186
    predicate_hint: `0x0056817e: test edi, edi`
  - 0x0056818a: je | true=0x00568239 | false=0x00568190
    predicate_hint: `0x00568186: test byte ptr [edi + 0x50], 8`
  - 0x00568210: je | true=0x0056821a | false=0x00568212
    predicate_hint: `0x0056820e: test ecx, ecx`
  - 0x00568233: je | true=0x00568239 | false=0x00568235
    predicate_hint: `0x00568231: test al, al`

### 0x00882ccc
- blocks=8, insns=75, edges=18, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00882cf7: jb | true=0x00882cfd | false=0x00882cf9
    predicate_hint: `0x00882cf3: cmp dword ptr [esi + 0x14], 0x10`
  - 0x00882d36: je | true=0x00882d44 | false=0x00882d38
    predicate_hint: `0x00882d34: cmp esi, eax`
  - 0x00882d4c: jb | true=0x00882d59 | false=0x00882d4e
    predicate_hint: `0x00882d44: cmp dword ptr [ebp - 0x14], 0x10`

### 0x0060d112
- blocks=7, insns=65, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060d121: ja | true=0x0060d12a | false=0x0060d123
    predicate_hint: `0x0060d11e: cmp dword ptr [ebx + 8], eax`
  - 0x0060d144: jne | true=0x0060d15a | false=0x0060d146
    predicate_hint: `0x0060d140: cmp dword ptr [eax + esi*4], 0`
  - 0x0060d162: je | true=0x0060d16c | false=0x0060d164
    predicate_hint: `0x0060d160: test edi, edi`

### 0x0056b0c1
- blocks=7, insns=60, edges=17, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056b0e5: je | true=0x0056b101 | false=0x0056b0e7
    predicate_hint: `0x0056b0e2: test byte ptr [edi], 1`
  - 0x0056b0f1: je | true=0x0056b101 | false=0x0056b0f3
    predicate_hint: `0x0056b0ef: test al, al`
  - 0x0056b113: je | true=0x0056b12c | false=0x0056b115
    predicate_hint: `0x0056b110: test byte ptr [edi], 1`
  - 0x0056b11f: je | true=0x0056b12c | false=0x0056b121
    predicate_hint: `0x0056b11d: test al, al`

### 0x006baed6
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006baeec: jne | true=0x006baef4 | false=0x006baeee
    predicate_hint: `0x006baeea: test ecx, ecx`
  - 0x006baef9: je | true=0x006baefd | false=0x006baefb
    predicate_hint: `0x006baef7: test eax, eax`
  - 0x006baf02: je | true=0x006baf06 | false=0x006baf04
    predicate_hint: `0x006baf00: test ecx, ecx`

### 0x006a76ec
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006a7702: jne | true=0x006a770a | false=0x006a7704
    predicate_hint: `0x006a7700: test ecx, ecx`
  - 0x006a770f: je | true=0x006a7713 | false=0x006a7711
    predicate_hint: `0x006a770d: test eax, eax`
  - 0x006a7718: je | true=0x006a771c | false=0x006a771a
    predicate_hint: `0x006a7716: test ecx, ecx`

### 0x006a7435
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006a744b: jne | true=0x006a7453 | false=0x006a744d
    predicate_hint: `0x006a7449: test ecx, ecx`
  - 0x006a7458: je | true=0x006a745c | false=0x006a745a
    predicate_hint: `0x006a7456: test eax, eax`
  - 0x006a7461: je | true=0x006a7465 | false=0x006a7463
    predicate_hint: `0x006a745f: test ecx, ecx`

### 0x00678bd6
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00678bec: jne | true=0x00678bf4 | false=0x00678bee
    predicate_hint: `0x00678bea: test ecx, ecx`
  - 0x00678bf9: je | true=0x00678bfd | false=0x00678bfb
    predicate_hint: `0x00678bf7: test eax, eax`
  - 0x00678c02: je | true=0x00678c06 | false=0x00678c04
    predicate_hint: `0x00678c00: test ecx, ecx`

### 0x00677fd2
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00677fe8: jne | true=0x00677ff0 | false=0x00677fea
    predicate_hint: `0x00677fe6: test ecx, ecx`
  - 0x00677ff5: je | true=0x00677ff9 | false=0x00677ff7
    predicate_hint: `0x00677ff3: test eax, eax`
  - 0x00677ffe: je | true=0x00678002 | false=0x00678000
    predicate_hint: `0x00677ffc: test ecx, ecx`

### 0x005fd2e1
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005fd2f7: jne | true=0x005fd2ff | false=0x005fd2f9
    predicate_hint: `0x005fd2f5: test ecx, ecx`
  - 0x005fd304: je | true=0x005fd308 | false=0x005fd306
    predicate_hint: `0x005fd302: test eax, eax`
  - 0x005fd30d: je | true=0x005fd311 | false=0x005fd30f
    predicate_hint: `0x005fd30b: test ecx, ecx`

### 0x00588b31
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00588b47: jne | true=0x00588b4f | false=0x00588b49
    predicate_hint: `0x00588b45: test ecx, ecx`
  - 0x00588b54: je | true=0x00588b58 | false=0x00588b56
    predicate_hint: `0x00588b52: test eax, eax`
  - 0x00588b5d: je | true=0x00588b61 | false=0x00588b5f
    predicate_hint: `0x00588b5b: test ecx, ecx`

### 0x00580fd5
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00580feb: jne | true=0x00580ff3 | false=0x00580fed
    predicate_hint: `0x00580fe9: test ecx, ecx`
  - 0x00580ff8: je | true=0x00580ffc | false=0x00580ffa
    predicate_hint: `0x00580ff6: test eax, eax`
  - 0x00581001: je | true=0x00581005 | false=0x00581003
    predicate_hint: `0x00580fff: test ecx, ecx`

### 0x0057fd44
- blocks=8, insns=30, edges=12, jcc=5, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057fd5a: jne | true=0x0057fd62 | false=0x0057fd5c
    predicate_hint: `0x0057fd58: test ecx, ecx`
  - 0x0057fd67: je | true=0x0057fd6b | false=0x0057fd69
    predicate_hint: `0x0057fd65: test eax, eax`
  - 0x0057fd70: je | true=0x0057fd74 | false=0x0057fd72
    predicate_hint: `0x0057fd6e: test ecx, ecx`

### 0x0054fa98
- blocks=8, insns=171, edges=29, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054faaf: jne | true=0x0054fab8 | false=0x0054fab1
    predicate_hint: `0x0054faad: test edx, edx`
  - 0x0054fac8: je | true=0x0054fab1 | false=0x0054faca
    predicate_hint: `0x0054fac6: test eax, eax`
  - 0x0054fad1: je | true=0x0054fab1 | false=0x0054fad3
    predicate_hint: `0x0054facf: test edx, edx`
  - 0x0054fbc2: je | true=0x0054fc58 | false=0x0054fbc8
    predicate_hint: `0x0054fbc0: test eax, eax`

### 0x005c4af0
- blocks=12, insns=164, edges=43, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c4b29: jae | true=0x005c4b33 | false=0x005c4b2b
    predicate_hint: `0x005c4b26: cmp eax, dword ptr [ebp - 0x18]`
  - 0x005c4b4f: ja | true=0x005c4b53 | false=0x005c4b51
    predicate_hint: `0x005c4b4d: cmp edx, esi`
  - 0x005c4b75: ja | true=0x005c4b92 | false=0x005c4b77
    predicate_hint: `0x005c4b73: cmp dword ptr [eax], edi`
  - 0x005c4c38: jbe | true=0x005c4c5c | false=0x005c4c3a
    predicate_hint: `0x005c4c34: cmp dword ptr [ebp + 0xc], 0`

### 0x00854ca0
- blocks=8, insns=138, edges=20, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00854cc1: je | true=0x00854d89 | false=0x00854cc7
    predicate_hint: `0x00854cbb: cmp dword ptr [ebp + 0x28], -1`
  - 0x00854cec: je | true=0x00854cf9 | false=0x00854cee
    predicate_hint: `0x00854cea: test eax, eax`
  - 0x00854d64: je | true=0x00854d70 | false=0x00854d66
    predicate_hint: `0x00854d62: cmp ecx, eax`

### 0x0088ccf0
- blocks=8, insns=134, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088cd3a: je | true=0x0088cdb4 | false=0x0088cd3c
    predicate_hint: `0x0088cd38: test ecx, ecx`
  - 0x0088cda4: jb | true=0x0088cda8 | false=0x0088cda6
    predicate_hint: `0x0088cda0: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088ce16: je | true=0x0088ce22 | false=0x0088ce18
    predicate_hint: `0x0088ce14: cmp ecx, eax`

### 0x0088c830
- blocks=8, insns=134, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088c87a: je | true=0x0088c8f4 | false=0x0088c87c
    predicate_hint: `0x0088c878: test ecx, ecx`
  - 0x0088c8e4: jb | true=0x0088c8e8 | false=0x0088c8e6
    predicate_hint: `0x0088c8e0: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088c956: je | true=0x0088c962 | false=0x0088c958
    predicate_hint: `0x0088c954: cmp ecx, eax`

### 0x0088b74d
- blocks=8, insns=133, edges=15, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088b77b: je | true=0x0088b812 | false=0x0088b781
    predicate_hint: `0x0088b779: test esi, esi`
  - 0x0088b7f4: jb | true=0x0088b7f8 | false=0x0088b7f6
    predicate_hint: `0x0088b7f0: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088b86c: je | true=0x0088b878 | false=0x0088b86e
    predicate_hint: `0x0088b86a: cmp ecx, ebx`

### 0x00854db0
- blocks=8, insns=132, edges=16, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00854dd1: je | true=0x00854e88 | false=0x00854dd7
    predicate_hint: `0x00854dcb: cmp dword ptr [ebp + 0x24], -1`
  - 0x00854dfc: je | true=0x00854e09 | false=0x00854dfe
    predicate_hint: `0x00854dfa: test eax, eax`
  - 0x00854e63: je | true=0x00854e6f | false=0x00854e65
    predicate_hint: `0x00854e61: cmp ecx, eax`

### 0x008987ad
- blocks=8, insns=125, edges=17, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008987de: je | true=0x00898846 | false=0x008987e0
    predicate_hint: `0x008987dc: test ebx, ebx`
  - 0x00898836: jb | true=0x0089883a | false=0x00898838
    predicate_hint: `0x00898832: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0089889a: je | true=0x008988a6 | false=0x0089889c
    predicate_hint: `0x00898898: cmp ecx, eax`

### 0x0088bf0d
- blocks=8, insns=121, edges=15, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088bf3b: je | true=0x0088bfc4 | false=0x0088bf41
    predicate_hint: `0x0088bf39: test esi, esi`
  - 0x0088bfb4: jb | true=0x0088bfb8 | false=0x0088bfb6
    predicate_hint: `0x0088bfb0: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088c01e: je | true=0x0088c02a | false=0x0088c020
    predicate_hint: `0x0088c01c: cmp ecx, ebx`

### 0x00843800
- blocks=8, insns=119, edges=15, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0084384b: je | true=0x008438ba | false=0x0084384d
    predicate_hint: `0x00843849: test edi, edi`
  - 0x008438aa: jb | true=0x008438ae | false=0x008438ac
    predicate_hint: `0x008438a6: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00843906: je | true=0x00843912 | false=0x00843908
    predicate_hint: `0x00843904: cmp ecx, eax`

### 0x0088babd
- blocks=8, insns=111, edges=15, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088baeb: je | true=0x0088bb62 | false=0x0088baed
    predicate_hint: `0x0088bae9: test esi, esi`
  - 0x0088bb52: jb | true=0x0088bb56 | false=0x0088bb54
    predicate_hint: `0x0088bb4e: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088bbb0: je | true=0x0088bbbc | false=0x0088bbb2
    predicate_hint: `0x0088bbae: cmp ecx, ebx`

### 0x0089746f
- blocks=7, insns=110, edges=16, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0089748b: je | true=0x00897567 | false=0x00897491
    predicate_hint: `0x00897485: cmp eax, dword ptr [edi + 0x110]`
  - 0x008974ff: je | true=0x0089750b | false=0x00897501
    predicate_hint: `0x008974fd: cmp ecx, eax`
  - 0x00897539: jb | true=0x00897546 | false=0x0089753b
    predicate_hint: `0x0089752e: cmp dword ptr [ebp - 0x20], 0x10`

### 0x0088c71b
- blocks=8, insns=106, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088c742: je | true=0x0088c7b5 | false=0x0088c744
    predicate_hint: `0x0088c740: test esi, esi`
  - 0x0088c797: jb | true=0x0088c79b | false=0x0088c799
    predicate_hint: `0x0088c793: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088c7f1: je | true=0x0088c7fd | false=0x0088c7f3
    predicate_hint: `0x0088c7ef: cmp ecx, ebx`

### 0x0088ed70
- blocks=8, insns=104, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088edb2: je | true=0x0088ee17 | false=0x0088edb4
    predicate_hint: `0x0088edb0: test edi, edi`
  - 0x0088ee07: jb | true=0x0088ee0b | false=0x0088ee09
    predicate_hint: `0x0088ee03: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088ee53: je | true=0x0088ee5f | false=0x0088ee55
    predicate_hint: `0x0088ee51: cmp ecx, eax`

### 0x0088c980
- blocks=8, insns=104, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088c9c2: je | true=0x0088ca27 | false=0x0088c9c4
    predicate_hint: `0x0088c9c0: test edi, edi`
  - 0x0088ca17: jb | true=0x0088ca1b | false=0x0088ca19
    predicate_hint: `0x0088ca13: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088ca63: je | true=0x0088ca6f | false=0x0088ca65
    predicate_hint: `0x0088ca61: cmp ecx, eax`

### 0x0088c360
- blocks=8, insns=104, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088c3a2: je | true=0x0088c407 | false=0x0088c3a4
    predicate_hint: `0x0088c3a0: test edi, edi`
  - 0x0088c3f7: jb | true=0x0088c3fb | false=0x0088c3f9
    predicate_hint: `0x0088c3f3: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088c443: je | true=0x0088c44f | false=0x0088c445
    predicate_hint: `0x0088c441: cmp ecx, eax`

### 0x0088e94d
- blocks=8, insns=103, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088e977: je | true=0x0088e9dd | false=0x0088e979
    predicate_hint: `0x0088e975: test ebx, ebx`
  - 0x0088e9cc: jb | true=0x0088e9d0 | false=0x0088e9ce
    predicate_hint: `0x0088e9c8: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088ea25: je | true=0x0088ea31 | false=0x0088ea27
    predicate_hint: `0x0088ea23: cmp ecx, eax`

### 0x00842bb0
- blocks=8, insns=102, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00842bf2: je | true=0x00842c4e | false=0x00842bf4
    predicate_hint: `0x00842bf0: test edi, edi`
  - 0x00842c3e: jb | true=0x00842c42 | false=0x00842c40
    predicate_hint: `0x00842c3a: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00842c88: je | true=0x00842c94 | false=0x00842c8a
    predicate_hint: `0x00842c86: cmp ecx, eax`

### 0x00842ab0
- blocks=8, insns=102, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00842af2: je | true=0x00842b4e | false=0x00842af4
    predicate_hint: `0x00842af0: test edi, edi`
  - 0x00842b3e: jb | true=0x00842b42 | false=0x00842b40
    predicate_hint: `0x00842b3a: cmp dword ptr [eax + 0x14], 0x10`
  - 0x00842b88: je | true=0x00842b94 | false=0x00842b8a
    predicate_hint: `0x00842b86: cmp ecx, eax`

### 0x008425db
- blocks=8, insns=101, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00842602: je | true=0x00842664 | false=0x00842604
    predicate_hint: `0x00842600: test esi, esi`
  - 0x00842654: jb | true=0x00842658 | false=0x00842656
    predicate_hint: `0x00842650: cmp dword ptr [eax + 0x14], 0x10`
  - 0x008426aa: je | true=0x008426b6 | false=0x008426ac
    predicate_hint: `0x008426a8: cmp ecx, eax`

### 0x0088ef5b
- blocks=8, insns=94, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088ef82: je | true=0x0088efe7 | false=0x0088ef84
    predicate_hint: `0x0088ef80: test esi, esi`
  - 0x0088efd7: jb | true=0x0088efdb | false=0x0088efd9
    predicate_hint: `0x0088efd3: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088f023: je | true=0x0088f02f | false=0x0088f025
    predicate_hint: `0x0088f021: cmp ecx, ebx`

### 0x0088e28b
- blocks=8, insns=94, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0088e2b2: je | true=0x0088e317 | false=0x0088e2b4
    predicate_hint: `0x0088e2b0: test esi, esi`
  - 0x0088e307: jb | true=0x0088e30b | false=0x0088e309
    predicate_hint: `0x0088e303: cmp dword ptr [eax + 0x14], 0x10`
  - 0x0088e353: je | true=0x0088e35f | false=0x0088e355
    predicate_hint: `0x0088e351: cmp ecx, ebx`

### 0x005781c1
- blocks=7, insns=83, edges=18, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005781e4: je | true=0x005781fc | false=0x005781e6
    predicate_hint: `0x005781e2: test eax, eax`
  - 0x0057820c: je | true=0x0057824f | false=0x0057820e
    predicate_hint: `0x0057820a: test al, al`
  - 0x0057824a: jne | true=0x0057820e | false=0x0057824c
    predicate_hint: `0x00578248: test al, al`

### 0x0069c3d0
- blocks=8, insns=82, edges=20, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069c3de: jne | true=0x0069c3f3 | false=0x0069c3e0
    predicate_hint: `0x0069c3dc: test ebx, ebx`
  - 0x0069c404: je | true=0x0069c476 | false=0x0069c406
    predicate_hint: `0x0069c402: test edi, edi`
  - 0x0069c412: je | true=0x0069c476 | false=0x0069c414
    predicate_hint: `0x0069c410: test al, al`
  - 0x0069c420: jne | true=0x0069c476 | false=0x0069c422
    predicate_hint: `0x0069c41e: test eax, eax`

### 0x0068a624
- blocks=5, insns=76, edges=17, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0068a648: je | true=0x0068a65c | false=0x0068a64a
    predicate_hint: `0x0068a646: test eax, eax`
  - 0x0068a690: jle | true=0x0068a674 | false=0x0068a692
    predicate_hint: `0x0068a68d: cmp ebx, 0x11`

### 0x00567009
- blocks=7, insns=70, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00567013: je | true=0x00567054 | false=0x00567015
    predicate_hint: `0x00567011: test esi, esi`
  - 0x0056701e: je | true=0x00567035 | false=0x00567020
    predicate_hint: `0x0056701c: cmp esi, ebx`
  - 0x0056702d: jne | true=0x00567022 | false=0x0056702f
    predicate_hint: `0x0056702b: cmp esi, ebx`

### 0x00579280
- blocks=7, insns=68, edges=17, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005792b6: je | true=0x005792fa | false=0x005792b8
    predicate_hint: `0x005792b4: test eax, eax`
  - 0x005792ba: je | true=0x005792fa | false=0x005792bc
    predicate_hint: `0x005792b8: test ebx, ebx`
  - 0x005792d0: je | true=0x005792fa | false=0x005792d2
    predicate_hint: `0x005792ce: test ecx, ecx`
  - 0x005792d4: je | true=0x005792fa | false=0x005792d6
    predicate_hint: `0x005792d2: test eax, eax`

### 0x0056af26
- blocks=8, insns=60, edges=13, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056af37: jne | true=0x0056af53 | false=0x0056af39
    predicate_hint: `0x0056af34: cmp dword ptr [esi + 8], ebx`
  - 0x0056af66: jne | true=0x0056af84 | false=0x0056af68
    predicate_hint: `0x0056af63: cmp dword ptr [esi + 0xc], ebx`
  - 0x0056af72: je | true=0x0056af7f | false=0x0056af74
    predicate_hint: `0x0056af70: test eax, eax`

### 0x00846363
- blocks=7, insns=58, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0084636b: jne | true=0x008463cb | false=0x0084636d
    predicate_hint: `0x00846369: test al, 1`
  - 0x00846389: je | true=0x00846395 | false=0x0084638b
    predicate_hint: `0x00846387: cmp ecx, edi`
  - 0x008463a8: je | true=0x008463b3 | false=0x008463aa
    predicate_hint: `0x008463a6: test eax, eax`

### 0x005cc700
- blocks=6, insns=56, edges=16, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005cc71c: ja | true=0x005cc726 | false=0x005cc71e
    predicate_hint: `0x005cc719: cmp ecx, dword ptr [ebp + 8]`
  - 0x005cc73a: jbe | true=0x005cc779 | false=0x005cc73c
    predicate_hint: `0x005cc736: cmp dword ptr [ebp + 8], 0`
  - 0x005cc74f: je | true=0x005cc779 | false=0x005cc751
    predicate_hint: `0x005cc74d: test ecx, ecx`

### 0x008e46d0
- blocks=8, insns=52, edges=13, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x008e46ee: jae | true=0x008e46f5 | false=0x008e46f0
    predicate_hint: `0x008e46eb: cmp esi, dword ptr [eax + 0xc]`
  - 0x008e46f7: jne | true=0x008e4736 | false=0x008e46f9
    predicate_hint: `0x008e46f5: test ecx, ecx`
  - 0x008e4718: je | true=0x008e4722 | false=0x008e471a
    predicate_hint: `0x008e4711: test eax, eax`

### 0x00644c42
- blocks=7, insns=50, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00644c49: jne | true=0x00644c90 | false=0x00644c4b
    predicate_hint: `0x00644c47: cmp esi, dword ptr [eax]`
  - 0x00644c4e: jne | true=0x00644c90 | false=0x00644c50
    predicate_hint: `0x00644c4b: cmp dword ptr [ebp + 0x10], eax`
  - 0x00644c93: jne | true=0x00644c79 | false=0x00644c95
    predicate_hint: `0x00644c90: cmp esi, dword ptr [ebp + 0x10]`

### 0x0057fd87
- blocks=7, insns=50, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057fd8e: jne | true=0x0057fdd5 | false=0x0057fd90
    predicate_hint: `0x0057fd8c: cmp esi, dword ptr [eax]`
  - 0x0057fd93: jne | true=0x0057fdd5 | false=0x0057fd95
    predicate_hint: `0x0057fd90: cmp dword ptr [ebp + 0x10], eax`
  - 0x0057fdd8: jne | true=0x0057fdbe | false=0x0057fdda
    predicate_hint: `0x0057fdd5: cmp esi, dword ptr [ebp + 0x10]`

### 0x0060faf6
- blocks=7, insns=49, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060fb03: jne | true=0x0060fb28 | false=0x0060fb05
    predicate_hint: `0x0060fafe: cmp eax, dword ptr [edx]`
  - 0x0060fb07: jne | true=0x0060fb28 | false=0x0060fb09
    predicate_hint: `0x0060fb05: cmp edx, dword ptr [esi]`
  - 0x0060fb2a: je | true=0x0060fb45 | false=0x0060fb2c
    predicate_hint: `0x0060fb28: cmp eax, edx`
  - 0x0060fb43: jne | true=0x0060fb2c | false=0x0060fb45
    predicate_hint: `0x0060fb40: cmp eax, dword ptr [ebp + 0x10]`

### 0x005fdcf8
- blocks=7, insns=49, edges=12, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005fdd05: jne | true=0x005fdd2a | false=0x005fdd07
    predicate_hint: `0x005fdd00: cmp eax, dword ptr [edx]`
  - 0x005fdd09: jne | true=0x005fdd2a | false=0x005fdd0b
    predicate_hint: `0x005fdd07: cmp edx, dword ptr [esi]`
  - 0x005fdd2c: je | true=0x005fdd47 | false=0x005fdd2e
    predicate_hint: `0x005fdd2a: cmp eax, edx`
  - 0x005fdd45: jne | true=0x005fdd2e | false=0x005fdd47
    predicate_hint: `0x005fdd42: cmp eax, dword ptr [ebp + 0x10]`

### 0x005333fb
- blocks=6, insns=43, edges=13, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00533404: je | true=0x0053343c | false=0x00533406
    predicate_hint: `0x00533402: test esi, esi`
  - 0x00533416: jne | true=0x00533422 | false=0x00533418
    predicate_hint: `0x00533414: test eax, eax`
  - 0x0053342c: je | true=0x0053343c | false=0x0053342e
    predicate_hint: `0x0053342a: test eax, eax`

### 0x0057b4ed
- blocks=6, insns=35, edges=10, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057b50c: je | true=0x0057b513 | false=0x0057b50e
    predicate_hint: `0x0057b50a: cmp eax, dword ptr [esi]`
  - 0x0057b511: jge | true=0x0057b515 | false=0x0057b513
    predicate_hint: `0x0057b50e: cmp edi, dword ptr [eax + 0x10]`
  - 0x0057b517: je | true=0x0057b522 | false=0x0057b519
    predicate_hint: `0x0057b515: cmp eax, dword ptr [esi]`

### 0x00576996
- blocks=6, insns=24, edges=9, jcc=4, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005769a7: je | true=0x005769b1 | false=0x005769a9
    predicate_hint: `0x005769a5: cmp eax, dword ptr [esi]`
  - 0x005769af: jge | true=0x005769b3 | false=0x005769b1
    predicate_hint: `0x005769ac: cmp ecx, dword ptr [eax + 0x10]`
  - 0x005769b6: je | true=0x005769bc | false=0x005769b8
    predicate_hint: `0x005769b3: cmp eax, dword ptr [esi]`

### 0x0063b448
- blocks=6, insns=52, edges=10, jcc=3, switch_indirect=0, truncated=False
- classes:
  - .?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@
- branch conditions:
  - 0x0063b49e: jne | true=0x0063b4a4 | false=0x0063b4a0
    predicate_hint: `0x0063b49c: test bl, bl`
  - 0x0063b4a2: je | true=0x0063b4ad | false=0x0063b4a4
    predicate_hint: `0x0063b4a0: test bh, bh`
  - 0x0063b4a6: je | true=0x0063b4ad | false=0x0063b4a8
    predicate_hint: `0x0063b4a4: test al, al`

### 0x006c698f
- blocks=6, insns=127, edges=28, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006c69d2: jb | true=0x006c69d8 | false=0x006c69d4
    predicate_hint: `0x006c69ce: cmp dword ptr [edi + 0x14], 0x10`
  - 0x006c6a25: jb | true=0x006c6a29 | false=0x006c6a27
    predicate_hint: `0x006c6a21: cmp dword ptr [edi + 0x14], 0x10`

### 0x008989b0
- blocks=5, insns=113, edges=17, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00898a40: je | true=0x00898a4c | false=0x00898a42
    predicate_hint: `0x00898a3e: cmp ecx, eax`
  - 0x00898a96: jb | true=0x00898aa3 | false=0x00898a98
    predicate_hint: `0x00898a8e: cmp dword ptr [ebp - 0x24], 0x10`

### 0x0087f0a9
- blocks=6, insns=99, edges=14, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0087f0f1: jb | true=0x0087f0f8 | false=0x0087f0f3
    predicate_hint: `0x0087f0ed: cmp dword ptr [esi + 0x24], 0x10`
  - 0x0087f122: jb | true=0x0087f126 | false=0x0087f124
    predicate_hint: `0x0087f11e: cmp dword ptr [eax + 0x14], 0x10`

### 0x005d8a20
- blocks=7, insns=92, edges=28, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005d8a2f: jne | true=0x005d8a36 | false=0x005d8a31
    predicate_hint: `0x005d8a2d: test eax, eax`
  - 0x005d8a41: jb | true=0x005d8aba | false=0x005d8a43
    predicate_hint: `0x005d8a3e: cmp dword ptr [eax], 0x10`
  - 0x005d8a75: jbe | true=0x005d8a99 | false=0x005d8a77
    predicate_hint: `0x005d8a71: cmp dword ptr [ebp + 0xc], 0`

### 0x005c5130
- blocks=7, insns=92, edges=28, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c513f: jne | true=0x005c5146 | false=0x005c5141
    predicate_hint: `0x005c513d: test eax, eax`
  - 0x005c5151: jb | true=0x005c51ca | false=0x005c5153
    predicate_hint: `0x005c514e: cmp dword ptr [eax], 0x10`
  - 0x005c5185: jbe | true=0x005c51a9 | false=0x005c5187
    predicate_hint: `0x005c5181: cmp dword ptr [ebp + 0xc], 0`

### 0x0062484b
- blocks=8, insns=91, edges=11, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006248a8: je | true=0x006248de | false=0x006248aa
    predicate_hint: `0x006248a6: test cl, cl`
  - 0x006248ae: je | true=0x006248b4 | false=0x006248b0
    predicate_hint: `0x006248ac: test al, al`
  - 0x006248e0: jne | true=0x006248e8 | false=0x006248e2
    predicate_hint: `0x006248de: test al, al`

### 0x0054c358
- blocks=4, insns=72, edges=15, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054c39e: je | true=0x0054c417 | false=0x0054c3a0
    predicate_hint: `0x0054c39b: cmp ecx, dword ptr [eax + 8]`
  - 0x0054c3b9: jb | true=0x0054c417 | false=0x0054c3bb
    predicate_hint: `0x0054c3b5: comiss xmm0, dword ptr [ebp - 8]`
  - 0x0054c415: jne | true=0x0054c3a0 | false=0x0054c417
    predicate_hint: `0x0054c412: cmp esi, dword ptr [eax + 8]`

### 0x00605cc4
- blocks=7, insns=65, edges=19, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00605cf3: je | true=0x00605d10 | false=0x00605cf5
    predicate_hint: `0x00605cf0: cmp eax, 5`
  - 0x00605d2e: je | true=0x00605d41 | false=0x00605d30
    predicate_hint: `0x00605d2b: cmp eax, 6`
  - 0x00605d52: je | true=0x00605d5c | false=0x00605d54
    predicate_hint: `0x00605d50: test eax, eax`

### 0x005a2fb0
- blocks=7, insns=65, edges=19, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005a2fd3: je | true=0x005a300c | false=0x005a2fd5
    predicate_hint: `0x005a2fd1: test ecx, ecx`
  - 0x005a2fef: je | true=0x005a300c | false=0x005a2ff1
    predicate_hint: `0x005a2fed: test eax, eax`
  - 0x005a301d: je | true=0x005a303e | false=0x005a301f
    predicate_hint: `0x005a301b: test eax, eax`

### 0x0089530b
- blocks=6, insns=60, edges=13, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00895353: jb | true=0x00895359 | false=0x00895355
    predicate_hint: `0x0089534f: cmp dword ptr [esi + 0x14], 0x10`
  - 0x00895378: jb | true=0x00895385 | false=0x0089537a
    predicate_hint: `0x0089536d: cmp dword ptr [ebp - 0x18], 0x10`

### 0x0063be80
- blocks=5, insns=59, edges=14, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063be91: je | true=0x0063bed3 | false=0x0063be93
    predicate_hint: `0x0063be8f: test ebx, ebx`
  - 0x0063beba: je | true=0x0063bed3 | false=0x0063bebc
    predicate_hint: `0x0063beb3: cmp byte ptr [eax + 0x124], 0`
  - 0x0063beca: je | true=0x0063bed3 | false=0x0063becc
    predicate_hint: `0x0063bec8: test eax, eax`

### 0x006972af
- blocks=5, insns=55, edges=15, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006972be: jne | true=0x006972c7 | false=0x006972c0
    predicate_hint: `0x006972bc: test dl, dl`
  - 0x006972e5: jne | true=0x00697303 | false=0x006972e7
    predicate_hint: `0x006972e3: test eax, eax`

### 0x0069b176
- blocks=8, insns=53, edges=13, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069b180: je | true=0x0069b186 | false=0x0069b182
    predicate_hint: `0x0069b17e: test al, al`
  - 0x0069b1b2: jne | true=0x0069b1c2 | false=0x0069b1b4
    predicate_hint: `0x0069b1ae: cmp dword ptr [ebp - 0x10], 0`
  - 0x0069b1bb: jle | true=0x0069b1d5 | false=0x0069b1bd
    predicate_hint: `0x0069b1b7: cmp dword ptr [esi + 0x40], 0`

### 0x00613d09
- blocks=6, insns=53, edges=12, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00613d1a: je | true=0x00613d62 | false=0x00613d1c
    predicate_hint: `0x00613d18: test ecx, ecx`
  - 0x00613d2e: je | true=0x00613d61 | false=0x00613d30
    predicate_hint: `0x00613d2c: test al, al`
  - 0x00613d56: jbe | true=0x00613d61 | false=0x00613d58
    predicate_hint: `0x00613d52: comiss xmm0, dword ptr [ebp - 4]`

### 0x005b7f90
- blocks=7, insns=45, edges=15, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005b7fa3: je | true=0x005b7ffe | false=0x005b7fa5
    predicate_hint: `0x005b7fa1: test eax, eax`
  - 0x005b7fe4: je | true=0x005b7ff5 | false=0x005b7fe6
    predicate_hint: `0x005b7fe0: cmp dword ptr [ebp - 0xc], 0`

### 0x0069aca4
- blocks=5, insns=41, edges=10, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069acc6: je | true=0x0069acce | false=0x0069acc8
    predicate_hint: `0x0069acc4: test eax, eax`
  - 0x0069acd9: je | true=0x0069ace1 | false=0x0069acdb
    predicate_hint: `0x0069acd7: test eax, eax`

### 0x0060f9df
- blocks=7, insns=37, edges=12, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060f9f2: jbe | true=0x0060fa1b | false=0x0060f9f4
    predicate_hint: `0x0060f9ef: comiss xmm0, dword ptr [esi]`
  - 0x0060f9fc: jae | true=0x0060fa03 | false=0x0060f9fe
    predicate_hint: `0x0060f9f7: cmp eax, 0x200`
  - 0x0060fa08: jae | true=0x0060fa0c | false=0x0060fa0a
    predicate_hint: `0x0060fa03: cmp eax, 0x1fffffff`

### 0x005fdc00
- blocks=7, insns=37, edges=12, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005fdc13: jbe | true=0x005fdc3c | false=0x005fdc15
    predicate_hint: `0x005fdc10: comiss xmm0, dword ptr [esi]`
  - 0x005fdc1d: jae | true=0x005fdc24 | false=0x005fdc1f
    predicate_hint: `0x005fdc18: cmp eax, 0x200`
  - 0x005fdc29: jae | true=0x005fdc2d | false=0x005fdc2b
    predicate_hint: `0x005fdc24: cmp eax, 0x1fffffff`

### 0x00565c1b
- blocks=7, insns=37, edges=12, jcc=3, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00565c2e: jbe | true=0x00565c57 | false=0x00565c30
    predicate_hint: `0x00565c2b: comiss xmm0, dword ptr [esi]`
  - 0x00565c38: jae | true=0x00565c3f | false=0x00565c3a
    predicate_hint: `0x00565c33: cmp eax, 0x200`
  - 0x00565c44: jae | true=0x00565c48 | false=0x00565c46
    predicate_hint: `0x00565c3f: cmp eax, 0x1fffffff`

### 0x0063201a
- blocks=4, insns=235, edges=14, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - IsPathingUsed
  - NextWayPoint
  - NextWaypointOrientation
- branch conditions:
  - 0x0063203a: jg | true=0x00632045 | false=0x0063203c
    predicate_hint: `0x00632034: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00632057: jne | true=0x0063203c | false=0x00632059
    predicate_hint: `0x0063204f: cmp dword ptr [0xf5cc30], -1`

### 0x006781a8
- blocks=4, insns=141, edges=7, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - MaximumDistanceWorkerToFarm
  - MaximumDistanceWorkerToResidence
  - ReAttachWorkerFrequency
- branch conditions:
  - 0x006781c8: jg | true=0x006781d3 | false=0x006781ca
    predicate_hint: `0x006781c2: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006781e5: jne | true=0x006781ca | false=0x006781e7
    predicate_hint: `0x006781dd: cmp dword ptr [0xf6eaf8], -1`

### 0x0062767a
- blocks=4, insns=417, edges=20, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - BlockingArea
  - NumBlockedPoints
- branch conditions:
  - 0x0062769a: jg | true=0x006276a5 | false=0x0062769c
    predicate_hint: `0x00627694: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006276b7: jne | true=0x0062769c | false=0x006276b9
    predicate_hint: `0x006276af: cmp dword ptr [0xf583c4], -1`

### 0x00631e3d
- blocks=4, insns=102, edges=12, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - CoarsePath
  - FinePath
- branch conditions:
  - 0x00631e5d: jg | true=0x00631e68 | false=0x00631e5f
    predicate_hint: `0x00631e57: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00631e7a: jne | true=0x00631e5f | false=0x00631e7c
    predicate_hint: `0x00631e72: cmp dword ptr [0xf5cc34], -1`

### 0x0067bb8a
- blocks=4, insns=424, edges=24, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - 0x0067bbaa: jg | true=0x0067bbb5 | false=0x0067bbac
    predicate_hint: `0x0067bba4: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0067bbc7: jne | true=0x0067bbac | false=0x0067bbc9
    predicate_hint: `0x0067bbbf: cmp dword ptr [0xf705a4], -1`

### 0x00638c75
- blocks=4, insns=292, edges=15, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - 0x00638c95: jg | true=0x00638ca0 | false=0x00638c97
    predicate_hint: `0x00638c8f: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00638cb2: jne | true=0x00638c97 | false=0x00638cb4
    predicate_hint: `0x00638caa: cmp dword ptr [0xf5e454], -1`

### 0x0063231d
- blocks=4, insns=138, edges=8, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - WaypointsCount
- branch conditions:
  - 0x0063233d: jg | true=0x00632348 | false=0x0063233f
    predicate_hint: `0x00632337: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0063235a: jne | true=0x0063233f | false=0x0063235c
    predicate_hint: `0x00632352: cmp dword ptr [0xf5c8e4], -1`

### 0x00631f80
- blocks=6, insns=54, edges=10, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - WayPoints
- branch conditions:
  - 0x00631fa0: jle | true=0x00631fa5 | false=0x00631fa2
    predicate_hint: `0x00631f9a: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00631fc2: jne | true=0x00631fa4 | false=0x00631fc4
    predicate_hint: `0x00631fba: cmp dword ptr [0xf5cb50], -1`

### 0x0069ce8f
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - 0x0069ceaf: jle | true=0x0069ceb4 | false=0x0069ceb1
    predicate_hint: `0x0069cea9: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0069ced1: jne | true=0x0069ceb3 | false=0x0069ced3
    predicate_hint: `0x0069cec9: cmp dword ptr [0xf78020], -1`

### 0x0058680d
- blocks=4, insns=52, edges=9, jcc=2, switch_indirect=0, truncated=False
- patterns:
  - WayPoints
- branch conditions:
  - 0x0058682d: jg | true=0x00586838 | false=0x0058682f
    predicate_hint: `0x00586827: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0058684a: jne | true=0x0058682f | false=0x0058684c
    predicate_hint: `0x00586842: cmp dword ptr [0xdf7b00], -1`

### 0x00580590
- blocks=4, insns=32, edges=7, jcc=2, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedInLargeSectorPredicate@EGL@@
- branch conditions:
  - 0x005805a6: je | true=0x005805c9 | false=0x005805a8
    predicate_hint: `0x005805a4: test al, al`
  - 0x005805b8: je | true=0x005805c9 | false=0x005805ba
    predicate_hint: `0x005805b6: test eax, eax`

### 0x0069a053
- blocks=4, insns=27, edges=8, jcc=2, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - 0x0069a06b: je | true=0x0069a086 | false=0x0069a06d
    predicate_hint: `0x0069a069: test eax, eax`
  - 0x0069a07b: je | true=0x0069a086 | false=0x0069a07d
    predicate_hint: `0x0069a079: test eax, eax`

### 0x005805d1
- blocks=5, insns=25, edges=7, jcc=2, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedInSectorPredicate@EGL@@
- branch conditions:
  - 0x005805e4: je | true=0x005805fe | false=0x005805e6
    predicate_hint: `0x005805e2: test al, al`
  - 0x005805f7: jne | true=0x005805fe | false=0x005805f9
    predicate_hint: `0x005805f4: cmp eax, dword ptr [esi + 0xc]`

### 0x0069a48a
- blocks=4, insns=465, edges=21, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069a4aa: jg | true=0x0069a4b5 | false=0x0069a4ac
    predicate_hint: `0x0069a4a4: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0069a4c7: jne | true=0x0069a4ac | false=0x0069a4c9
    predicate_hint: `0x0069a4bf: cmp dword ptr [0xf77db0], -1`

### 0x006880a6
- blocks=4, insns=373, edges=37, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006880c6: jg | true=0x006880d1 | false=0x006880c8
    predicate_hint: `0x006880c0: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006880e3: jne | true=0x006880c8 | false=0x006880e5
    predicate_hint: `0x006880db: cmp dword ptr [0xf73ad8], -1`

### 0x00627469
- blocks=4, insns=160, edges=11, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00627489: jg | true=0x00627494 | false=0x0062748b
    predicate_hint: `0x00627483: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006274a6: jne | true=0x0062748b | false=0x006274a8
    predicate_hint: `0x0062749e: cmp dword ptr [0xf583ec], -1`

### 0x0064d55d
- blocks=4, insns=111, edges=12, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0064d57d: jg | true=0x0064d588 | false=0x0064d57f
    predicate_hint: `0x0064d577: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0064d59a: jne | true=0x0064d57f | false=0x0064d59c
    predicate_hint: `0x0064d592: cmp dword ptr [0xf64478], -1`

### 0x006c528d
- blocks=4, insns=84, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006c52ad: jg | true=0x006c52b8 | false=0x006c52af
    predicate_hint: `0x006c52a7: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006c52ca: jne | true=0x006c52af | false=0x006c52cc
    predicate_hint: `0x006c52c2: cmp dword ptr [0xf810f8], -1`

### 0x006748a0
- blocks=4, insns=80, edges=9, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006748c0: jg | true=0x006748cb | false=0x006748c2
    predicate_hint: `0x006748ba: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006748dd: jne | true=0x006748c2 | false=0x006748df
    predicate_hint: `0x006748d5: cmp dword ptr [0xf6dd20], -1`

### 0x00638b95
- blocks=6, insns=76, edges=14, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00638bb5: jle | true=0x00638bba | false=0x00638bb7
    predicate_hint: `0x00638baf: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00638bd7: jne | true=0x00638bb9 | false=0x00638bd9
    predicate_hint: `0x00638bcf: cmp dword ptr [0xf5eb40], -1`

### 0x00628848
- blocks=4, insns=71, edges=9, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00628868: jg | true=0x00628873 | false=0x0062886a
    predicate_hint: `0x00628862: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00628885: jne | true=0x0062886a | false=0x00628887
    predicate_hint: `0x0062887d: cmp dword ptr [0xf59350], -1`

### 0x00680907
- blocks=4, insns=69, edges=9, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00680927: jg | true=0x00680932 | false=0x00680929
    predicate_hint: `0x00680921: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00680944: jne | true=0x00680929 | false=0x00680946
    predicate_hint: `0x0068093c: cmp dword ptr [0xf71ae4], -1`

### 0x00648cb5
- blocks=6, insns=67, edges=11, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00648cd5: jle | true=0x00648cda | false=0x00648cd7
    predicate_hint: `0x00648ccf: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00648cf7: jne | true=0x00648cd9 | false=0x00648cf9
    predicate_hint: `0x00648cef: cmp dword ptr [0xf62d54], -1`

### 0x0062876f
- blocks=4, insns=64, edges=11, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0062878f: jg | true=0x0062879a | false=0x00628791
    predicate_hint: `0x00628789: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006287ac: jne | true=0x00628791 | false=0x006287ae
    predicate_hint: `0x006287a4: cmp dword ptr [0xf59344], -1`

### 0x0065f4c6
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065f4e2: jbe | true=0x0065f501 | false=0x0065f4e4
    predicate_hint: `0x0065f4e0: cmp ecx, edi`
  - 0x0065f501: jae | true=0x0065f4ee | false=0x0065f503

### 0x00579005
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00579021: jbe | true=0x00579040 | false=0x00579023
    predicate_hint: `0x0057901f: cmp ecx, edi`
  - 0x00579040: jae | true=0x0057902d | false=0x00579042

### 0x0057113f
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057115b: jbe | true=0x0057117a | false=0x0057115d
    predicate_hint: `0x00571159: cmp ecx, edi`
  - 0x0057117a: jae | true=0x00571167 | false=0x0057117c

### 0x00567092
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005670ae: jbe | true=0x005670cd | false=0x005670b0
    predicate_hint: `0x005670ac: cmp ecx, edi`
  - 0x005670cd: jae | true=0x005670ba | false=0x005670cf

### 0x00559816
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00559832: jbe | true=0x00559851 | false=0x00559834
    predicate_hint: `0x00559830: cmp ecx, edi`
  - 0x00559851: jae | true=0x0055983e | false=0x00559853

### 0x0055977c
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00559798: jbe | true=0x005597b7 | false=0x0055979a
    predicate_hint: `0x00559796: cmp ecx, edi`
  - 0x005597b7: jae | true=0x005597a4 | false=0x005597b9

### 0x005584cf
- blocks=5, insns=62, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005584eb: jbe | true=0x0055850a | false=0x005584ed
    predicate_hint: `0x005584e9: cmp ecx, edi`
  - 0x0055850a: jae | true=0x005584f7 | false=0x0055850c

### 0x005c5420
- blocks=5, insns=60, edges=14, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c544c: jne | true=0x005c546d | false=0x005c544e
    predicate_hint: `0x005c5449: cmp eax, dword ptr [ebp + 8]`
  - 0x005c5480: je | true=0x005c54af | false=0x005c5482
    predicate_hint: `0x005c547e: test ecx, ecx`

### 0x0054b69b
- blocks=5, insns=56, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054b6b2: jbe | true=0x0054b6d1 | false=0x0054b6b4
    predicate_hint: `0x0054b6b0: cmp ecx, edi`
  - 0x0054b6d1: jae | true=0x0054b6be | false=0x0054b6d3

### 0x005c54f0
- blocks=6, insns=55, edges=12, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c5508: je | true=0x005c552a | false=0x005c550a
    predicate_hint: `0x005c5506: test ecx, ecx`
  - 0x005c553d: je | true=0x005c5564 | false=0x005c553f
    predicate_hint: `0x005c553b: test ecx, ecx`

### 0x0068f264
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0068f284: jle | true=0x0068f289 | false=0x0068f286
    predicate_hint: `0x0068f27e: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0068f2a6: jne | true=0x0068f288 | false=0x0068f2a8
    predicate_hint: `0x0068f29e: cmp dword ptr [0xf755a0], -1`

### 0x0068a16f
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0068a18f: jle | true=0x0068a194 | false=0x0068a191
    predicate_hint: `0x0068a189: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0068a1b1: jne | true=0x0068a193 | false=0x0068a1b3
    predicate_hint: `0x0068a1a9: cmp dword ptr [0xf73cf0], -1`

### 0x0066916f
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0066918f: jle | true=0x00669194 | false=0x00669191
    predicate_hint: `0x00669189: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x006691b1: jne | true=0x00669193 | false=0x006691b3
    predicate_hint: `0x006691a9: cmp dword ptr [0xf692d0], -1`

### 0x00668ca6
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00668cc6: jle | true=0x00668ccb | false=0x00668cc8
    predicate_hint: `0x00668cc0: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00668ce8: jne | true=0x00668cca | false=0x00668cea
    predicate_hint: `0x00668ce0: cmp dword ptr [0xf69270], -1`

### 0x00638923
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00638943: jle | true=0x00638948 | false=0x00638945
    predicate_hint: `0x0063893d: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00638965: jne | true=0x00638947 | false=0x00638967
    predicate_hint: `0x0063895d: cmp dword ptr [0xf5e7c4], -1`

### 0x00631daa
- blocks=6, insns=52, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00631dca: jle | true=0x00631dcf | false=0x00631dcc
    predicate_hint: `0x00631dc4: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x00631dec: jne | true=0x00631dce | false=0x00631dee
    predicate_hint: `0x00631de4: cmp dword ptr [0xf5cc80], -1`

### 0x0060b776
- blocks=4, insns=52, edges=9, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060b796: jg | true=0x0060b7a1 | false=0x0060b798
    predicate_hint: `0x0060b790: cmp eax, dword ptr [ecx + 0x3adc]`
  - 0x0060b7b3: jne | true=0x0060b798 | false=0x0060b7b5
    predicate_hint: `0x0060b7ab: cmp dword ptr [0xf54ef8], -1`

### 0x005c57f0
- blocks=5, insns=52, edges=12, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c5815: ja | true=0x005c5825 | false=0x005c5817
    predicate_hint: `0x005c5812: cmp ecx, dword ptr [ebp + 0xc]`
  - 0x005c5829: jbe | true=0x005c586f | false=0x005c582b
    predicate_hint: `0x005c5825: cmp dword ptr [ebp + 0xc], 0`

### 0x00582930
- blocks=4, insns=51, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00582942: je | true=0x005829a4 | false=0x00582944
    predicate_hint: `0x00582940: test al, al`
  - 0x00582969: je | true=0x005829a4 | false=0x0058296b
    predicate_hint: `0x00582967: test al, al`

### 0x00606b46
- blocks=5, insns=48, edges=14, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00606b56: je | true=0x00606b71 | false=0x00606b58
    predicate_hint: `0x00606b54: test edi, edi`
  - 0x00606b5d: je | true=0x00606b68 | false=0x00606b5f
    predicate_hint: `0x00606b5b: test eax, eax`

### 0x00554f4d
- blocks=3, insns=46, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00554f92: jne | true=0x00554f85 | false=0x00554f94
    predicate_hint: `0x00554f8f: sub esi, 1`

### 0x006b7e86
- blocks=4, insns=44, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006b7e99: jnp | true=0x006b7ef8 | false=0x006b7e9b
    predicate_hint: `0x006b7e96: test ah, 0x44`
  - 0x006b7ec6: jbe | true=0x006b7ef8 | false=0x006b7ec8
    predicate_hint: `0x006b7ec2: comiss xmm0, dword ptr [esi + 0x48]`

### 0x0059ffc0
- blocks=7, insns=44, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0059ffe2: je | true=0x0059ffe6 | false=0x0059ffe4
    predicate_hint: `0x0059ffdb: cmp dword ptr [0xf4ace4], 0`
  - 0x0059fffe: je | true=0x005a000d | false=0x005a0000
    predicate_hint: `0x0059fffa: cmp dword ptr [ebp - 0x10], 0`

### 0x006b0cfa
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006b0d11: jae | true=0x006b0d37 | false=0x006b0d13
    predicate_hint: `0x006b0d0f: cmp eax, edi`
  - 0x006b0d23: jb | true=0x006b0d3e | false=0x006b0d25
    predicate_hint: `0x006b0d21: cmp ecx, edi`

### 0x006b0c54
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006b0c6b: jae | true=0x006b0c91 | false=0x006b0c6d
    predicate_hint: `0x006b0c69: cmp eax, edi`
  - 0x006b0c7d: jb | true=0x006b0c98 | false=0x006b0c7f
    predicate_hint: `0x006b0c7b: cmp ecx, edi`

### 0x006b0c01
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006b0c18: jae | true=0x006b0c3e | false=0x006b0c1a
    predicate_hint: `0x006b0c16: cmp eax, edi`
  - 0x006b0c2a: jb | true=0x006b0c45 | false=0x006b0c2c
    predicate_hint: `0x006b0c28: cmp ecx, edi`

### 0x006a3a0a
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006a3a21: jae | true=0x006a3a47 | false=0x006a3a23
    predicate_hint: `0x006a3a1f: cmp eax, edi`
  - 0x006a3a33: jb | true=0x006a3a4e | false=0x006a3a35
    predicate_hint: `0x006a3a31: cmp ecx, edi`

### 0x0069ff61
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069ff78: jae | true=0x0069ff9e | false=0x0069ff7a
    predicate_hint: `0x0069ff76: cmp eax, edi`
  - 0x0069ff8a: jb | true=0x0069ffa5 | false=0x0069ff8c
    predicate_hint: `0x0069ff88: cmp ecx, edi`

### 0x0066d679
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0066d690: jae | true=0x0066d6b6 | false=0x0066d692
    predicate_hint: `0x0066d68e: cmp eax, edi`
  - 0x0066d6a2: jb | true=0x0066d6bd | false=0x0066d6a4
    predicate_hint: `0x0066d6a0: cmp ecx, edi`

### 0x0061e909
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0061e920: jae | true=0x0061e946 | false=0x0061e922
    predicate_hint: `0x0061e91e: cmp eax, edi`
  - 0x0061e932: jb | true=0x0061e94d | false=0x0061e934
    predicate_hint: `0x0061e930: cmp ecx, edi`

### 0x00611669
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00611680: jae | true=0x006116a6 | false=0x00611682
    predicate_hint: `0x0061167e: cmp eax, edi`
  - 0x00611692: jb | true=0x006116ad | false=0x00611694
    predicate_hint: `0x00611690: cmp ecx, edi`

### 0x0060ba28
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060ba3f: jae | true=0x0060ba65 | false=0x0060ba41
    predicate_hint: `0x0060ba3d: cmp eax, edi`
  - 0x0060ba51: jb | true=0x0060ba6c | false=0x0060ba53
    predicate_hint: `0x0060ba4f: cmp ecx, edi`

### 0x0060ae05
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0060ae1c: jae | true=0x0060ae42 | false=0x0060ae1e
    predicate_hint: `0x0060ae1a: cmp eax, edi`
  - 0x0060ae2e: jb | true=0x0060ae49 | false=0x0060ae30
    predicate_hint: `0x0060ae2c: cmp ecx, edi`

### 0x005810d1
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005810e8: jae | true=0x0058110e | false=0x005810ea
    predicate_hint: `0x005810e6: cmp eax, edi`
  - 0x005810fa: jb | true=0x00581115 | false=0x005810fc
    predicate_hint: `0x005810f8: cmp ecx, edi`

### 0x0056eb81
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056eb98: jae | true=0x0056ebbe | false=0x0056eb9a
    predicate_hint: `0x0056eb96: cmp eax, edi`
  - 0x0056ebaa: jb | true=0x0056ebc5 | false=0x0056ebac
    predicate_hint: `0x0056eba8: cmp ecx, edi`

### 0x00569763
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056977a: jae | true=0x005697a0 | false=0x0056977c
    predicate_hint: `0x00569778: cmp eax, edi`
  - 0x0056978c: jb | true=0x005697a7 | false=0x0056978e
    predicate_hint: `0x0056978a: cmp ecx, edi`

### 0x0056833a
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00568351: jae | true=0x00568377 | false=0x00568353
    predicate_hint: `0x0056834f: cmp eax, edi`
  - 0x00568363: jb | true=0x0056837e | false=0x00568365
    predicate_hint: `0x00568361: cmp ecx, edi`

### 0x00566fb5
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00566fcc: jae | true=0x00566ff2 | false=0x00566fce
    predicate_hint: `0x00566fca: cmp eax, edi`
  - 0x00566fde: jb | true=0x00566ff9 | false=0x00566fe0
    predicate_hint: `0x00566fdc: cmp ecx, edi`

### 0x0055b203
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055b21a: jae | true=0x0055b240 | false=0x0055b21c
    predicate_hint: `0x0055b218: cmp eax, edi`
  - 0x0055b22c: jb | true=0x0055b247 | false=0x0055b22e
    predicate_hint: `0x0055b22a: cmp ecx, edi`

### 0x0051b48f
- blocks=5, insns=41, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0051b4a6: jae | true=0x0051b4cc | false=0x0051b4a8
    predicate_hint: `0x0051b4a4: cmp eax, edi`
  - 0x0051b4b8: jb | true=0x0051b4d3 | false=0x0051b4ba
    predicate_hint: `0x0051b4b6: cmp ecx, edi`

### 0x00570fb3
- blocks=5, insns=40, edges=6, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00570fc3: je | true=0x00570ff1 | false=0x00570fc5
    predicate_hint: `0x00570fc1: test eax, eax`
  - 0x00570fe3: je | true=0x00570ff0 | false=0x00570fe5
    predicate_hint: `0x00570fe0: cmp eax, -1`

### 0x00641654
- blocks=5, insns=37, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00641689: je | true=0x00641693 | false=0x0064168b
    predicate_hint: `0x00641687: test al, al`
  - 0x0064168d: jne | true=0x00641693 | false=0x0064168f
    predicate_hint: `0x0064168b: cmp edi, esi`

### 0x006a930f
- blocks=6, insns=36, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006a9322: jne | true=0x006a9328 | false=0x006a9324
    predicate_hint: `0x006a9320: test edi, edi`
  - 0x006a932e: ja | true=0x006a9352 | false=0x006a9330
    predicate_hint: `0x006a9328: cmp edi, 0xaaaaaaa`

### 0x0065bd8c
- blocks=6, insns=36, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065bd9f: jne | true=0x0065bda5 | false=0x0065bda1
    predicate_hint: `0x0065bd9d: test edi, edi`
  - 0x0065bdab: ja | true=0x0065bdcf | false=0x0065bdad
    predicate_hint: `0x0065bda5: cmp edi, 0x1fffffff`

### 0x00569602
- blocks=6, insns=36, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00569615: jne | true=0x0056961b | false=0x00569617
    predicate_hint: `0x00569613: test edi, edi`
  - 0x00569621: ja | true=0x00569645 | false=0x00569623
    predicate_hint: `0x0056961b: cmp edi, 0x3fffffff`

### 0x00699e58
- blocks=5, insns=33, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00699e71: jne | true=0x00699e9a | false=0x00699e73
    predicate_hint: `0x00699e6f: test eax, eax`
  - 0x00699e8f: jle | true=0x00699ea4 | false=0x00699e91
    predicate_hint: `0x00699e89: cmp ecx, dword ptr [eax + 0x130]`

### 0x005652c9
- blocks=6, insns=33, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005652d6: jne | true=0x005652dc | false=0x005652d8
    predicate_hint: `0x005652d4: test esi, esi`
  - 0x005652e2: ja | true=0x00565306 | false=0x005652e4
    predicate_hint: `0x005652dc: cmp esi, 0x7ffffff`

### 0x006516a1
- blocks=5, insns=31, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006516b4: jae | true=0x006516d9 | false=0x006516b6
    predicate_hint: `0x006516b2: cmp eax, ecx`
  - 0x006516c4: jb | true=0x006516de | false=0x006516c6
    predicate_hint: `0x006516c2: cmp eax, ecx`

### 0x0061e8bd
- blocks=5, insns=31, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0061e8d0: jae | true=0x0061e8f5 | false=0x0061e8d2
    predicate_hint: `0x0061e8ce: cmp eax, ecx`
  - 0x0061e8e0: jb | true=0x0061e8fa | false=0x0061e8e2
    predicate_hint: `0x0061e8de: cmp eax, ecx`

### 0x00611f33
- blocks=5, insns=31, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00611f46: jae | true=0x00611f6b | false=0x00611f48
    predicate_hint: `0x00611f44: cmp eax, ecx`
  - 0x00611f56: jb | true=0x00611f70 | false=0x00611f58
    predicate_hint: `0x00611f54: cmp eax, ecx`

### 0x0055a6d2
- blocks=5, insns=31, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055a6e4: jae | true=0x0055a708 | false=0x0055a6e6
    predicate_hint: `0x0055a6e2: cmp eax, ecx`
  - 0x0055a6f3: jb | true=0x0055a70d | false=0x0055a6f5
    predicate_hint: `0x0055a6f1: cmp eax, ecx`

### 0x0069fe5d
- blocks=3, insns=30, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069fe78: je | true=0x0069fe89 | false=0x0069fe7a
    predicate_hint: `0x0069fe76: cmp edi, ebx`
  - 0x0069fe87: jne | true=0x0069fe7a | false=0x0069fe89
    predicate_hint: `0x0069fe85: cmp esi, ebx`

### 0x005769ed
- blocks=3, insns=29, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005769fe: jne | true=0x00576a29 | false=0x00576a00
    predicate_hint: `0x005769fa: cmp byte ptr [esi + 0xd], 0`
  - 0x00576a27: je | true=0x00576a00 | false=0x00576a29
    predicate_hint: `0x00576a23: cmp byte ptr [edi + 0xd], 0`

### 0x0054b4bd
- blocks=3, insns=29, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054b4da: je | true=0x0054b4eb | false=0x0054b4dc
    predicate_hint: `0x0054b4d8: cmp edi, ebx`
  - 0x0054b4e9: jne | true=0x0054b4dc | false=0x0054b4eb
    predicate_hint: `0x0054b4e7: cmp esi, ebx`

### 0x0065f312
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065f32d: je | true=0x0065f33d | false=0x0065f32f
    predicate_hint: `0x0065f32b: cmp edi, ebx`
  - 0x0065f33b: jne | true=0x0065f32f | false=0x0065f33d
    predicate_hint: `0x0065f339: cmp esi, ebx`

### 0x00578e2e
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00578e49: je | true=0x00578e59 | false=0x00578e4b
    predicate_hint: `0x00578e47: cmp edi, ebx`
  - 0x00578e57: jne | true=0x00578e4b | false=0x00578e59
    predicate_hint: `0x00578e55: cmp esi, ebx`

### 0x00566eb3
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00566ece: je | true=0x00566ede | false=0x00566ed0
    predicate_hint: `0x00566ecc: cmp edi, ebx`
  - 0x00566edc: jne | true=0x00566ed0 | false=0x00566ede
    predicate_hint: `0x00566eda: cmp esi, ebx`

### 0x00564601
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056461c: je | true=0x0056462c | false=0x0056461e
    predicate_hint: `0x0056461a: cmp edi, ebx`
  - 0x0056462a: jne | true=0x0056461e | false=0x0056462c
    predicate_hint: `0x00564628: cmp esi, ebx`

### 0x00559507
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00559522: je | true=0x00559532 | false=0x00559524
    predicate_hint: `0x00559520: cmp edi, ebx`
  - 0x00559530: jne | true=0x00559524 | false=0x00559532
    predicate_hint: `0x0055952e: cmp esi, ebx`

### 0x0055833e
- blocks=3, insns=28, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00558359: je | true=0x00558369 | false=0x0055835b
    predicate_hint: `0x00558357: cmp edi, ebx`
  - 0x00558367: jne | true=0x0055835b | false=0x00558369
    predicate_hint: `0x00558365: cmp esi, ebx`

### 0x00536a01
- blocks=5, insns=28, edges=7, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00536a0f: jae | true=0x00536a2e | false=0x00536a11
    predicate_hint: `0x00536a0c: cmp eax, dword ptr [ebp + 8]`
  - 0x00536a19: jb | true=0x00536a33 | false=0x00536a1b
    predicate_hint: `0x00536a16: cmp eax, dword ptr [ebp + 8]`

### 0x0066a5b2
- blocks=3, insns=27, edges=6, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0066a5c3: jne | true=0x0066a5e6 | false=0x0066a5c5
    predicate_hint: `0x0066a5bf: cmp byte ptr [edi + 0xd], 0`
  - 0x0066a5e4: je | true=0x0066a5c5 | false=0x0066a5e6
    predicate_hint: `0x0066a5e0: cmp byte ptr [esi + 0xd], 0`

### 0x0069b103
- blocks=4, insns=25, edges=9, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069b11f: jne | true=0x0069b147 | false=0x0069b121
    predicate_hint: `0x0069b117: cmp dword ptr [eax*4 + 0xbe1434], 1`
  - 0x0069b12a: jne | true=0x0069b147 | false=0x0069b12c
    predicate_hint: `0x0069b128: test al, al`

### 0x0069c7d1
- blocks=5, insns=24, edges=10, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069c7e7: jne | true=0x0069c7f2 | false=0x0069c7e9
    predicate_hint: `0x0069c7e5: test eax, eax`
  - 0x0069c7f9: jne | true=0x0069c7ff | false=0x0069c7fb
    predicate_hint: `0x0069c7f7: test eax, eax`

### 0x0054540e
- blocks=4, insns=24, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00545422: je | true=0x0054542c | false=0x00545424
    predicate_hint: `0x00545420: cmp eax, dword ptr [esi]`
  - 0x0054542a: jge | true=0x0054542e | false=0x0054542c
    predicate_hint: `0x00545427: cmp ecx, dword ptr [eax + 0x10]`

### 0x005727d7
- blocks=3, insns=22, edges=5, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005727ea: je | true=0x005727fa | false=0x005727ec
    predicate_hint: `0x005727e8: cmp eax, esi`
  - 0x005727f8: jne | true=0x005727ec | false=0x005727fa
    predicate_hint: `0x005727f5: cmp dword ptr [ebp - 4], esi`

### 0x0069b0ab
- blocks=4, insns=20, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069b0b9: jne | true=0x0069b0df | false=0x0069b0bb
    predicate_hint: `0x0069b0b1: cmp dword ptr [eax*4 + 0xbe1434], 3`
  - 0x0069b0c2: jne | true=0x0069b0df | false=0x0069b0c4
    predicate_hint: `0x0069b0c0: test al, al`

### 0x0069ae66
- blocks=4, insns=20, edges=8, jcc=2, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069ae74: jne | true=0x0069ae9a | false=0x0069ae76
    predicate_hint: `0x0069ae6c: cmp dword ptr [eax*4 + 0xbe1434], 2`
  - 0x0069ae7d: jne | true=0x0069ae9a | false=0x0069ae7f
    predicate_hint: `0x0069ae7b: test al, al`

### 0x0069c627
- blocks=3, insns=20, edges=3, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - 0x0069c648: je | true=0x0069c64d | false=0x0069c64a
    predicate_hint: `0x0069c646: test eax, eax`

### 0x00645e98
- blocks=3, insns=18, edges=3, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - 0x00645ea8: je | true=0x00645eb4 | false=0x00645eaa
    predicate_hint: `0x00645ea2: mov dword ptr [esi], 0xbbe3c8`

### 0x00645e6a
- blocks=3, insns=18, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehaviorProperties@GGL@@
- branch conditions:
  - 0x00645e76: je | true=0x00645e82 | false=0x00645e78
    predicate_hint: `0x00645e72: test byte ptr [ebp + 8], 1`

### 0x00645c1c
- blocks=3, insns=18, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - 0x00645c28: je | true=0x00645c34 | false=0x00645c2a
    predicate_hint: `0x00645c24: test byte ptr [ebp + 8], 1`

### 0x00585f7a
- blocks=3, insns=18, edges=4, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
- branch conditions:
  - 0x00585f86: je | true=0x00585f92 | false=0x00585f88
    predicate_hint: `0x00585f82: test byte ptr [ebp + 8], 1`

### 0x004ed68d
- blocks=3, insns=18, edges=4, jcc=1, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_WORK_BUILDING_SUCCESS
- branch conditions:
  - 0x004ed68d: jo | true=0x004ed694 | false=0x004ed68f

### 0x0069826d
- blocks=3, insns=17, edges=3, jcc=1, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - 0x00698276: je | true=0x00698282 | false=0x00698278
    predicate_hint: `0x00698270: mov dword ptr [esi], 0xbbe3c8`

### 0x005c4f70
- blocks=5, insns=121, edges=27, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c5022: je | true=0x005c507b | false=0x005c5024
    predicate_hint: `0x005c501f: cmp dword ptr [eax], 0`

### 0x005c9800
- blocks=5, insns=105, edges=23, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005c983d: jne | true=0x005c984b | false=0x005c983f
    predicate_hint: `0x005c9839: cmp dword ptr [ebp + 8], 0`

### 0x005b8720
- blocks=5, insns=105, edges=23, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005b875d: jne | true=0x005b876b | false=0x005b875f
    predicate_hint: `0x005b8759: cmp dword ptr [ebp + 8], 0`

### 0x005364d4
- blocks=3, insns=86, edges=12, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00536519: jae | true=0x00536523 | false=0x0053651b
    predicate_hint: `0x00536517: cmp eax, ecx`

### 0x005131e7
- blocks=3, insns=82, edges=26, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00513277: je | true=0x00513283 | false=0x00513279
    predicate_hint: `0x00513275: test ecx, ecx`

### 0x00581065
- blocks=3, insns=61, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0058109d: je | true=0x005810b3 | false=0x0058109f
    predicate_hint: `0x00581097: cmp dword ptr [esi], 0`

### 0x0056eb15
- blocks=3, insns=61, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0056eb4d: je | true=0x0056eb63 | false=0x0056eb4f
    predicate_hint: `0x0056eb47: cmp dword ptr [esi], 0`

### 0x005696ac
- blocks=3, insns=61, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005696e4: je | true=0x005696fa | false=0x005696e6
    predicate_hint: `0x005696de: cmp dword ptr [esi], 0`

### 0x0051b423
- blocks=3, insns=61, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0051b45b: je | true=0x0051b471 | false=0x0051b45d
    predicate_hint: `0x0051b455: cmp dword ptr [esi], 0`

### 0x00893fa0
- blocks=3, insns=58, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00893ff9: je | true=0x00894005 | false=0x00893ffb
    predicate_hint: `0x00893ff7: cmp ecx, eax`

### 0x0059f950
- blocks=4, insns=55, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0059f999: je | true=0x0059f9aa | false=0x0059f99b
    predicate_hint: `0x0059f997: test esi, esi`

### 0x005cc960
- blocks=3, insns=54, edges=13, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005cc982: je | true=0x005cc9ea | false=0x005cc984
    predicate_hint: `0x005cc97f: cmp eax, dword ptr [ebp + 8]`

### 0x0063ade6
- blocks=3, insns=52, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063adf6: jne | true=0x0063ae43 | false=0x0063adf8
    predicate_hint: `0x0063adf3: mov dword ptr [ebp - 0x14], esi`

### 0x006ad089
- blocks=3, insns=51, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006ad0b8: je | true=0x006ad0cf | false=0x006ad0ba
    predicate_hint: `0x006ad0b5: cmp dword ptr [esi], 0`

### 0x00651640
- blocks=3, insns=51, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065166f: je | true=0x00651686 | false=0x00651671
    predicate_hint: `0x0065166c: cmp dword ptr [esi], 0`

### 0x0055a673
- blocks=3, insns=51, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055a6a1: je | true=0x0055a6b7 | false=0x0055a6a3
    predicate_hint: `0x0055a69e: cmp dword ptr [esi], 0`

### 0x007ebdd0
- blocks=3, insns=49, edges=8, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007ebe02: je | true=0x007ebe0e | false=0x007ebe04
    predicate_hint: `0x007ebe00: cmp ecx, eax`

### 0x005369a7
- blocks=3, insns=49, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005369d3: je | true=0x005369e7 | false=0x005369d5
    predicate_hint: `0x005369d0: cmp dword ptr [esi], 0`

### 0x00894120
- blocks=3, insns=43, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0089414f: je | true=0x0089415b | false=0x00894151
    predicate_hint: `0x0089414d: cmp ecx, eax`

### 0x006b9462
- blocks=3, insns=43, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006b9485: je | true=0x006b94a1 | false=0x006b9487
    predicate_hint: `0x006b9483: test al, al`

### 0x007eb5e3
- blocks=3, insns=42, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007eb604: je | true=0x007eb610 | false=0x007eb606
    predicate_hint: `0x007eb602: cmp ecx, eax`

### 0x007ec3d6
- blocks=3, insns=37, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007ec40c: je | true=0x007ec418 | false=0x007ec40e
    predicate_hint: `0x007ec40a: cmp ecx, eax`

### 0x007eb060
- blocks=3, insns=37, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x007eb096: je | true=0x007eb0a2 | false=0x007eb098
    predicate_hint: `0x007eb094: cmp ecx, eax`

### 0x0067403a
- blocks=3, insns=36, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00674067: je | true=0x00674075 | false=0x00674069
    predicate_hint: `0x00674065: cmp edx, dword ptr [ecx]`

### 0x0084ae63
- blocks=3, insns=35, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0084ae92: je | true=0x0084ae9e | false=0x0084ae94
    predicate_hint: `0x0084ae90: cmp ecx, eax`

### 0x0063b393
- blocks=3, insns=34, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063b399: je | true=0x0063b3cc | false=0x0063b39b
    predicate_hint: `0x0063b396: cmp esi, dword ptr [ebp + 8]`

### 0x0065e2e1
- blocks=3, insns=31, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0065e2fd: je | true=0x0065e31f | false=0x0065e2ff
    predicate_hint: `0x0065e2fb: test ecx, ecx`

### 0x005cc4a0
- blocks=4, insns=31, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005cc4ab: jne | true=0x005cc4c7 | false=0x005cc4ad
    predicate_hint: `0x005cc4a7: cmp dword ptr [ebp + 0xc], 1`

### 0x00576df0
- blocks=3, insns=31, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00576e11: je | true=0x00576e25 | false=0x00576e13
    predicate_hint: `0x00576e0f: test al, al`

### 0x00534739
- blocks=4, insns=31, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00534740: je | true=0x00534756 | false=0x00534742
    predicate_hint: `0x0053473c: cmp dword ptr [ebp + 0x10], 0`

### 0x00894213
- blocks=3, insns=30, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00894236: je | true=0x00894242 | false=0x00894238
    predicate_hint: `0x00894234: cmp ecx, eax`

### 0x005cc910
- blocks=4, insns=29, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005cc924: ja | true=0x005cc934 | false=0x005cc926
    predicate_hint: `0x005cc922: cmp ecx, dword ptr [eax]`

### 0x005684d7
- blocks=3, insns=28, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005684ea: je | true=0x005684fe | false=0x005684ec
    predicate_hint: `0x005684e8: test al, al`

### 0x0054c2a6
- blocks=3, insns=28, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054c2b0: je | true=0x0054c2ea | false=0x0054c2b2
    predicate_hint: `0x0054c2ac: cmp dword ptr [eax + 0x5c], 0`

### 0x0053095d
- blocks=3, insns=25, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00530974: je | true=0x00530986 | false=0x00530976
    predicate_hint: `0x00530972: test edi, edi`

### 0x0069ec2d
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069ec32: jne | true=0x0069ec41 | false=0x0069ec34
    predicate_hint: `0x0069ec30: test esi, esi`

### 0x0069ce69
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069ce6e: jne | true=0x0069ce7d | false=0x0069ce70
    predicate_hint: `0x0069ce6c: test esi, esi`

### 0x0067a91d
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0067a922: jne | true=0x0067a931 | false=0x0067a924
    predicate_hint: `0x0067a920: test esi, esi`

### 0x006785a8
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006785ad: jne | true=0x006785bc | false=0x006785af
    predicate_hint: `0x006785ab: test esi, esi`

### 0x00678182
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00678187: jne | true=0x00678196 | false=0x00678189
    predicate_hint: `0x00678185: test esi, esi`

### 0x0066b228
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0066b22d: jne | true=0x0066b23c | false=0x0066b22f
    predicate_hint: `0x0066b22b: test esi, esi`

### 0x00668ba1
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00668ba6: jne | true=0x00668bb5 | false=0x00668ba8
    predicate_hint: `0x00668ba4: test esi, esi`

### 0x0063afc4
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0063afc9: jne | true=0x0063afd8 | false=0x0063afcb
    predicate_hint: `0x0063afc7: test esi, esi`

### 0x00633f1a
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00633f1f: jne | true=0x00633f2e | false=0x00633f21
    predicate_hint: `0x00633f1d: test esi, esi`

### 0x00586054
- blocks=3, insns=23, edges=7, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00586059: jne | true=0x00586068 | false=0x0058605b
    predicate_hint: `0x00586057: test esi, esi`

### 0x00587cd5
- blocks=3, insns=22, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00587ce9: je | true=0x00587cf4 | false=0x00587ceb
    predicate_hint: `0x00587ce7: test edi, edi`

### 0x006754b8
- blocks=3, insns=21, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x006754cc: je | true=0x006754d6 | false=0x006754ce
    predicate_hint: `0x006754ca: test edi, edi`

### 0x00644b9e
- blocks=3, insns=21, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00644bb6: je | true=0x00644bc5 | false=0x00644bb8
    predicate_hint: `0x00644bb1: add eax, 0xf61700`

### 0x0058064c
- blocks=3, insns=21, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00580662: je | true=0x0058066e | false=0x00580664
    predicate_hint: `0x0058065e: test byte ptr [ebp + 8], 1`

### 0x0057ff1d
- blocks=3, insns=21, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0057ff31: je | true=0x0057ff3d | false=0x0057ff33
    predicate_hint: `0x0057ff2f: test edi, edi`

### 0x0055c446
- blocks=4, insns=21, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055c456: je | true=0x0055c45f | false=0x0055c458
    predicate_hint: `0x0055c454: test al, al`

### 0x0054a55f
- blocks=3, insns=21, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0054a577: je | true=0x0054a586 | false=0x0054a579
    predicate_hint: `0x0054a572: add eax, 0xdd8480`

### 0x005fd587
- blocks=3, insns=20, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x005fd59b: je | true=0x005fd5aa | false=0x005fd59d
    predicate_hint: `0x005fd599: test esi, esi`

### 0x00575fc7
- blocks=3, insns=19, edges=5, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00575fdd: je | true=0x00575ff7 | false=0x00575fdf
    predicate_hint: `0x00575fd9: cmp dword ptr [esi + 0x18], 0`

### 0x0069c99d
- blocks=3, insns=18, edges=6, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069c9a7: jne | true=0x0069c9c5 | false=0x0069c9a9
    predicate_hint: `0x0069c9a5: test al, al`

### 0x0058062a
- blocks=3, insns=18, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00580636: je | true=0x00580642 | false=0x00580638
    predicate_hint: `0x00580632: test byte ptr [ebp + 8], 1`

### 0x00532259
- blocks=3, insns=18, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0053226c: je | true=0x0053227d | false=0x0053226e
    predicate_hint: `0x0053226a: test edx, edx`

### 0x00532281
- blocks=3, insns=17, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00532294: je | true=0x005322a3 | false=0x00532296
    predicate_hint: `0x00532292: test edx, edx`

### 0x0069c12e
- blocks=3, insns=15, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069c13a: jne | true=0x0069c143 | false=0x0069c13c
    predicate_hint: `0x0069c136: cmp byte ptr [esi + 0x3d], 0`

### 0x0069b4d7
- blocks=3, insns=15, edges=4, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0069b4e1: je | true=0x0069b4f0 | false=0x0069b4e3
    predicate_hint: `0x0069b4df: test al, al`

### 0x0055fc14
- blocks=3, insns=15, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0055fc27: je | true=0x0055fc30 | false=0x0055fc29
    predicate_hint: `0x0055fc25: test edx, edx`

### 0x00871230
- blocks=3, insns=14, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0087123b: je | true=0x00871247 | false=0x0087123d
    predicate_hint: `0x00871239: cmp ecx, eax`

### 0x0068a306
- blocks=3, insns=13, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x0068a319: je | true=0x0068a31e | false=0x0068a31b
    predicate_hint: `0x0068a317: test ecx, ecx`

### 0x00607853
- blocks=3, insns=13, edges=3, jcc=1, switch_indirect=0, truncated=False
- branch conditions:
  - 0x00607862: je | true=0x00607869 | false=0x00607864
    predicate_hint: `0x00607860: test eax, eax`

### 0x008ecf90
- blocks=1, insns=17, edges=1, jcc=0, switch_indirect=0, truncated=False
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

### 0x004f74f0
- blocks=1, insns=8, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
  - .?AVCCamperBehavior@GGL@@
  - .?AVCWorkerAlarmModeBehavior@GGL@@
  - .?AVCWorkerBehavior@GGL@@
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - none

### 0x00645be5
- blocks=1, insns=7, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00645e91
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehaviorProperties@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00580675
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCPotentialCampSitePredicate@GGL@@
  - .?AVCUnblockedInLargeSectorPredicate@EGL@@
  - .?AVCUnblockedInSectorPredicate@EGL@@
- branch conditions:
  - none

### 0x0069d023
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehavior@GGL@@
  - .?AVCWorkerFleeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00696d33
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehavior@GGL@@
  - .?AVCWorkerAlarmModeBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x0064629f
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampWithFreeSlotPredicate@GGL@@
  - .?AVCPotentialCampSitePredicate@GGL@@
- branch conditions:
  - none

### 0x00645def
- blocks=1, insns=33, edges=4, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - none

### 0x00696a75
- blocks=1, insns=18, edges=3, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehavior@GGL@@
- branch conditions:
  - none

### 0x00645ff9
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - none

### 0x00645e40
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - none

### 0x005804ab
- blocks=1, insns=14, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCBlockingStatusPredicate@EGL@@
- branch conditions:
  - none

### 0x004d634a
- blocks=1, insns=14, edges=2, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - UpdateBlocking
- branch conditions:
  - none

### 0x005804d4
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedAreasPredicate@EGL@@
- branch conditions:
  - none

### 0x0056cf36
- blocks=1, insns=13, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCAStar64Normal@EGL@@
- branch conditions:
  - none

### 0x004ed5d7
- blocks=1, insns=11, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_EAT_BUILDING_SUCCESS
- branch conditions:
  - none

### 0x004ed9e7
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - TASK_GO_TO_CAMP
- branch conditions:
  - none

### 0x004ed9b9
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - TASK_GO_TO_BLOCKED_PILE
- branch conditions:
  - none

### 0x004ed60b
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHECK_GO_TO_REST_BUILDING_SUCCESS
- branch conditions:
  - none

### 0x004ed50a
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - TASK_CHANGE_WORK_TIME_CAMP
- branch conditions:
  - none

### 0x004ebfbf
- blocks=1, insns=10, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - CheckSettlerPlacement
- branch conditions:
  - none

### 0x00697f7b
- blocks=1, insns=9, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00585f60
- blocks=1, insns=8, edges=1, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
  - .?AVCPath@GGL@@
- branch conditions:
  - none

### 0x004f0b10
- blocks=1, insns=6, edges=0, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - none

### 0x00634fdd
- blocks=1, insns=5, edges=1, jcc=0, switch_indirect=1, truncated=False
- classes:
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - none
- indirect jumps:
  - 0x00634fe3: jmp dword ptr [eax + 0x10]

### 0x004f0ee0
- blocks=1, insns=4, edges=1, jcc=0, switch_indirect=0, truncated=False
- patterns:
  - WorkerAlarmMode
- branch conditions:
  - none

### 0x00698266
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehavior@GGL@@
- branch conditions:
  - none

### 0x00698062
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerBehaviorProps@GGL@@
- branch conditions:
  - none

### 0x00660af3
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerFleeBehavior@GGL@@
- branch conditions:
  - none

### 0x006464b5
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampWithFreeSlotPredicate@GGL@@
- branch conditions:
  - none

### 0x0063b4c7
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCBuildBlockedOnlyPredicate@?A0xe5557549@GGL@@
- branch conditions:
  - none

### 0x0062e056
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCamperBehavior@GGL@@
- branch conditions:
  - none

### 0x0058b20e
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCWorkerAlarmModeBehavior@GGL@@
- branch conditions:
  - none

### 0x00586227
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCoarsePath@EGL@@
- branch conditions:
  - none

### 0x0056a50a
- blocks=1, insns=3, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCBlockingStatusPredicate@EGL@@
- branch conditions:
  - none

### 0x00645e67
- blocks=1, insns=2, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehavior@GGL@@
- branch conditions:
  - none

### 0x00645c19
- blocks=1, insns=2, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCCampBehaviorProperties@GGL@@
- branch conditions:
  - none

### 0x00585f77
- blocks=1, insns=2, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCPath@EGL@@
- branch conditions:
  - none

### 0x00580649
- blocks=1, insns=2, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedBuildingAreasPredicate@EGL@@
- branch conditions:
  - none

### 0x00580627
- blocks=1, insns=2, edges=0, jcc=0, switch_indirect=0, truncated=False
- classes:
  - .?AVCUnblockedAreasPredicate@EGL@@
- branch conditions:
  - none

### 0x005fd315
- blocks=1, insns=38, edges=2, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0061c64c
- blocks=1, insns=31, edges=3, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0064ec2c
- blocks=1, insns=26, edges=3, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x006b07f3
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x006a9423
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0067cfe0
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0061e633
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00611570
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0060ad20
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0058e49d
- blocks=1, insns=23, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0055b125
- blocks=1, insns=23, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c4cf0
- blocks=1, insns=22, edges=3, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0063423e
- blocks=1, insns=19, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00611e48
- blocks=1, insns=19, edges=0, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0056a408
- blocks=2, insns=17, edges=4, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00547cad
- blocks=1, insns=17, edges=2, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00674bc6
- blocks=1, insns=16, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00674b83
- blocks=1, insns=16, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005a1700
- blocks=1, insns=15, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x006a236e
- blocks=1, insns=14, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005fa320
- blocks=1, insns=14, edges=3, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005fac30
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005fac10
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c9fe0
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c9fc0
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c9fa0
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c5400
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005c53e0
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005b8940
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005a2aa0
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005a2a80
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x005a2a60
- blocks=1, insns=13, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x00674ba9
- blocks=1, insns=12, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0052cf4b
- blocks=1, insns=12, edges=2, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0066d329
- blocks=1, insns=9, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x0063499c
- blocks=1, insns=7, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

### 0x006a36ec
- blocks=1, insns=6, edges=1, jcc=0, switch_indirect=0, truncated=False
- branch conditions:
  - none

## Limits

- Static CFG only; no runtime traces.
- Function boundaries and call-chain context are heuristic.
- Predicate hints are inferred from nearby disassembly text.
