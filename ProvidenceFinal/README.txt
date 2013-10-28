How do we obtained these files?

Mainly we first decide that more than 3 minutes of silence or a new recording 
are new "document" boundaries ("@"). We decide that every 10 seconds (or more) 
of silence are potential document boundaries ("@?"). This gives us the .txt in
ToSegment/, then we consider the over-segmentation (%s/@?/@) and train a topic
model on it. We use this topic model and src/split_corpus.py to split or not
according to the KL-divergence in topics between potential documents.

