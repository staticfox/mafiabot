def public(c, e, bot):
    print(e.arguments)
    print(e.source.nick)
    print(e.source)
    print(e.target)
    print(e)
    print(dir(e))
    print(e.__dict__)
    pass

def private(c, e, bot):
    pass
