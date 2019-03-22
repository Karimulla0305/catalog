from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///tablets.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Delete TabletCompanyName if exisitng.
session.query(TabletCompanyName).delete()
# Delete TabletName if exisitng.
session.query(TabletName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Shaik Karimulla", email="karim030589@gmail.com",
             picture='http://www.enchanting-costarica.com/wp-content/'
             'uploads/2018/02/jcarvaja17-min.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample car companys
Cmp1 = TabletCompanyName(name="Asparin",
                         user_id=1)
session.add(Cmp1)
session.commit()

Cmp2 = TabletCompanyName(name="MephthalsPass",
                         user_id=1)
session.add(Cmp2)
session.commit

Cmp3 = TabletCompanyName(name="Dolo-650",
                         user_id=1)
session.add(Cmp3)
session.commit()

Cmp4 = TabletCompanyName(name="Saridon",
                         user_id=1)
session.add(Cmp4)
session.commit()

Cmp5 = TabletCompanyName(name="Citrizen",
                         user_id=1)
session.add(Cmp5)
session.commit()

Cmp6 = TabletCompanyName(name="Gonadil",
                         user_id=1)
session.add(Cmp6)
session.commit()

# Populare a cars with models for testing
# Using different users for cars names year also
N1 = TabletName(name="Omee",
                price="7,00,650",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=1,
                user_id=1)
session.add(N1)
session.commit()

N2 = TabletName(name="OroFer-XT",
                price="7,650",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=2,
                user_id=1)
session.add(N2)
session.commit()

N3 = TabletName(name="Paracetmol",
                price="650",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=3,
                user_id=1)
session.add(N3)
session.commit()

N4 = TabletName(name="Leo-cetrizen",
                price="50",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=4,
                user_id=1)
session.add(N4)
session.commit()

N5 = TabletName(name="Gelicel",
                price="70",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=5,
                user_id=1)
session.add(N5)
session.commit()

N6 = TabletName(name="Ulixir",
                price="780",
                discription="2019-02-18",
                power="2019-02-18",
                tabletcompanynameid=6,
                user_id=1)
session.add(N6)
session.commit()

print("Your tablets database has been inserted!")
