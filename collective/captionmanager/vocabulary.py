from captionstransformer import registry

from zope import interface
from zope import component
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from collective.captionmanager.i18n import captionmanagerMessageFactory as _

transformers = registry.REGISTRY.keys()

format_vocabulary = SimpleVocabulary([
    SimpleTerm(transform, transform, unicode(transform))\
    for transform in transformers])

class LanguageVocabulary(object):
    interface.implements(IVocabularyFactory)

    def  __call__(self, context):
        portal_state = component.queryMultiAdapter((context, context.REQUEST),
                                         name=u'plone_portal_state')
        languages = portal_state.locale().displayNames.languages
#        codes = [language.encode('utf-8') for language in languages]
        values = languages.values()
        values.sort()
        #push first most used language
        firsts = ['fr', 'en', 'es', 'de']

        terms = []

        for code in firsts:
            terms.append(SimpleTerm(code, code, languages[code]))

        for language in values:
            #find the code
            found = None
            for code in languages:
                if language == languages[code]:
                    found = code
                    break
            if found in firsts:
                continue
            terms.append(SimpleTerm(code, code, languages[code]))

        return SimpleVocabulary(terms)


LanguageVocabularyFactory = LanguageVocabulary()
