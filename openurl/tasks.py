import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from openurl.models import Library


def get_session(config):
    """
    Build a SQLAlchemy session for the configured database
    :param config: dict of configuration values
    :return: sqlalchemy.orm.Session
    """
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    return Session()


def _parse_line(line):
    """
    Parse a single line from the OpenURL data file
    :param line: raw line from the file
    :return: (name, server) tuple, or None if the line should be skipped
    """
    line = line.strip()
    if not line:
        return None
    fields = line.split('\t')
    if len(fields) != 2:
        # The data file has a stray numeric first line; anything else
        # is genuinely malformed and worth flagging.
        if not line.isdigit():
            sys.stderr.write('Found line with wrong number of tabs: %s\n' % line)
        return None
    name, server = fields
    return name, server


def update_openurl_db(config):
    """
    Update the library table with OpenURL server information read from
    the configured data file, adding, updating and deleting entries as
    needed to reflect the file's contents.
    :param config: dict of configuration values
    """
    session = get_session(config)
    try:
        names = []
        with open(config['INSTITUTE_OPENURL_DATA']) as fh:
            for line in fh:
                parsed = _parse_line(line)
                if parsed is None:
                    continue
                name, server = parsed
                names.append(name)

                try:
                    lib = session.query(Library).filter(Library.libname == name).one()
                    if lib.libserver != server:
                        lib.libserver = server
                        sys.stderr.write('Updating OpenURL entry: %s\n' % lib)
                        session.commit()
                except NoResultFound:
                    lib = Library(libname=name, libserver=server, institute=0)
                    sys.stderr.write('Adding OpenURL entry: %s\n' % lib)
                    session.add(lib)
                    session.commit()

        records = session.query(Library).filter(~Library.libname.in_(names)).all()
        for record in records:
            sys.stderr.write('Deleting stale OpenURL entry: %s\n' % record)
            session.query(Library).filter(Library.id == record.id).delete()
        session.commit()
    finally:
        session.close()


def export_openurl_db(config):
    """
    Print all library records currently stored in the database
    :param config: dict of configuration values
    """
    session = get_session(config)
    try:
        records = session.query(Library).all()
        for r in records:
            print("{0}\t{1}".format(r.libname, r.libserver))
    finally:
        session.close()
