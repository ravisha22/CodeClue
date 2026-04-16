### blind-requests-struct-1
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | COVERED | COVERED | COVERED | MISS | 3/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| Goldeneye | COVERED | COVERED | COVERED | MISS | 3/4 |

### blind-echo-struct-2
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | COVERED | MISS | COVERED | MISS | 2/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| Goldeneye | COVERED | MISS | COVERED | COVERED | 3/4 |

### blind-requests-rel-1
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | COVERED | COVERED | COVERED | MISS | 3/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | MISS | 3/4 |
| Goldeneye | COVERED | COVERED | COVERED | MISS | 3/4 |

### blind-echo-rel-1
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | COVERED | COVERED | MISS | COVERED | 3/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| Goldeneye | COVERED | COVERED | MISS | COVERED | 3/4 |

### blind-requests-mech-2
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | MISS | MISS | COVERED | COVERED | 2/4 |
| Sonnet 4.6 | MISS | MISS | COVERED | COVERED | 2/4 |
| Goldeneye | MISS | MISS | MISS | MISS | 0/4 |

### blind-echo-mech-1
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | COVERED | COVERED | MISS | MISS | 2/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | MISS | 3/4 |
| Goldeneye | COVERED | COVERED | MISS | MISS | 2/4 |

### blind-click-2
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | MISS | MISS | MISS | COVERED | 1/4 |
| Sonnet 4.6 | COVERED | MISS | MISS | COVERED | 2/4 |
| Goldeneye | MISS | MISS | MISS | COVERED | 1/4 |

### blind-zod-mech-1
| Model | F1 | F2 | F3 | F4 | Score |
| --- | --- | --- | --- | --- | --- |
| GPT-5.4 | MISS | MISS | MISS | MISS | 0/4 |
| Sonnet 4.6 | COVERED | COVERED | COVERED | COVERED | 4/4 |
| Goldeneye | MISS | MISS | MISS | MISS | 0/4 |

1. Grand total per model (scaffold)
   - GPT-5.4: 16/32
   - Sonnet 4.6: 26/32
   - Goldeneye: 15/32

2. Side-by-side: pre-scaffold vs scaffold per model
   - GPT-5.4: 24/32 -> 16/32
   - Sonnet 4.6: 16/32 -> 26/32
   - Goldeneye: 14/32 -> 15/32

3. Did the scaffold help? By how much per model?
   - GPT-5.4: No. -8 points.
   - Sonnet 4.6: Yes. +10 points.
   - Goldeneye: Slightly. +1 point.
