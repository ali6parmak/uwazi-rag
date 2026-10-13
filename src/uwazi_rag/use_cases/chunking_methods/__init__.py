"""Chunking-method families (Step 3.5 + Step 4c wave 3.1): one class per strategy.

A method turns one raw capture into ``list[Chunk]`` with the ``paragraph_ids``
provenance the eval scorecard anchors through (the mandatory contract —
enforced once in the ABC, not per implementation). ``MergeChunker`` is the
incumbent PLAN.md Step 2/3.5 chunker; the Wave 3.1 method race adds
``SegmentChunker`` (merge-off segments) and ``SectionChunker`` (heading
partition) as settings-carrying faces over the shared ``build_chunks`` —
awaiting eval evidence, never a knob flip (vic-chargebook stays
``PassThroughChunker``: pre-chunked, out of scope for the method race).
"""

from uwazi_rag.use_cases.chunking_methods.base import ChunkMethod
from uwazi_rag.use_cases.chunking_methods.merge import MergeChunker
from uwazi_rag.use_cases.chunking_methods.passthrough import PassThroughChunker
from uwazi_rag.use_cases.chunking_methods.section import SectionChunker
from uwazi_rag.use_cases.chunking_methods.section_split import SectionSplitChunker
from uwazi_rag.use_cases.chunking_methods.segment import SegmentChunker
from uwazi_rag.use_cases.chunking_methods.type_merge import TypeMergeChunker

__all__ = [
    "ChunkMethod",
    "MergeChunker",
    "PassThroughChunker",
    "SectionChunker",
    "SectionSplitChunker",
    "SegmentChunker",
    "TypeMergeChunker",
]
