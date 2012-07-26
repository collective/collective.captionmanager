#python
from captionstransformer import registry
from StringIO import StringIO

#zope
from zope import interface
from zope import component
from zope import schema
from z3c.form import form, button

#plone
from plone.autoform.form import AutoExtensibleForm
from plone.z3cform import layout
from plone.app.vocabularies import language

from collective.captionmanager.i18n import captionmanagerMessageFactory as _
from collective.captionmanager import vocabulary
from urllib2 import urlopen
from urlparse import urlparse, parse_qs


class FormSchema(interface.Interface):
    """Schema for this form"""

    input_link = schema.URI(title=_(u"input link"))

    output_language = schema.Choice(title=_(u"output language"),
                         vocabulary="collective.captionmanager.vocabulary.languages")

    output_format = schema.Choice(title=_(u"output format"),
                                 description=_(u"output_format_description"),
                                 vocabulary=vocabulary.format_vocabulary)


class Form(AutoExtensibleForm, form.Form):
    schema = FormSchema
    label = _(u"Youtube caption download form")

    @button.buttonAndHandler(_(u'Downlaod'))
    def handle_download(self, action):
        data, errors = self.extractData()
        input_info = registry.REGISTRY.get('transcript')
        output_info = registry.REGISTRY.get(data['output_format'])
        filename = 'captions%s' % output_info['extension']
        query = parse_qs(urlparse(data['input_link']).query,
                         keep_blank_values=True)
        url = 'http://video.google.com/timedtext?lang=%s&v=%s' % (data['output_language'],
                                                                  query['v'][0])
        text = urlopen(url)

        if text is None:
            raise Exception # TODO manage errors

        reader = input_info['reader'](text)
        captions = reader.read()

        writer = output_info['writer'](StringIO())
        writer.set_captions(captions)
        output = writer.captions_to_text()

        response = self.request.response
        contenttype = "%s; charset=utf-8" % output_info['mimetype']
        response.setHeader("Content-type", contenttype)

        response.setHeader("Content-disposition",
                           "attachment;filename=%s"%filename)
        response.write(output.encode('utf-8'))
        return output


class FormAdapter(object):
    interface.implements(FormSchema)
    def __init__(self, context):
        self.context = context


class CaptionsFromYoutubeView(layout.FormWrapper):
    form = Form
