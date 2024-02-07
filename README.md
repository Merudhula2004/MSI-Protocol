# MSI-Protocol

- Cache coherence protocol used in multiprocessor systems to maintain consistency among caches 
- Three possible states that a cache line can be in:
Modified (M), Shared (S), and Invalid (I)
- Each cache line is associated with one of these states, and transitions between states occur based on the operations performed by processors on the shared memory.

# Key states:
1. **Modified (M):**
- The cache line is valid, and the processor has modified its copy.
- If another processor wants to read or write to this cache line, the owning processor must either supply the data or write it back to memory.

2. **Shared (S):**
- The cache line is valid, and multiple processors may have a copy of it.
- If a processor wants to write to this cache line, it must first acquire ownership and transition the state to Modified.

3. **Invalid (I):**
- The cache line is invalid or has no meaningful data.
- If a processor wants to read or write to this cache line, it must acquire a valid copy from another cache.

# State Transition Rules:

1. **Modified to Invalid:**
- Occurs when another processor in the system modifies the data in its cache, making the current cache's Modified copy obsolete.
- Rule: When a processor in the Modified state writes to the memory, other caches' copies become invalid.

2. **Shared to Invalid:**
- Occurs when another processor in the system wants to modify the data, requiring exclusive access.
- Rule: If a processor in the Shared state wants to write, it must transition to the Invalid state to get an exclusive copy.

3. **Invalid to Shared:**
- Occurs when a processor reads data for the first time.
- Rule: If a cache is in the Invalid state, it can transition to Shared upon a read operation.

4. **Shared to Modified:**
- Occurs when a processor in the Shared state wants to write to the data.
- Rule: If a processor in the Shared state wants to write, it must transition to the Modified state to have exclusive access.


