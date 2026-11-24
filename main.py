#!/usr/bin/env python3
"""news-23 b139 heroes-scene: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
which must be an existing directory outside this repository.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "1ddaf195790390e536424f282adfc8009b23ff08aff365d34550019aca3e5792"
EXPECTED_SIZE = 181260  # bytes of the final rendered entry.png
MIN_SIZE = 10_000
MAX_SIZE = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    here_abs = os.path.abspath(here)
    if not os.path.isdir(outdir_abs):
        fail("MAKEFUN_OUTPUT_DIR is not an existing directory: " + outdir)
    if os.path.commonpath([outdir_abs, here_abs]) == here_abs:
        fail("MAKEFUN_OUTPUT_DIR must be outside the repository")
    dst = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        fail("output would overwrite the source image")

    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        fail("cannot read entry.png: " + str(exc))

    if len(data) < MIN_SIZE:
        fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_SIZE:
        fail("entry.png too large: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")

    # Walk the PNG chunks: first chunk must be a 13-byte IHDR for 1024x1024,
    # every chunk CRC must verify, IDAT payload must be non-empty, and the
    # last chunk must be a 0-byte IEND with no trailing data.
    # Chunk layout: 4-byte length, 4-byte type, data, 4-byte CRC;
    # the next chunk starts at 12 + length.
    pos = 8
    first = True
    idat_total = 0
    while True:
        if pos + 8 > len(data):
            fail("truncated chunk header at offset %d" % pos)
        clen, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            fail("truncated chunk %r at offset %d" % (ctype, pos))
        chunk = data[pos + 4:pos + 8 + clen]
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        crc_actual = zlib.crc32(chunk) & 0xFFFFFFFF
        if crc_actual != crc_stored:
            fail("CRC mismatch in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or clen != 13:
                fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_id, comp, filt, inter = struct.unpack(
                ">IIBBBBB", data[pos + 8:pos + 21])
            if (w, h) != (1024, 1024):
                fail("IHDR dimensions are %dx%d, expected 1024x1024" % (w, h))
            if depth != 8:
                fail("IHDR bit depth is %d, expected 8" % depth)
            if ctype_id not in (2, 6):
                fail("IHDR colour type is %d, expected 2 or 6" % ctype_id)
            if comp != 0 or filt != 0 or inter != 0:
                fail("IHDR compression/filter/interlace must all be 0")
            first = False
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        pos += 12 + clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND chunk must be 0 bytes")
            if pos != len(data):
                fail("trailing data after IEND")
            break
        if pos >= len(data):
            fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small: %d bytes" % idat_total)

    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s, expected %s" % (sha, EXPECTED_SHA256))
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail("size mismatch: got %d, expected %d" % (len(data), EXPECTED_SIZE))

    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        fail("output does not match source byte-for-byte")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), sha))


if __name__ == "__main__":
    main()
