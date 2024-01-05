import datetime
import re
import time
from datetime import datetime
from typing import Optional

import faker
import phonenumbers
from prettytable import PrettyTable
from psycopg2 import connect
from sqlalchemy import BigInteger, Date, TIMESTAMP, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, \
    SmallInteger, Text, text, Table, Column, update
from sqlalchemy import create_engine, select, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BloodBag(Base):
    __tablename__ = 'BloodBag'
    __table_args__ = (
        PrimaryKeyConstraint('BagID', name='BagID'),
    )

    BagID: Mapped[int] = mapped_column(Integer, primary_key=True)
    BloodType: Mapped[str] = mapped_column(Text)
    StorageTemperature: Mapped[int] = mapped_column(SmallInteger)

    def __init__(self, key, BloodType, StorageTemperature):
        self.BagID = key
        self.BloodType = BloodType
        self.StorageTemperature = StorageTemperature

    def __repr__(self):
        return "{}::{}::{}" \
            .format(self.BagID, self.BloodType, self.StorageTemperature)


class Donor(Base):
    __tablename__ = 'Donor'
    __table_args__ = (
        PrimaryKeyConstraint('DonorID', name='DonorID'),
    )

    DonorID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(Text)
    LastName: Mapped[str] = mapped_column(Text)
    DateOfBirth: Mapped[datetime.date] = mapped_column(Date)
    ContactNumber: Mapped[str] = mapped_column(Text)
    BloodType: Mapped[str] = mapped_column(Text)

    def __init__(self, key, FirstName, LastName, DateOfBirth, ContactNumber, BloodType):
        self.DonorID = key
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateOfBirth = DateOfBirth
        self.ContactNumber = ContactNumber
        self.BloodType = BloodType

    def __repr__(self):
        return "{}::{}::{}::{}::{}::{}" \
            .format(self.DonorID, self.FirstName, self.LastName, self.DateOfBirth, self.ContactNumber, self.BloodType)


class BloodDonation(Base):
    __tablename__ = 'BloodDonation'
    __table_args__ = (
        ForeignKeyConstraint(['DonorID'], ['Donor.DonorID'], name='DonorID'),
        PrimaryKeyConstraint('DonationID', name='DonationID')
    )

    DonationID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DonationDate: Mapped[datetime.date] = mapped_column(Date)
    DonationTime: Mapped[datetime.timestamp] = mapped_column(TIMESTAMP)
    DonorID: Mapped[int] = mapped_column(Integer)
    DonationStatus: Mapped[str] = mapped_column(Text)

    def __init__(self, key, DonationDate, DonationTime, DonorID, DonationStatus):
        self.DonationID = key
        self.DonationDate = DonationDate
        self.DonationTime = DonationTime
        self.DonorID = DonorID
        self.DonationStatus = DonationStatus

    def __repr__(self):
        return "{}::{}::{}::{}::{}" \
            .format(self.DonationID, self.DonationDate, self.DonationTime, self.DonorID, self.DonationStatus)


class t_BloodBag_BloodDonation(Base):
    __tablename__ = 'BloodBag-BloodDonation'
    BloodDonationID = Column('BloodDonationID', Integer, primary_key=True, nullable=False)
    BloodBagID = Column('BloodBagID', Integer, primary_key=True, nullable=False)
    __table_args__ = (ForeignKeyConstraint(['BloodBagID'], ['BloodBag.BagID'], name='BloodBagID'),
                      ForeignKeyConstraint(['BloodDonationID'], ['BloodDonation.DonationID'], name='BloodDonationID'),
                      PrimaryKeyConstraint('BloodDonationID', 'BloodBagID', name='BloodBag-BloodDonation_pkey'))

    def __init__(self, BloodDonationID, BloodBagID):
        self.BloodBagID = BloodBagID
        self.BloodDonationID = BloodDonationID

    def __repr__(self):
        return "{}::{}" \
            .format(self.BloodDonationID, self.BloodBagID)


class Recipient(Base):
    __tablename__ = 'Recipient'
    __table_args__ = (
        ForeignKeyConstraint(['BloodBagID'], ['BloodBag.BagID'], name='BloodBagID'),
        PrimaryKeyConstraint('RecipientID', name='RecipientID')
    )

    RecipientID: Mapped[int] = mapped_column(Integer, primary_key=True)
    FirstName: Mapped[str] = mapped_column(Text)
    LastName: Mapped[str] = mapped_column(Text)
    DateOfBirth: Mapped[datetime.date] = mapped_column(Date)
    ContactNumber: Mapped[str] = mapped_column(Text)
    BloodTypeNeeded: Mapped[str] = mapped_column(Text)
    BloodBagID: Mapped[Optional[int]] = mapped_column(Integer)

    def __init__(self, key, FirstName, LastName, DateOfBirth, ContactNumber, BloodTypeNeeded, BloodBagID):
        self.RecipientID = key
        self.FirstName = FirstName
        self.LastName = LastName
        self.DateOfBirth = DateOfBirth
        self.ContactNumber = ContactNumber
        self.BloodTypeNeeded = BloodTypeNeeded
        self.BloodBagID = BloodBagID

    def __repr__(self):
        return "{}::{}::{}::{}::{}::{}::{}" \
            .format(self.RecipientID, self.FirstName, self.LastName, self.DateOfBirth, self.ContactNumber,
                    self.BloodTypeNeeded, self.BloodBagID)


class BloodBank(Base):
    __tablename__ = 'BloodBank'
    __table_args__ = (
        ForeignKeyConstraint(['BloodDonationID'], ['BloodDonation.DonationID'], name='BloodDonationID'),
        PrimaryKeyConstraint('BloodBankID', name='BloodBankID')
    )

    BloodBankID: Mapped[int] = mapped_column(Integer, primary_key=True)
    Name: Mapped[str] = mapped_column(Text)
    Location: Mapped[str] = mapped_column(Text)
    ContactNumber: Mapped[str] = mapped_column(Text)
    TotalDonations: Mapped[int] = mapped_column(BigInteger, server_default=text('0'))
    BloodDonationID: Mapped[Optional[int]] = mapped_column(Integer)

    def __init__(self, key, Name, Location, ContactNumber, TotalDonations, BloodDonationID):
        self.BloodBankID = key
        self.Name = Name
        self.Location = Location
        self.ContactNumber = ContactNumber
        self.TotalDonations = TotalDonations
        self.BloodDonationID = BloodDonationID

    def __repr__(self):
        return "{}::{}::{}::{}::{}::{}" \
            .format(self.BloodBankID, self.Name, self.Location, self.ContactNumber, self.TotalDonations,
                    self.BloodDonationID)


use_faker = True
faker.Faker.seed(time.time())
fake = faker.Faker()
use_alchemy = True


def verify_value(selected_table, selected_param, entered_param, typeof) -> bool:
    format_for_date = "%Y-%m-%d"
    format_for_timestamp = "%Y-%m-%d %H-%M-%S"
    if (((selected_table == 1 and selected_param == 2) or (selected_table == 5 and selected_param == 6) or
         (selected_table == 6 and selected_param == 6)) and
            entered_param not in ['A+', 'O+', 'B+', 'AB+', 'A-', 'O-', 'B-', 'AB-']):
        # BloodBag.BloodType, Recipient.BloodTypeNeeded, Donor.BloodType
        return False
    if ((selected_table == 1 and selected_param == 3) and
            not (17 < int(entered_param) < 24)):  # BloodBag.StorageTemperature
        return False
    if typeof == 'date':
        try:
            check_date = bool(datetime.strptime(entered_param, format_for_date))
        except ValueError:
            check_date = False
        return check_date
    if typeof == 'timestamp without time zone':
        try:
            check_date = bool(datetime.strptime(entered_param, format_for_timestamp))
        except ValueError:
            check_date = False
        return check_date
    if (selected_table == 3 and selected_param == 4) or (selected_table == 5 and
                                                         selected_param == 5) or (selected_table == 6
                                                                                  and selected_param == 5):
        # ContactNumber
        phone_number = phonenumbers.parse(entered_param)
        if not phonenumbers.is_possible_number(phone_number):
            return False
    if (typeof == 'integer' or typeof == 'smallint' or typeof == 'bigint') and isinstance(entered_param, str):
        if not (entered_param.isnumeric()):
            return False
    if typeof == 'text' and not (selected_table == 3 and selected_param == 3):  # Address can contain all symbols
        if not re.search("^[A-Z][a-z]", entered_param):
            return False
    return True


class Model:
    tables = {
        1: {1: 'BloodBag',
            2: {1: 'BagID', 2: 'BloodType', 3: 'StorageTemperature'}},
        2: {1: 'BloodBag-BloodDonation',
            2: {1: 'BloodDonationID', 2: 'BloodBagID'}},
        3: {1: 'BloodBank',
            2: {1: 'BloodBankID', 2: 'Name', 3: 'Location', 4: 'ContactNumber', 5: 'TotalDonations',
                6: 'BloodDonationID'}},
        4: {1: 'BloodDonation',
            2: {1: 'DonationID', 2: 'DonationDate', 3: 'DonationTime', 4: 'DonorID', 5: 'DonationStatus'}},
        5: {1: 'Donor',
            2: {1: 'DonorID', 2: 'FirstName', 3: 'LastName', 4: 'DateOfBirth',
                5: 'ContactNumber', 6: 'BloodType'}},
        6: {1: 'Recipient',
            2: {1: 'RecipientID', 2: 'FirstName', 3: 'LastName', 4: 'DateOfBirth',
                5: 'ContactNumber', 6: 'BloodTypeNeeded', 7: 'BloodBagID'}}
    }
    classes_table = {1: BloodBag, 2: t_BloodBag_BloodDonation, 3: BloodBank, 4: BloodDonation, 5: Donor, 6: Recipient}
    session = None

    def __init__(self, connection_settings):
        if use_alchemy:
            db_url = (f"postgresql://{connection_settings['user']}:"
                      f"{connection_settings['password']}@{connection_settings['host']}:"
                      f"{connection_settings['port']}/{connection_settings['dbname']}")
            engine = create_engine(db_url)
            Session = sessionmaker(engine)
            self.session = Session()
        else:
            self.connection = connect(
                dbname=connection_settings['dbname'],
                user=connection_settings['user'],
                password=connection_settings['password'],
                host=connection_settings['host'],
                port=connection_settings['port']
            )

    def execute(self, execute_string, params=None):
        cursor = self.connection.cursor()
        cursor.execute(execute_string, params)
        self.connection.commit()
        return cursor

    def get_table(self, selected_table):
        if use_alchemy:
            res = self.session.query(self.classes_table[selected_table]).all()
            column_names = []
            for data in self.tables[selected_table][2]:
                column_names.append(self.tables[selected_table][2][data])
            x = PrettyTable()
            x.field_names = column_names

            for data in res:
                in_string = str(data)
                x.add_row(in_string.split('::'))
            return x
        else:
            return self.execute(f'SELECT * FROM "{self.tables[selected_table][1]}"')

    def get_params(self, selected_table):
        return self.tables[selected_table][2]

    def add_table(self, selected_table, entered_params):
        stmt = None
        if selected_table == 1:
            stmt = BloodBag(key=entered_params[1], BloodType=entered_params[2], StorageTemperature=entered_params[3])
        elif selected_table == 2:
            stmt = t_BloodBag_BloodDonation(entered_params[1], entered_params[2])
        elif selected_table == 3:
            stmt = BloodBank(entered_params[1], entered_params[2], entered_params[3], entered_params[4],
                             entered_params[5], entered_params[6])
        elif selected_table == 4:
            stmt = BloodDonation(entered_params[1], entered_params[2], entered_params[3], entered_params[4],
                                 entered_params[5])
        elif selected_table == 5:
            stmt = Donor(entered_params[1], entered_params[2], entered_params[3], entered_params[4],
                         entered_params[5], entered_params[6])
        elif selected_table == 6:
            stmt = Recipient(entered_params[1], entered_params[2], entered_params[3], entered_params[4],
                             entered_params[5], entered_params[6], entered_params[7])
        self.session.add(stmt)
        self.session.commit()

    def delete_table(self, selected_table, selected_id):
        if selected_table == 1:
            status = self.session.query(self.classes_table[1]).filter(
                self.classes_table[1].BagID == selected_id).delete()
        elif selected_table == 2:
            status = (self.session.query(self.classes_table[2])
                      .filter(self.classes_table[2].BloodDonationID == selected_id).delete())
        elif selected_table == 3:
            status = self.session.query(self.classes_table[3]).filter(
                self.classes_table[3].BloodBankID == selected_id).delete()
        elif selected_table == 4:
            status = self.session.query(self.classes_table[4]).filter(
                self.classes_table[4].DonationID == selected_id).delete()
        elif selected_table == 5:
            status = self.session.query(self.classes_table[5]).filter(
                self.classes_table[5].DonorID == selected_id).delete()
        elif selected_table == 6:
            status = self.session.query(self.classes_table[6]).filter(
                self.classes_table[6].RecipientID == selected_id).delete()

        self.session.commit()

    def edit_table(self, selected_table, selected_id, selected_param, entered_param):
        stmt = None
        if selected_table == 1:
            if selected_param == 1:
                stmt = (update(self.classes_table[1]).where(self.classes_table[1].BagID == selected_id)
                        .values({self.classes_table[1].BagID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[1]).where(self.classes_table[1].BagID == selected_id)
                        .values({self.classes_table[1].BloodType: entered_param}))
            elif selected_param == 3:
                stmt = (update(self.classes_table[1]).where(self.classes_table[1].BagID == selected_id)
                        .values({self.classes_table[1].StorageTemperature: entered_param}))
        elif selected_table == 2:
            if selected_param == 1:
                stmt = (update(self.classes_table[2]).where(self.classes_table[2].BloodDonationID == selected_id)
                        .values({self.classes_table[2].BloodDonationID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[2]).where(self.classes_table[2].BloodDonationID == selected_id)
                        .values({self.classes_table[2].BloodBagID: entered_param}))
        elif selected_table == 3:
            if selected_param == 1:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].BloodBankID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].Name: entered_param}))
            elif selected_param == 3:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].Location: entered_param}))
            if selected_param == 4:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].ContactNumber: entered_param}))
            elif selected_param == 5:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].TotalDonations: entered_param}))
            elif selected_param == 6:
                stmt = (update(self.classes_table[3]).where(self.classes_table[3].BloodBankID == selected_id)
                        .values({self.classes_table[3].BloodDonationID: entered_param}))
        elif selected_table == 4:
            if selected_param == 1:
                stmt = (update(self.classes_table[4]).where(self.classes_table[4].DonationID == selected_id)
                        .values({self.classes_table[4].DonationID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[4]).where(self.classes_table[4].DonationID == selected_id)
                        .values({self.classes_table[4].DonationDate: entered_param}))
            elif selected_param == 3:
                stmt = (update(self.classes_table[4]).where(self.classes_table[4].DonationID == selected_id)
                        .values({self.classes_table[4].DonationTime: entered_param}))
            elif selected_param == 4:
                stmt = (update(self.classes_table[4]).where(self.classes_table[4].DonationID == selected_id)
                        .values({self.classes_table[4].DonorID: entered_param}))
            elif selected_param == 5:
                stmt = (update(self.classes_table[4]).where(self.classes_table[4].DonationID == selected_id)
                        .values({self.classes_table[4].DonationStatus: entered_param}))
        elif selected_table == 5:
            if selected_param == 1:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].DonorID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].FirstName: entered_param}))
            elif selected_param == 3:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].LastName: entered_param}))
            elif selected_param == 4:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].DateOfBirth: entered_param}))
            elif selected_param == 5:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].ContactNumber: entered_param}))
            elif selected_param == 6:
                stmt = (update(self.classes_table[5]).where(self.classes_table[5].DonorID == selected_id)
                        .values({self.classes_table[5].BloodType: entered_param}))
        elif selected_table == 6:
            if selected_param == 1:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].RecipientID: entered_param}))
            elif selected_param == 2:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].FirstName: entered_param}))
            elif selected_param == 3:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].LastName: entered_param}))
            if selected_param == 4:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].DateOfBirth: entered_param}))
            elif selected_param == 5:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].ContactNumber: entered_param}))
            elif selected_param == 6:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].BloodTypeNeeded: entered_param}))
            elif selected_param == 7:
                stmt = (update(self.classes_table[6]).where(self.classes_table[6].RecipientID == selected_id)
                        .values({self.classes_table[6].BloodBagID: entered_param}))

        self.session.execute(stmt)
        self.session.commit()
