from collections import namedtuple
Phone = namedtuple('phone', 'area_code prefix body fax')


def senthill(AreaCode, Prefix, Body):
    AreaCode = AreaCode[1:]  # Remove + at beginning
    return Phone(area_code=AreaCode, prefix=Prefix, body=Body, fax=False)


def phone(p):
    return p[0]


def basic_phone(p):
    return p


def fax_phone(p):
    return p._replace(fax=True)

functions = {
   'Senthil Gunabalan' : senthill,
   'Phone' : phone,
   'Basic Phone' : basic_phone,
   'Fax Phone' : fax_phone
}