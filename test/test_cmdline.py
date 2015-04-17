from libpathod import cmdline
import tutils
import cStringIO
import mock


def test_pathod():
    assert cmdline.args_pathod(["pathod"])


@mock.patch("argparse.ArgumentParser.error")
def test_pathoc(perror):
    assert cmdline.args_pathoc(["pathoc", "foo.com", "get:/"])
    s = cStringIO.StringIO()
    tutils.raises(SystemExit, cmdline.args_pathoc, ["pathoc", "--show-uas"], s, s)

    a = cmdline.args_pathoc(["pathoc", "foo.com:8888", "get:/"])
    assert a.port == 8888

    a = cmdline.args_pathoc(["pathoc", "foo.com:xxx", "get:/"])
    assert perror.called
    perror.reset_mock()

    a = cmdline.args_pathoc(["pathoc", "-I", "10, 20", "foo.com:8888", "get:/"])
    assert a.ignorecodes == [10, 20]

    a = cmdline.args_pathoc(["pathoc", "-I", "xx, 20", "foo.com:8888", "get:/"])
    assert perror.called
    perror.reset_mock()

    a = cmdline.args_pathoc(["pathoc", "-c", "foo:10", "foo.com:8888", "get:/"])
    assert a.connect_to == ["foo", 10]

    a = cmdline.args_pathoc(["pathoc", "-c", "foo", "foo.com:8888", "get:/"])
    assert perror.called
    perror.reset_mock()

    a = cmdline.args_pathoc(["pathoc", "-c", "foo:bar", "foo.com:8888", "get:/"])
    assert perror.called
    perror.reset_mock()

    a = cmdline.args_pathoc(
        [
            "pathoc",
            "foo.com:8888",
            tutils.test_data.path("data/request")
        ]
    )
    assert len(a.requests) == 1

    tutils.raises(
        SystemExit,
        cmdline.args_pathoc,
        ["pathoc", "foo.com", "invalid"],
        s, s
    )
