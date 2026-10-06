"""Chunking-method families (Step 3.5): one class per strategy, settings on the constructor.

A method turns one raw capture into ``list[Chunk]`` with the ``paragraph_ids``
provenance the eval scorecard anchors through (the mandatory contract —
enforced once in the ABC, not per implementation). ``MergeChunker`` is the one
chunker PLAN.md Step 2/3.5 settled on; further strategies (drop-footnotes,
section regrouping) add classes here — awaiting explicit approval and eval
evidence, never a knob flip.
"""

from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.chunking_methods.merge import MergeChunker
from uwazi_rag.use_cases.chunking_methods.passthrough import PassThroughChunker

__all__ = ["ChunkMethod", "MergeChunker", "PassThroughChunker"]
