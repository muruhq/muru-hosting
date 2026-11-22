from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UploadSourceRequest(_message.Message):
    __slots__ = ("header", "chunk")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    header: UploadSourceHeader
    chunk: bytes
    def __init__(self, header: _Optional[_Union[UploadSourceHeader, _Mapping]] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class UploadSourceHeader(_message.Message):
    __slots__ = ("name", "sha256", "commit")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    name: str
    sha256: str
    commit: str
    def __init__(self, name: _Optional[str] = ..., sha256: _Optional[str] = ..., commit: _Optional[str] = ...) -> None: ...

class Source(_message.Message):
    __slots__ = ("name", "path", "commit", "sha256", "created_unix")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    COMMIT_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    CREATED_UNIX_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    commit: str
    sha256: str
    created_unix: int
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., commit: _Optional[str] = ..., sha256: _Optional[str] = ..., created_unix: _Optional[int] = ...) -> None: ...

class ListSourcesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSourcesResponse(_message.Message):
    __slots__ = ("sources",)
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[Source]
    def __init__(self, sources: _Optional[_Iterable[_Union[Source, _Mapping]]] = ...) -> None: ...

class RemoveSourceRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RemoveSourceResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
