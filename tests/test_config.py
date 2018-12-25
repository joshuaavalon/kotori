from pytest import raises

from kotori.config import ItemKey


def test_item_key():
    key = ItemKey(path="/origin/foo/bar.jpg")
    assert key.key_path == "/foo/bar"
    assert key.key == "foo/bar"
    assert key.transform == "origin"
    assert key.suffix == ".jpg"
    assert key.folder == "/foo"
    assert key.name == "bar"
    assert key.format == "JPEG"

    with raises(ValueError):
        ItemKey(path="/foo.jpg")

    with raises(ValueError):
        ItemKey(path="/origin/foo.jpg2")
