
import pytest  # type: ignore  # NOQA
from ruamel.yaml.docinfo import Version, version, Tag, DocInfo  # NOQA


class TestVersion:
    def test_create_from_integers(self) -> None:
        v = Version(1, 2)
        assert v.major == 1
        assert v.minor == 2

    def test_create_using_generator(self) -> None:
        v = version(1, 2)
        assert isinstance(v, Version)
        assert v.major == 1
        assert v.minor == 2

    def test_create_from_string_using_generator(self) -> None:
        v = version('1.2')
        assert isinstance(v, Version)
        assert v.major == 1
        assert v.minor == 2

    def test_create_from_string_extra_param(self) -> None:
        with pytest.raises(AssertionError):
            _ = version('1.2', 3)

    def test_create_from_single_integer(self) -> None:
        with pytest.raises(AssertionError):
            _ = version(1)
        with pytest.raises(TypeError):
            _ = Version(1)  # type: ignore


class TestDocInfo:
    def test_empty(self) -> None:
        di = DocInfo()
        assert di.requested_version is None
        assert di.doc_version is None
        assert di.tags == []

    def test_versions(self) -> None:
        di = DocInfo(version('1.2'), version('1.1'))
        assert di.requested_version > di.doc_version  # type: ignore
