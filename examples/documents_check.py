
from pydicates import Predicate, Context, BOOLEANS

# We can interpret predicates only in a specific context.
# Let create the context for boolean operations.

# Create empty context.
boolean_context = Context()

# Fill context with predefined boolean operations.
boolean_context.bulk_register(BOOLEANS)


# Define the constructor for custom predicate.
def OwnedBy(owner_id):
    # Second argument can be any object,
    # that store predicate specific data.
    return Predicate('owned_by', owner_id)


# Define processor for custom predicate.
# The first argument — context, in case you need to calculate child predicates.
# The second argument — predicate data, which we stored in its constructor.
# The third and next arguments — current calculation context, for example, current document.
def owned_by(context, owner_id, document):
    return document['owner'] == owner_id


# Register predicate processor in the context.
boolean_context.register('owned_by', owned_by)


# Define one more predicate.
def HasTag(tag):
    return Predicate('has_tag', tag)


def has_tag(context, tag, document):
    return tag in document['tags']


boolean_context.register('has_tag', has_tag)


# Some test documents.
document_1 = {'owner': 'alex', 'tags': ('gamedev', 'game-design')}
document_2 = {'owner': 'bob', 'tags': ('gamedev', 'game-design')}
document_3 = {'owner': 'alice', 'tags': ('gamedev',)}
document_4 = {'owner': 'alice', 'tags': ('gamedev', 'game-design')}


# Check which game design document belong to Alex.
condition_1 = OwnedBy('alex') & HasTag('game-design')

assert boolean_context(condition_1, document_1)
assert not boolean_context(condition_1, document_2)
assert not boolean_context(condition_1, document_3)
assert not boolean_context(condition_1, document_4)

# Check which game design document belong to Alex or Alice.
condition_2 = (OwnedBy('alex') | OwnedBy('alice')) & HasTag('game-design')

assert boolean_context(condition_2, document_1)
assert not boolean_context(condition_2, document_2)
assert not boolean_context(condition_2, document_3)
assert boolean_context(condition_2, document_4)
