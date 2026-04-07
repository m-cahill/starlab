"""Replay intake (M07) and replay parser substrate (M08).

M07 treats replay files as opaque bytes for policy. M08 adds a governed parser
boundary (optional ``s2protocol``) behind ``ReplayParserAdapter``.
"""
