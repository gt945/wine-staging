import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

        self.patch_author       = header.get('author', None)
        self.patch_email        = header.get('email', None)
        self.patch_subject      = header.get('subject', None)
        self.is_binary          = False
    def read(self):
        """Return the full patch as a string."""
        return "".join(chunk for chunk in self.read_chunks())

    def __init__(self, filename, fp=None):
        self.fp       = fp if fp is not None else open(filename)
        fp.read()
        fp.read()
            fp.read()
                fp.read()
        fp.read()
        patch.is_binary = True
    if sys.version_info[0] > 2:
        author = str(email.header.make_header(email.header.decode_header(author)))
    else:
        author = ' '.join([data.decode(format or 'utf-8').encode('utf-8') for \
                          data, format in email.header.decode_header(author)])
def read_patch(filename, fp=None):
    with _FileReader(filename, fp) as fp:
                fp.read()
                fp.read()
                    fp.read()
                if 'signedoffby' not in header:
                fp.read()
                fp.read()
    result = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        return tempfile._TemporaryFileWrapper(file=open(result.name, 'r+'), \
    with tempfile.NamedTemporaryFile(mode='w+') as diff:
    with tempfile.NamedTemporaryFile(mode='w+') as intermediate:
        diff = tempfile.NamedTemporaryFile(mode='w+')
    # Basic tests for _parse_author() and _parse_subject()
    # Basic tests for read_patch()
    class PatchReaderTests(unittest.TestCase):
        def test_simple(self):
            with open("tests/simple.patch") as fp:
                source = fp.read().split("\n")

            # Test formatted git patch with author and subject
            patchfile = tempfile.NamedTemporaryFile(mode='w+')
            patchfile.write("\n".join(source))
            patchfile.flush()

            patches = list(read_patch(patchfile.name))
            self.assertEqual(len(patches), 1)
            self.assertEqual(patches[0].patch_author,   "Author Name")
            self.assertEqual(patches[0].patch_email,    "author@email.com")
            self.assertEqual(patches[0].patch_subject,  "component: Replace arg1 with arg2.")
            self.assertEqual(patches[0].patch_revision, 3)
            self.assertEqual(patches[0].signed_off_by,  [("Author Name", "author@email.com"),
                                                         ("Other Developer", "other@email.com")])
            self.assertEqual(patches[0].filename,       patchfile.name)
            self.assertEqual(patches[0].is_binary,      False)
            self.assertEqual(patches[0].modified_file,  "test.txt")

            lines = patches[0].read().rstrip("\n").split("\n")
            self.assertEqual(lines, source[10:23])

            # Test with git diff
            del source[0:10]
            self.assertTrue(source[0].startswith("diff --git"))
            patchfile = tempfile.NamedTemporaryFile(mode='w+')
            patchfile.write("\n".join(source))
            patchfile.flush()

            patches = list(read_patch(patchfile.name))
            self.assertEqual(len(patches), 1)
            self.assertEqual(patches[0].patch_author,   None)
            self.assertEqual(patches[0].patch_email,    None)
            self.assertEqual(patches[0].patch_subject,  None)
            self.assertEqual(patches[0].patch_revision, 1)
            self.assertEqual(patches[0].signed_off_by,  [])
            self.assertEqual(patches[0].filename,       patchfile.name)
            self.assertEqual(patches[0].is_binary,      False)
            self.assertEqual(patches[0].modified_file, "test.txt")

            lines = patches[0].read().rstrip("\n").split("\n")
            self.assertEqual(lines, source[:13])

            # Test with unified diff
            del source[0:2]
            self.assertTrue(source[0].startswith("---"))
            patchfile = tempfile.NamedTemporaryFile(mode='w+')
            patchfile.write("\n".join(source))
            patchfile.flush()

            patches = list(read_patch(patchfile.name))
            self.assertEqual(len(patches), 1)
            self.assertEqual(patches[0].patch_author,   None)
            self.assertEqual(patches[0].patch_email,    None)
            self.assertEqual(patches[0].patch_subject,  None)
            self.assertEqual(patches[0].patch_revision, 1)
            self.assertEqual(patches[0].signed_off_by,  [])
            self.assertEqual(patches[0].filename,       patchfile.name)
            self.assertEqual(patches[0].is_binary,      False)
            self.assertEqual(patches[0].modified_file,  "test.txt")

            lines = patches[0].read().rstrip("\n").split("\n")
            self.assertEqual(lines, source[:11])

            # Test with StringIO buffer
            fp = StringIO("\n".join(source))
            patches = list(read_patch("unknown.patch", fp))
            self.assertEqual(len(patches), 1)
            self.assertEqual(patches[0].patch_author,   None)
            self.assertEqual(patches[0].patch_email,    None)
            self.assertEqual(patches[0].patch_subject,  None)
            self.assertEqual(patches[0].patch_revision, 1)
            self.assertEqual(patches[0].signed_off_by,  [])
            self.assertEqual(patches[0].filename,       "unknown.patch")
            self.assertEqual(patches[0].is_binary,      False)
            self.assertEqual(patches[0].modified_file,  "test.txt")

    # Basic tests for apply_patch()
    class PatchApplyTests(unittest.TestCase):
        def test_apply(self):
            source = ["line1();", "line2();", "line3();",
                      "function(arg1);",
                      "line5();", "line6();", "line7();"]
            original = tempfile.NamedTemporaryFile(mode='w+')
            original.write("\n".join(source + [""]))
            original.flush()

            source = ["@@ -1,7 +1,7 @@",
                      " line1();", " line2();", " line3();",
                      "-function(arg1);",
                      "+function(arg2);",
                      " line5();", " line6();", " line7();"]
            patchfile = tempfile.NamedTemporaryFile(mode='w+')
            patchfile.write("\n".join(source + [""]))
            patchfile.flush()

            expected = ["line1();", "line2();", "line3();",
                        "function(arg2);",
                        "line5();", "line6();", "line7();"]
            result = apply_patch(original, patchfile, fuzz=0)
            lines = result.read().rstrip("\n").split("\n")
            self.assertEqual(lines, expected)

            expected = ["line1();", "line2();", "line3();",
                        "function(arg1);",
                        "line5();", "line6();", "line7();"]
            result = apply_patch(result, patchfile, reverse=True, fuzz=0)
            lines = result.read().rstrip("\n").split("\n")
            self.assertEqual(lines, expected)

            source1 = tempfile.NamedTemporaryFile(mode='w+')
            source2  = tempfile.NamedTemporaryFile(mode='w+')