from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Institute(Base):
    __tablename__ = 'institute'
    id = Column(Integer, primary_key=True)
    canonical_name = Column(String)
    city = Column(String)
    street = Column(String)
    state = Column(String)
    country = Column(String)
    ringgold_id = Column(Integer)
    ads_id = Column(String)

    def __repr__(self):
        return '<Institute, name: {0}, Ringgold ID: {1}, ADS ID: {2}>'.format(
            self.canonical_name, self.ringgold_id, self.ads_id)


class Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True)
    libserver = Column(String)
    iconurl = Column(String)
    libname = Column(String)
    institute = Column(Integer, ForeignKey('institute.id'))

    def __repr__(self):
        return '<Library, name: {0}, OpenURL server: {1}, OpenURL icon: {2}>'.format(
            self.libname, self.libserver, self.iconurl)
