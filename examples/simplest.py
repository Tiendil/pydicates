
from pydicates import Predicate, common


def HasTag(tag):
    return Predicate('has_tag', tag)


def has_tag(context, tag, document):
    return tag in document['tags']


common.register('has_tag', has_tag)


document = {'tags': ('a', 'b', 'c', 'd')}


assert common(HasTag('a') & HasTag('c'), document)
assert not common(HasTag('a') & HasTag('e'), document)
assert common(HasTag('a') & ~HasTag('e'), document)
assert common(HasTag('a') & (HasTag('e') | HasTag('d')), document)
