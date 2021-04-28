
from pydicates import Predicate, Context, BOOLEANS

# We can interpret predicates only in specific context
# let create context for boolean operations

# create empty context
boolean_context = Context()

# fill context with predefined boolean operations
boolean_context.bulk_register(BOOLEANS)


# define constructor for custom predicate
def OwnedBy(owner_id):
    # second argument can be any object,
    # that store predicate specific data
    return Predicate('owned_by', owner_id)


# define processor for custom predicate
# first argument — context, in case you need to evaluate other predicates
# second argument — predicate data, stored in its constructor
# third and next arguments — current evaluation context, for example, checked document
def owned_by(context, owner_id, document):
    return document['owner'] == owner_id


# register predicate processor in context
boolean_context.register('owned_by', owned_by)


# define one more predicate
def HasTag(tag):
    return Predicate('has_tag', tag)


def has_tag(context, tag, document):
    return tag in document['tags']


boolean_context.register('has_tag', has_tag)


# some test documents
document_1 = {'owner': 'alex', 'tags': ('gamedev', 'game-design')}
document_2 = {'owner': 'bob', 'tags': ('gamedev', 'game-design')}
document_3 = {'owner': 'alice', 'tags': ('gamedev',)}
document_4 = {'owner': 'alice', 'tags': ('gamedev', 'game-design')}


# check which game design document belong to Alex
condition_1 = OwnedBy('alex') & HasTag('game-design')

assert boolean_context(condition_1, document_1)
assert not boolean_context(condition_1, document_2)
assert not boolean_context(condition_1, document_3)
assert not boolean_context(condition_1, document_4)

# check which game design document belong to Alex or Alice
condition_2 = (OwnedBy('alex') | OwnedBy('alice')) & HasTag('game-design')

assert boolean_context(condition_2, document_1)
assert not boolean_context(condition_2, document_2)
assert not boolean_context(condition_2, document_3)
assert boolean_context(condition_2, document_4)
