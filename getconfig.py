from lxml import etree

def get_config_value(value):
    f = open('config.xml', 'r')
    conf = f.read()
    parser = etree.XMLParser()
    parser.feed(conf)
    root = parser.close()
    nobj = etree.ElementTree(root)
    return nobj.find(value.split('.')[0]).findtext(value.split('.')[1])

