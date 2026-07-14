import pytest
from sqlalchemy import create_engine

from openurl import tasks
from openurl.models import Base, Library


@pytest.fixture
def config(tmp_path):
    db_path = tmp_path / 'test.db'
    return {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///{0}'.format(db_path),
    }


@pytest.fixture(autouse=True)
def setup_db(config):
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)
    engine.dispose()


def write_data_file(tmp_path, content, name='openurl_data.txt'):
    path = tmp_path / name
    path.write_text(content)
    return str(path)


def library_names(config):
    session = tasks.get_session(config)
    try:
        return sorted(r.libname for r in session.query(Library).all())
    finally:
        session.close()


def library_map(config):
    session = tasks.get_session(config)
    try:
        return {r.libname: r.libserver for r in session.query(Library).all()}
    finally:
        session.close()


def test_update_openurl_db_adds_new_entries(tmp_path, config):
    data_file = write_data_file(
        tmp_path,
        'Library A\thttp://a.example.com\nLibrary B\thttp://b.example.com\n',
    )
    config['INSTITUTE_OPENURL_DATA'] = data_file

    tasks.update_openurl_db(config)

    assert library_map(config) == {
        'Library A': 'http://a.example.com',
        'Library B': 'http://b.example.com',
    }


def test_update_openurl_db_updates_existing_entry(tmp_path, config):
    config['INSTITUTE_OPENURL_DATA'] = write_data_file(
        tmp_path, 'Library A\thttp://old.example.com\n'
    )
    tasks.update_openurl_db(config)

    config['INSTITUTE_OPENURL_DATA'] = write_data_file(
        tmp_path, 'Library A\thttp://new.example.com\n'
    )
    tasks.update_openurl_db(config)

    assert library_map(config) == {'Library A': 'http://new.example.com'}


def test_update_openurl_db_deletes_stale_entries(tmp_path, config):
    config['INSTITUTE_OPENURL_DATA'] = write_data_file(
        tmp_path,
        'Library A\thttp://a.example.com\nLibrary B\thttp://b.example.com\n',
    )
    tasks.update_openurl_db(config)

    config['INSTITUTE_OPENURL_DATA'] = write_data_file(
        tmp_path, 'Library A\thttp://a.example.com\n'
    )
    tasks.update_openurl_db(config)

    assert library_names(config) == ['Library A']


def test_update_openurl_db_handles_malformed_and_empty_lines(tmp_path, config, capsys):
    content = (
        '42\n'
        'Library A\thttp://a.example.com\n'
        '\n'
        'badline_without_tab\n'
        'Library B\ttoo\tmany\tfields\n'
        '   \n'
    )
    config['INSTITUTE_OPENURL_DATA'] = write_data_file(tmp_path, content)

    tasks.update_openurl_db(config)

    assert library_names(config) == ['Library A']
    captured = capsys.readouterr()
    assert 'badline_without_tab' in captured.err


def test_export_openurl_db(tmp_path, config, capsys):
    config['INSTITUTE_OPENURL_DATA'] = write_data_file(
        tmp_path, 'Library A\thttp://a.example.com\n'
    )
    tasks.update_openurl_db(config)

    tasks.export_openurl_db(config)

    captured = capsys.readouterr()
    assert captured.out == 'Library A\thttp://a.example.com\n'
